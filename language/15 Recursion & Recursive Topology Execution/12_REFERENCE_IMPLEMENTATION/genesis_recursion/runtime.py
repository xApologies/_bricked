from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any
from .model import *
from .util import sha256_obj
from .errors import RuntimeFault

@dataclass
class _Frame:
    function:str; pc:int; regs:dict[int,Any]=field(default_factory=dict); return_pc:int|None=None; return_dest:int|None=None
    depth:int=0; fuel_remaining:int|None=None; visit_history:tuple[Any,...]=(); closed:bool=False; history_root:str='0'*64
    parent_frame_id:str|None=None; frame_id:str=''

class LinearFrameLedger:
    def __init__(self): self.resources={}
    def open(self,kind,resource_id): self.resources[resource_id]=kind.upper()
    def close(self,resource_id): self.resources.pop(resource_id,None)
    def assert_boundary_safe(self):
        if self.resources: raise RuntimeFault(f'linear resources cross recursion/yield boundary: {sorted(self.resources.items())}','RECURSION_LINEAR_RESOURCE_CAPTURE')
        return True

class RecursiveVM:
    def __init__(self,max_steps=1_000_000): self.max_steps=max_steps
    def run(self,program):
        from .verifier import verify
        vr=verify(program); steps=0; frames_log=[]; frame_serial=0
        root=_Frame('__main__',program.main_start,depth=0,frame_id='frame-main')
        stack=[root]
        while stack:
            if steps>=self.max_steps: raise RuntimeFault('recursive execution step budget exhausted','RECURSION_STEP_BUDGET')
            fr=stack[-1]
            if not 0<=fr.pc<len(program.instructions): raise RuntimeFault('pc out of range','RECURSION_PC')
            ins=program.instructions[fr.pc]; steps+=1
            def v(r):
                if r not in fr.regs: raise RuntimeFault(f'use of undefined r{r}','RECURSION_REGISTER')
                return fr.regs[r]
            out=None; adv=True
            if ins.op==Op.CONST: out=ins.attrs.get('value')
            elif ins.op==Op.MOVE: out=v(ins.args[0])
            elif ins.op==Op.INT_ADD: out=int(v(ins.args[0]))+int(v(ins.args[1]))
            elif ins.op==Op.INT_SUB: out=int(v(ins.args[0]))-int(v(ins.args[1]))
            elif ins.op==Op.INT_LT: out=int(v(ins.args[0]))<int(v(ins.args[1]))
            elif ins.op==Op.INT_LE: out=int(v(ins.args[0]))<=int(v(ins.args[1]))
            elif ins.op==Op.DATA_EQ: out=v(ins.args[0])==v(ins.args[1])
            elif ins.op==Op.BOOL_NOT: out=not bool(v(ins.args[0]))
            elif ins.op==Op.BOOL_AND: out=bool(v(ins.args[0])) and bool(v(ins.args[1]))
            elif ins.op==Op.BOOL_OR: out=bool(v(ins.args[0])) or bool(v(ins.args[1]))
            elif ins.op==Op.BRANCH: fr.pc=ins.attrs['true'] if bool(v(ins.args[0])) else ins.attrs['false']; adv=False
            elif ins.op==Op.JUMP: fr.pc=ins.attrs['target']; adv=False
            elif ins.op==Op.RCALL:
                name=ins.attrs['function']; fn=program.functions[name]; args=[v(r) for r in ins.args]
                depth=fr.depth+1
                maxd=fn.max_depth or 4096
                if depth>maxd: raise RuntimeFault(f'{name}: maximum recursion depth exceeded','RECURSION_DEPTH_EXCEEDED')
                fuel=fn.fuel; visits=()
                if fr.function==name and ins.attrs.get('recursive'):
                    if fn.mode=='DECREASING':
                        mi=next(i for i,p in enumerate(fn.params) if p[0]==fn.metric_param); old=fr.regs.get(mi); new=args[mi]
                        if not (isinstance(old,int) and isinstance(new,int) and new<old): raise RuntimeFault(f'{name}: runtime metric failed to decrease','RECURSION_NOT_DECREASING')
                    elif fn.mode=='FUEL':
                        oldfuel=fr.fuel_remaining if fr.fuel_remaining is not None else fn.fuel
                        if oldfuel is None or oldfuel<=0: raise RuntimeFault(f'{name}: recursion fuel exhausted','RECURSION_FUEL_EXHAUSTED')
                        fuel=oldfuel-1
                    elif fn.mode=='VISIT_ONCE':
                        ki=next(i for i,p in enumerate(fn.params) if p[0]==fn.visit_key); key=args[ki]
                        visits=fr.visit_history
                        if key in visits: raise RuntimeFault(f'{name}: repeated visit key {key!r}','RECURSION_VISIT_REPEAT')
                        visits=visits+(key,)
                else:
                    if fn.mode=='VISIT_ONCE':
                        ki=next(i for i,p in enumerate(fn.params) if p[0]==fn.visit_key); visits=(args[ki],)
                frame_serial+=1; fid=f'frame-{frame_serial:08d}'
                child=_Frame(name,fn.start,{i:a for i,a in enumerate(args)},fr.pc+1,ins.out,depth,fuel,visits,False,fr.history_root,fr.frame_id,fid)
                stack.append(child); adv=False
            elif ins.op==Op.RECURSION_CLOSE:
                payload={'frame':fr.frame_id,'function':fr.function,'depth':fr.depth,'return_value_hash':sha256_obj(v(ins.args[0])),'history_before':fr.history_root}
                fr.history_root=sha256_obj(payload); fr.closed=True
            elif ins.op==Op.RRETURN:
                if not fr.closed: raise RuntimeFault('recursive return without closure','RECURSION_RETURN_UNCLOSED')
                rv=v(ins.args[0]); receipt={'frame_id':fr.frame_id,'parent_frame_id':fr.parent_frame_id,'function':fr.function,'depth':fr.depth,'history_root':fr.history_root,'return_hash':sha256_obj(rv),'closed':True}
                receipt['receipt_id']='rclose-'+sha256_obj(receipt)[:32]; frames_log.append(receipt)
                stack.pop()
                if not stack: raise RuntimeFault('recursive function returned without caller','RECURSION_STACK')
                parent=stack[-1]; parent.history_root=sha256_obj({'parent':parent.history_root,'child':receipt['receipt_id']}); parent.regs[fr.return_dest]=rv; parent.pc=fr.return_pc; adv=False
            elif ins.op==Op.HALT:
                if fr.function!='__main__': raise RuntimeFault('HALT inside recursive function','RECURSION_HALT_CONTEXT')
                exports={k:fr.regs[r] for k,r in program.exports.items() if r in fr.regs}
                receipt={'program_id':program.metadata.get('program_id'),'module':program.module,'steps':steps,'frames_closed':len(frames_log),'max_depth':max([x['depth'] for x in frames_log],default=0),'history_root':fr.history_root,'exports':{k:sha256_obj(v) for k,v in exports.items()},'verified':vr['ok'],'status':'HALTED'}
                receipt['receipt_id']='grec-run-'+sha256_obj(receipt)[:32]
                return RecursiveExecutionResult(True,exports,receipt,frames_log,steps)
            else: raise RuntimeFault(f'unimplemented recursion opcode {ins.op}','RECURSION_OPCODE')
            if ins.out is not None and ins.op!=Op.RCALL: fr.regs[ins.out]=out
            if adv: fr.pc+=1
        raise RuntimeFault('execution ended without HALT','RECURSION_NO_HALT')
