from __future__ import annotations
from .model import *
from .verifier import verify
from .util import sha256_obj
from .errors import RuntimeFault
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm.backend import ReferenceBackend

class VM:
    def __init__(self,backend=None): self.backend=backend or ReferenceBackend()
    def run(self,program,max_steps=100000):
        vr=verify(program); regs={}; pc=0; steps=0; stack=[]; halted=False; open_portals=set(); open_roads=set()
        def get(r):
            if r not in regs: raise RuntimeFault(f'uninitialized r{r}','RUNTIME_USE')
            return regs[r]
        def val(r): return get(r).value
        while 0<=pc<len(program.instructions):
            if steps>=max_steps: raise RuntimeFault('step limit','RUNTIME_STEP_LIMIT')
            i=program.instructions[pc]; steps+=1; adv=True; out=None; typ=i.result_type; a=i.attrs
            if i.op==Opcode.NOP: pass
            elif i.op==Opcode.CONST: out=a.get('value')
            elif i.op==Opcode.MOVE: out=val(i.args[0]); typ=get(i.args[0]).type
            elif i.op==Opcode.HASH: out=sha256_obj(val(i.args[0])); typ=TypeTag.HASH
            elif i.op==Opcode.DATA_RECORD: out={'__kind__':'RECORD','type':a['record_type'],'fields':{f:val(r) for f,r in zip(a['fields'],i.args)}}
            elif i.op==Opcode.DATA_FIELD: out=val(i.args[0])['fields'][a['field']]
            elif i.op==Opcode.DATA_VARIANT: out={'__kind__':'VARIANT','type':a['variant_type'],'tag':a['tag'],'payload':val(i.args[0]) if i.args else None}
            elif i.op==Opcode.DATA_IS: out=val(i.args[0]).get('tag')==a['tag']; typ=TypeTag.BOOL
            elif i.op==Opcode.DATA_PAYLOAD:
                v=val(i.args[0])
                if a.get('expected_tag') and v.get('tag')!=a['expected_tag']: raise RuntimeFault('variant tag mismatch','RUNTIME_MATCH')
                out=v.get('payload')
            elif i.op==Opcode.DATA_EQ: out=val(i.args[0])==val(i.args[1]); typ=TypeTag.BOOL
            elif i.op==Opcode.BOOL_NOT: out=not bool(val(i.args[0])); typ=TypeTag.BOOL
            elif i.op==Opcode.BOOL_AND: out=bool(val(i.args[0])) and bool(val(i.args[1])); typ=TypeTag.BOOL
            elif i.op==Opcode.BOOL_OR: out=bool(val(i.args[0])) or bool(val(i.args[1])); typ=TypeTag.BOOL
            elif i.op==Opcode.INT_ADD: out=int(val(i.args[0]))+int(val(i.args[1])); typ=TypeTag.INT
            elif i.op==Opcode.INT_SUB: out=int(val(i.args[0]))-int(val(i.args[1])); typ=TypeTag.INT
            elif i.op==Opcode.INT_LT: out=int(val(i.args[0]))<int(val(i.args[1])); typ=TypeTag.BOOL
            elif i.op==Opcode.INT_LE: out=int(val(i.args[0]))<=int(val(i.args[1])); typ=TypeTag.BOOL
            elif i.op==Opcode.FABRIC_MOUNT: out=self.backend.mount_fabric(a.get('uri','fabric://reference'))
            elif i.op==Opcode.FABRIC_ALLOC: out=self.backend.alloc(val(i.args[0]),a.get('cells',1))
            elif i.op==Opcode.FABRIC_READ: out=self.backend.read_fabric(val(i.args[0]),a.get('addr','0'))
            elif i.op==Opcode.FABRIC_WRITE_OVERLAY: out=self.backend.write_overlay(val(i.args[0]),a.get('addr','0'),a.get('value'))
            elif i.op==Opcode.GEO_INSTANTIATE: out=self.backend.instantiate(val(i.args[0]),val(i.args[1]),a.get('mmo',{'handle':'@anonymous'}))
            elif i.op==Opcode.GEO_FORK: out=self.backend.fork(val(i.args[0]),a)
            elif i.op==Opcode.RELATE: out=self.backend.relate(val(i.args[0]),a.get('target','environment'),a)
            elif i.op==Opcode.ADMIT: out=self.backend.admit(val(i.args[0]),a)
            elif i.op==Opcode.TRANSFORM: out=self.backend.transform(val(i.args[0]),val(i.args[1]),a)
            elif i.op==Opcode.INHERIT: out=self.backend.inherit(val(i.args[0]),a)
            elif i.op==Opcode.PORTAL_OPEN:
                out=self.backend.portal_open(val(i.args[0]),val(i.args[1]),a.get('sector','GENERIC'),a); open_portals.add(out['resource_id'])
            elif i.op==Opcode.PORTAL_TRANSPORT: out=self.backend.portal_transport(val(i.args[0]),val(i.args[1]),a)
            elif i.op==Opcode.PORTAL_CLOSE:
                p=val(i.args[0]); out=self.backend.portal_close(p,val(i.args[1])); open_portals.discard(p['resource_id'])
            elif i.op==Opcode.ROAD_BEGIN:
                out=self.backend.road_begin(val(i.args[0]),a); open_roads.add(out['resource_id'])
            elif i.op==Opcode.ROAD_APPEND:
                old=val(i.args[0]); out=self.backend.road_append(old,val(i.args[1])); open_roads.discard(old['resource_id']); open_roads.add(out['resource_id'])
            elif i.op==Opcode.ROAD_CLOSE:
                road=val(i.args[0]); out=self.backend.road_close(road,val(i.args[1])); open_roads.discard(road['resource_id'])
            elif i.op==Opcode.BRIDGE_SECTOR: out=self.backend.bridge(val(i.args[0]),a.get('from'),a.get('to'),a)
            elif i.op==Opcode.Q_PREPARE: out=self.backend.q_prepare(val(i.args[0]),a)
            elif i.op==Opcode.Q_SUPERPOSE: out=self.backend.q_successor('SUPERPOSE',[val(i.args[0])],a)
            elif i.op==Opcode.Q_ENTANGLE: out=self.backend.q_successor('ENTANGLE',[val(i.args[0]),val(i.args[1])],a)
            elif i.op==Opcode.Q_CHANNEL: out=self.backend.q_successor('CHANNEL',[val(i.args[0])],a)
            elif i.op==Opcode.Q_MEASURE: out=self.backend.q_measure(val(i.args[0]),a)
            elif i.op==Opcode.BRANE_LIFT: out=self.backend.brane_lift(val(i.args[0]),a)
            elif i.op==Opcode.PROVENANCE_SEAL: out=self.backend.provenance_seal(val(i.args[0]),a)
            elif i.op==Opcode.ASSERT_CLOSURE: out=self.backend.assert_closure(val(i.args[0])); typ=TypeTag.BOOL
            elif i.op==Opcode.EMIT_RECEIPT: out=self.backend.execution_receipt({'program':program.name,'pc':pc,'control':True})
            elif i.op==Opcode.JUMP: pc=a['target']; adv=False
            elif i.op==Opcode.BRANCH: pc=a['true'] if bool(val(i.args[0])) else a['false']; adv=False
            elif i.op==Opcode.CALL: stack.append(pc+1); pc=a['target']; adv=False
            elif i.op==Opcode.RETURN:
                if not stack: halted=True; break
                pc=stack.pop(); adv=False
            elif i.op==Opcode.HALT: halted=True; break
            else: raise RuntimeFault(f'unimplemented {i.op}','RUNTIME_OPCODE')
            if i.out is not None: regs[i.out]=TaggedValue(typ,out)
            if adv: pc+=1
        if open_portals: raise RuntimeFault('open portals at runtime halt','RUNTIME_OPEN_PORTAL')
        if open_roads: raise RuntimeFault('open roads at runtime halt','RUNTIME_OPEN_ROAD')
        ex={r:regs[r] for r in program.exports if r in regs}
        receipt=self.backend.execution_receipt({'program':program.name,'version':program.version,'steps':steps,'verified':vr['ok'],'exports':{str(r):sha256_obj(regs[r].value) for r in ex},'control_paths':vr['halting_paths']})
        return ExecutionResult(halted or pc>=len(program.instructions),regs,ex,receipt)
