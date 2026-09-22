from .model import Opcode, TypeTag
from .isa import result_type
from .errors import VerifyError

CONTROL={Opcode.JUMP,Opcode.BRANCH,Opcode.CALL,Opcode.RETURN,Opcode.HALT}

def verify(program):
    defined=set(); types={}; qstate_live={}; portals={}; roads={}
    for pc,i in enumerate(program.instructions):
        if i.out is not None and not (0<=i.out<256): raise VerifyError(f'pc {pc}: output register out of range')
        for r in i.args:
            if r not in defined: raise VerifyError(f'pc {pc}: use before define r{r}')
        if i.out is not None and i.out in defined: raise VerifyError(f'pc {pc}: register redefinition r{i.out}')
        expected=result_type(i.op)
        if i.out is not None and expected not in (TypeTag.ANY,TypeTag.VOID) and i.result_type not in (expected,TypeTag.ANY):
            raise VerifyError(f'pc {pc}: result type {i.result_type} != {expected}')
        if i.op==Opcode.Q_MEASURE:
            if not i.args: raise VerifyError('Q_MEASURE missing qstate')
            q=i.args[0]
            if not qstate_live.get(q,False): raise VerifyError(f'pc {pc}: QSTATE r{q} not live')
            qstate_live[q]=False
        elif i.op in (Opcode.Q_SUPERPOSE,Opcode.Q_CHANNEL):
            if not i.args: raise VerifyError(f'{i.op.name} missing qstate')
            q=i.args[0]
            if not qstate_live.get(q,False): raise VerifyError(f'pc {pc}: QSTATE r{q} not live')
            qstate_live[q]=False
        elif i.op==Opcode.Q_ENTANGLE:
            if len(i.args)<2: raise VerifyError('Q_ENTANGLE requires two qstates')
            for q in i.args[:2]:
                if not qstate_live.get(q,False): raise VerifyError(f'pc {pc}: QSTATE r{q} not live')
                qstate_live[q]=False
        if i.op==Opcode.PORTAL_OPEN and i.out is not None: portals[i.out]='OPEN'
        if i.op==Opcode.PORTAL_CLOSE:
            p=i.args[0]
            if portals.get(p)!='OPEN': raise VerifyError(f'pc {pc}: portal r{p} is not OPEN')
            portals[p]='CLOSED'
        if i.op==Opcode.ROAD_BEGIN and i.out is not None: roads[i.out]='OPEN'
        if i.op==Opcode.ROAD_APPEND:
            r=i.args[0]
            if roads.get(r)!='OPEN': raise VerifyError(f'pc {pc}: road r{r} is not OPEN')
            roads[r]='MOVED'
        if i.op==Opcode.ROAD_CLOSE:
            r=i.args[0]
            if roads.get(r)!='OPEN': raise VerifyError(f'pc {pc}: road r{r} is not OPEN')
            roads[r]='CLOSED'
        if i.out is not None:
            defined.add(i.out); types[i.out]=i.result_type
            if i.result_type==TypeTag.QSTATE: qstate_live[i.out]=True
            if i.op==Opcode.ROAD_APPEND: roads[i.out]='OPEN'
        if i.op in (Opcode.JUMP,Opcode.CALL):
            t=i.attrs.get('target')
            if not isinstance(t,int) or not (0<=t<len(program.instructions)): raise VerifyError(f'pc {pc}: invalid target')
        if i.op==Opcode.BRANCH:
            for key in ('true','false'):
                t=i.attrs.get(key)
                if not isinstance(t,int) or not (0<=t<len(program.instructions)): raise VerifyError(f'pc {pc}: invalid branch {key}')
    openp=[r for r,s in portals.items() if s=='OPEN']
    openr=[r for r,s in roads.items() if s=='OPEN']
    if openp: raise VerifyError(f'unclosed portals: {openp}')
    if openr: raise VerifyError(f'unclosed roads: {openr}')
    for e in program.exports:
        if e not in defined: raise VerifyError(f'undefined export r{e}')
    return {'ok':True,'registers':len(defined),'instructions':len(program.instructions),'exports':list(program.exports)}
