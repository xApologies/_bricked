from __future__ import annotations
from .model import *
from .isa import result_type
from .errors import VerifyError
Q_UNARY={Opcode.Q_SUPERPOSE,Opcode.Q_CHANNEL,Opcode.Q_MEASURE}

def _state_key(pc,defined,types,qlive,portals,roads):
    return (pc,tuple(sorted(defined)),tuple(sorted((k,v.value) for k,v in types.items())),tuple(sorted(qlive.items())),tuple(sorted(portals.items())),tuple(sorted(roads.items())))

def verify(program,max_states=200000):
    n=len(program.instructions)
    if not n: raise VerifyError('empty program','VERIFY_EMPTY')
    work=[(0,set(),{}, {}, {}, {})]; seen=set(); halt_paths=0; explored=0; maxreg=-1
    while work:
        pc,defined,types,qlive,portals,roads=work.pop(); explored+=1
        if explored>max_states: raise VerifyError('control-flow verification state budget exceeded','VERIFY_BUDGET')
        if not 0<=pc<n: raise VerifyError(f'pc out of range {pc}','VERIFY_TARGET')
        key=_state_key(pc,defined,types,qlive,portals,roads)
        if key in seen: continue
        seen.add(key)
        i=program.instructions[pc]; d=set(defined); ty=dict(types); q=dict(qlive); po=dict(portals); ro=dict(roads)
        for r in i.args:
            if r not in d: raise VerifyError(f'pc {pc}: use before define r{r}','VERIFY_USE_BEFORE_DEFINE')
            maxreg=max(maxreg,r)
        if i.out is not None:
            if i.out in d: raise VerifyError(f'pc {pc}: register redefinition r{i.out}','VERIFY_REDEFINE')
            if not 0<=i.out<256: raise VerifyError('register out of range','VERIFY_REGISTER')
            maxreg=max(maxreg,i.out)
        exp=result_type(i.op)
        if i.out is not None and exp not in (TypeTag.ANY,TypeTag.VOID) and i.result_type not in (exp,TypeTag.ANY):
            raise VerifyError(f'pc {pc}: result type {i.result_type} != {exp}','VERIFY_RESULT_TYPE')
        if i.op==Opcode.BRANCH and (len(i.args)!=1 or ty.get(i.args[0]) not in (TypeTag.BOOL,TypeTag.ANY)):
            raise VerifyError(f'pc {pc}: BRANCH requires BOOL','VERIFY_BRANCH_TYPE')
        if i.op==Opcode.BOOL_NOT and ty.get(i.args[0]) not in (TypeTag.BOOL,TypeTag.ANY): raise VerifyError('BOOL_NOT operand','VERIFY_DATA_TYPE')
        if i.op in (Opcode.BOOL_AND,Opcode.BOOL_OR) and any(ty.get(r) not in (TypeTag.BOOL,TypeTag.ANY) for r in i.args): raise VerifyError('boolean operands','VERIFY_DATA_TYPE')
        if i.op in (Opcode.INT_ADD,Opcode.INT_SUB,Opcode.INT_LT,Opcode.INT_LE) and any(ty.get(r) not in (TypeTag.INT,TypeTag.ANY) for r in i.args): raise VerifyError('integer operands','VERIFY_DATA_TYPE')
        if i.op in Q_UNARY:
            qr=i.args[0]
            if not q.get(qr,False): raise VerifyError(f'pc {pc}: QSTATE r{qr} not live','VERIFY_QSTATE_CONSUMED')
            q[qr]=False
        elif i.op==Opcode.Q_ENTANGLE:
            if len(i.args)<2 or i.args[0]==i.args[1]: raise VerifyError('Q_ENTANGLE requires two distinct qstates','VERIFY_QSTATE_ALIAS')
            for qr in i.args[:2]:
                if not q.get(qr,False): raise VerifyError(f'pc {pc}: QSTATE r{qr} not live','VERIFY_QSTATE_CONSUMED')
                q[qr]=False
        if i.op==Opcode.PORTAL_OPEN and i.out is not None: po[i.out]='OPEN'
        if i.op==Opcode.PORTAL_CLOSE:
            pr=i.args[0]
            if po.get(pr)!='OPEN': raise VerifyError(f'pc {pc}: portal r{pr} not OPEN','VERIFY_PORTAL_STATE')
            po[pr]='CLOSED'
        if i.op==Opcode.ROAD_BEGIN and i.out is not None: ro[i.out]='OPEN'
        if i.op==Opcode.ROAD_APPEND:
            rr=i.args[0]
            if ro.get(rr)!='OPEN': raise VerifyError(f'pc {pc}: road r{rr} not OPEN','VERIFY_ROAD_STATE')
            ro[rr]='MOVED'
        if i.op==Opcode.ROAD_CLOSE:
            rr=i.args[0]
            if ro.get(rr)!='OPEN': raise VerifyError(f'pc {pc}: road r{rr} not OPEN','VERIFY_ROAD_STATE')
            ro[rr]='CLOSED'
        if i.out is not None:
            d.add(i.out); ty[i.out]=i.result_type
            if i.result_type==TypeTag.QSTATE: q[i.out]=True
            if i.op==Opcode.ROAD_APPEND: ro[i.out]='OPEN'
        if i.op==Opcode.HALT:
            if any(s=='OPEN' for s in po.values()): raise VerifyError(f'pc {pc}: open portal on halting path','VERIFY_OPEN_PORTAL')
            if any(s=='OPEN' for s in ro.values()): raise VerifyError(f'pc {pc}: open road on halting path','VERIFY_OPEN_ROAD')
            halt_paths+=1; continue
        if i.op==Opcode.RETURN:
            if any(s=='OPEN' for s in po.values()): raise VerifyError('open portal at return','VERIFY_OPEN_PORTAL')
            if any(s=='OPEN' for s in ro.values()): raise VerifyError('open road at return','VERIFY_OPEN_ROAD')
            halt_paths+=1; continue
        if i.op in (Opcode.JUMP,Opcode.CALL):
            t=i.attrs.get('target')
            if not isinstance(t,int) or not 0<=t<n: raise VerifyError(f'pc {pc}: invalid target','VERIFY_TARGET')
            work.append((t,d,ty,q,po,ro)); continue
        if i.op==Opcode.BRANCH:
            for k in ('true','false'):
                t=i.attrs.get(k)
                if not isinstance(t,int) or not 0<=t<n: raise VerifyError(f'pc {pc}: invalid branch {k}','VERIFY_TARGET')
                work.append((t,set(d),dict(ty),dict(q),dict(po),dict(ro)))
            continue
        if pc+1<n: work.append((pc+1,d,ty,q,po,ro))
        else: halt_paths+=1
    if halt_paths==0: raise VerifyError('no halting path','VERIFY_NO_HALT')
    for r in program.exports:
        if not 0<=r<256: raise VerifyError('bad export register','VERIFY_EXPORT')
    return {'ok':True,'reachable_states':len(seen),'halting_paths':halt_paths,'max_register':maxreg,'instructions':n,'exports':list(program.exports),'verifier':'CFG_PATH_V0_1'}
