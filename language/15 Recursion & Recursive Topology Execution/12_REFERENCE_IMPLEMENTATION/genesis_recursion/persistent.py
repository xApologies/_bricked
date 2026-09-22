from __future__ import annotations
from dataclasses import dataclass
from .util import sha256_obj
from .errors import RuntimeFault

@dataclass
class PersistentResult:
    status:str; state:int; total_steps:int; history_root:str; continuation:dict|None; receipt:dict|None

class PersistentRecursiveTask:
    def __init__(self,task_id,state=0,delta=1,close_at=None,history_root=None,total_steps=0):
        self.task_id=task_id; self.state=int(state); self.delta=int(delta); self.close_at=None if close_at is None else int(close_at)
        self.history_root=history_root or '0'*64; self.total_steps=int(total_steps)
    def _closed(self):
        if self.close_at is None:return False
        return self.state>=self.close_at if self.delta>=0 else self.state<=self.close_at
    def run_slice(self,budget):
        if not 1<=int(budget)<=1_000_000: raise ValueError('slice budget out of range')
        for _ in range(int(budget)):
            if self._closed(): break
            self.state+=self.delta; self.total_steps+=1; self.history_root=sha256_obj({'history':self.history_root,'task':self.task_id,'step':self.total_steps,'state':self.state})
        if self._closed():
            receipt={'task_id':self.task_id,'status':'CLOSED','state':self.state,'total_steps':self.total_steps,'history_root':self.history_root}; receipt['receipt_id']='gpersist-'+sha256_obj(receipt)[:32]
            return PersistentResult('CLOSED',self.state,self.total_steps,self.history_root,None,receipt)
        body={'task_id':self.task_id,'state':self.state,'delta':self.delta,'close_at':self.close_at,'total_steps':self.total_steps,'history_root':self.history_root}
        token=dict(body); token['digest']=sha256_obj(body)
        return PersistentResult('SUSPENDED',self.state,self.total_steps,self.history_root,token,None)
    @classmethod
    def resume(cls,token):
        body={k:token[k] for k in ('task_id','state','delta','close_at','total_steps','history_root')}
        if token.get('digest')!=sha256_obj(body): raise RuntimeFault('persistent recursion continuation failed integrity check','RECURSION_CONTINUATION_INVALID')
        return cls(**body)
