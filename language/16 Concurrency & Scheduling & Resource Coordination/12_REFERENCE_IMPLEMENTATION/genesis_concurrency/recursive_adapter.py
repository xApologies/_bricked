from __future__ import annotations
from .util import sha256_obj
from .errors import ConcurrencyError

def make_token(task_id:str,state:int=0,delta:int=1,close_at:int|None=None,total_steps:int=0,history_root:str|None=None):
    body={'task_id':task_id,'state':int(state),'delta':int(delta),'close_at':None if close_at is None else int(close_at),'total_steps':int(total_steps),'history_root':history_root or '0'*64}
    token=dict(body); token['digest']=sha256_obj(body); return token

def validate_token(token:dict):
    keys=('task_id','state','delta','close_at','total_steps','history_root')
    try: body={k:token[k] for k in keys}
    except KeyError as e: raise ConcurrencyError(f'missing recursion continuation field {e.args[0]}','RECURSION_CONTINUATION_INVALID')
    if token.get('digest')!=sha256_obj(body): raise ConcurrencyError('recursion continuation digest mismatch','RECURSION_CONTINUATION_INVALID')
    return body

def run_slice(token:dict,budget:int):
    body=validate_token(token); budget=int(budget)
    if not 1<=budget<=1_000_000: raise ConcurrencyError('slice budget out of range','RECURSION_SLICE_BUDGET')
    state=int(body['state']); delta=int(body['delta']); close_at=body['close_at']; total=int(body['total_steps']); hist=body['history_root']
    def closed():
        if close_at is None:return False
        return state>=close_at if delta>=0 else state<=close_at
    used=0
    for _ in range(budget):
        if closed(): break
        state+=delta; total+=1; used+=1; hist=sha256_obj({'history':hist,'task':body['task_id'],'step':total,'state':state})
    if closed():
        receipt={'task_id':body['task_id'],'status':'CLOSED','state':state,'total_steps':total,'history_root':hist}; receipt['receipt_id']='gpersist-'+sha256_obj(receipt)[:32]
        return {'status':'CLOSED','state':state,'steps_used':used,'continuation':None,'receipt':receipt}
    nxt=make_token(body['task_id'],state,delta,close_at,total,hist)
    return {'status':'SUSPENDED','state':state,'steps_used':used,'continuation':nxt,'receipt':None}
