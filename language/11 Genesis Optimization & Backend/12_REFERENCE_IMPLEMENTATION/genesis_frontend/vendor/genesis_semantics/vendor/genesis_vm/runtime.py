from __future__ import annotations
from .model import Opcode, TypeTag, TaggedValue, ExecutionResult
from .verifier import verify
from .backend import ReferenceBackend
from .util import sha256_obj
from .errors import RuntimeFault, ClosureError

class VM:
    def __init__(self, backend=None): self.backend=backend or ReferenceBackend()
    def run(self, program, max_steps=100000):
        vr=verify(program)
        regs={}; pc=0; steps=0; stack=[]; halted=False; open_portals=set(); open_roads=set()
        def get(r):
            if r not in regs: raise RuntimeFault(f'uninitialized r{r}')
            return regs[r]
        def resource(r): return get(r).value
        while pc < len(program.instructions):
            if steps>=max_steps: raise RuntimeFault('step limit')
            i=program.instructions[pc]; steps+=1; advance=True; out=None; typ=i.result_type
            lit=i.attrs.get('_literal_args',[])
            if i.op==Opcode.NOP: pass
            elif i.op==Opcode.CONST:
                out=i.attrs.get('value', lit[0] if lit else None)
            elif i.op==Opcode.MOVE:
                v=get(i.args[0]); out=v.value; typ=v.type
                if v.type==TypeTag.QSTATE: raise RuntimeFault('QSTATE cannot use generic MOVE')
            elif i.op==Opcode.HASH: out=sha256_obj(get(i.args[0]).value); typ=TypeTag.HASH
            elif i.op==Opcode.FABRIC_MOUNT: out=self.backend.mount_fabric(i.attrs.get('uri','fabric://reference'))
            elif i.op==Opcode.FABRIC_ALLOC:
                cells=i.attrs.get('cells',lit[0] if lit else 1); out=self.backend.alloc(resource(i.args[0]),cells)
            elif i.op==Opcode.FABRIC_READ:
                addr=i.attrs.get('addr',lit[0] if lit else '0'); out=self.backend.read_fabric(resource(i.args[0]),addr)
            elif i.op==Opcode.FABRIC_WRITE_OVERLAY:
                addr=i.attrs.get('addr',lit[0] if lit else '0'); value=i.attrs.get('value',lit[1] if len(lit)>1 else None); out=self.backend.write_overlay(resource(i.args[0]),addr,value)
            elif i.op==Opcode.GEO_INSTANTIATE:
                mmo=i.attrs.get('mmo',lit[0] if lit else {'handle':'@anonymous'}); out=self.backend.instantiate(resource(i.args[0]),resource(i.args[1]),mmo)
            elif i.op==Opcode.GEO_FORK: out=self.backend.fork(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.RELATE:
                target=resource(i.args[1]) if len(i.args)>1 else i.attrs.get('target',lit[0] if lit else 'environment'); out=self.backend.relate(resource(i.args[0]),target,i.attrs)
            elif i.op==Opcode.ADMIT: out=self.backend.admit(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.TRANSFORM: out=self.backend.transform(resource(i.args[0]),resource(i.args[1]),i.attrs)
            elif i.op==Opcode.INHERIT: out=self.backend.inherit(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.PORTAL_OPEN:
                sector=i.attrs.get('sector',lit[0] if lit else 'GENERIC'); out=self.backend.portal_open(resource(i.args[0]),resource(i.args[1]),sector,i.attrs); open_portals.add(out['resource_id'])
            elif i.op==Opcode.PORTAL_TRANSPORT: out=self.backend.portal_transport(resource(i.args[0]),resource(i.args[1]),i.attrs)
            elif i.op==Opcode.PORTAL_CLOSE:
                p=resource(i.args[0]); out=self.backend.portal_close(p,resource(i.args[1])); open_portals.discard(p['resource_id'])
            elif i.op==Opcode.ROAD_BEGIN:
                out=self.backend.road_begin(resource(i.args[0]),i.attrs); open_roads.add(out['resource_id'])
            elif i.op==Opcode.ROAD_APPEND:
                old=resource(i.args[0]); out=self.backend.road_append(old,resource(i.args[1])); open_roads.discard(old['resource_id']); open_roads.add(out['resource_id'])
            elif i.op==Opcode.ROAD_CLOSE:
                road=resource(i.args[0]); out=self.backend.road_close(road,resource(i.args[1])); open_roads.discard(road['resource_id'])
            elif i.op==Opcode.BRIDGE_SECTOR:
                fs=i.attrs.get('from'); ts=i.attrs.get('to'); out=self.backend.bridge(resource(i.args[0]),fs,ts,i.attrs)
            elif i.op==Opcode.Q_PREPARE: out=self.backend.q_prepare(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.Q_SUPERPOSE: out=self.backend.q_successor('SUPERPOSE',[resource(i.args[0])],i.attrs)
            elif i.op==Opcode.Q_ENTANGLE: out=self.backend.q_successor('ENTANGLE',[resource(i.args[0]),resource(i.args[1])],i.attrs)
            elif i.op==Opcode.Q_CHANNEL: out=self.backend.q_successor('CHANNEL',[resource(i.args[0])],i.attrs)
            elif i.op==Opcode.Q_MEASURE: out=self.backend.q_measure(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.BRANE_LIFT: out=self.backend.brane_lift(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.PROVENANCE_SEAL: out=self.backend.provenance_seal(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.ASSERT_CLOSURE:
                out=self.backend.assert_closure(resource(i.args[0])); typ=TypeTag.BOOL
                if not out and i.attrs.get('required',True): raise ClosureError('closure assertion failed')
            elif i.op==Opcode.EMIT_RECEIPT:
                payload={'program':program.name,'pc':pc,'ledger_root':sha256_obj([x['resource_id'] for x in self.backend.ledger])}; out=self.backend.execution_receipt(payload)
            elif i.op==Opcode.JUMP: pc=i.attrs['target']; advance=False
            elif i.op==Opcode.BRANCH:
                cond=bool(get(i.args[0]).value); pc=i.attrs['true'] if cond else i.attrs['false']; advance=False
            elif i.op==Opcode.CALL: stack.append(pc+1); pc=i.attrs['target']; advance=False
            elif i.op==Opcode.RETURN:
                if not stack: halted=True; break
                pc=stack.pop(); advance=False
            elif i.op==Opcode.HALT: halted=True; break
            else: raise RuntimeFault(f'unimplemented {i.op.name}')
            if i.out is not None: regs[i.out]=TaggedValue(typ,out)
            if advance: pc+=1
        if open_portals: raise ClosureError(f'open portal resources at halt: {sorted(open_portals)}')
        if open_roads: raise ClosureError(f'open road resources at halt: {sorted(open_roads)}')
        exports={r:regs[r] for r in program.exports}
        receipt=self.backend.execution_receipt({
            'program':program.name,'version':program.version,'steps':steps,'verified':vr['ok'],
            'exports':{str(r):sha256_obj(regs[r].value) for r in program.exports},
            'ledger_root':sha256_obj([x['resource_id'] for x in self.backend.ledger]),
            'open_portals':0,'open_roads':0,
        })
        return ExecutionResult(halted=halted or pc>=len(program.instructions),registers=regs,exports=exports,receipt=receipt)
