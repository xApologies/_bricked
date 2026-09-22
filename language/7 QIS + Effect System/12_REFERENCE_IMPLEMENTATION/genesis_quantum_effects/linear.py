from .model import OwnershipRecord,OwnershipState,StateKind
from .util import digest,now_ns
from .errors import OwnershipError,NoCloningError,ConsumedStateError

class LinearOwnershipRegistry:
    def __init__(self): self.records={}; self.receipts=[]
    def claim(self,state,owner):
        if state.state_id in self.records and self.records[state.state_id].status==OwnershipState.OWNED.value: raise OwnershipError('already owned')
        tok=digest({'state_id':state.state_id,'owner':owner,'nonce':len(self.records)})
        r=OwnershipRecord(state.state_id,tok,owner,OwnershipState.OWNED.value,0); self.records[state.state_id]=r
        self.receipts.append({'op':'CLAIM','state_id':state.state_id,'owner':owner,'token':tok,'timestamp_ns':now_ns()}); return r
    def assert_owned(self,state_id,token):
        r=self.records.get(state_id)
        if not r or r.status!=OwnershipState.OWNED.value or r.token!=token: raise ConsumedStateError('state not live-owned')
        return r
    def borrow_metadata(self,state_id,token):
        r=self.assert_owned(state_id,token); rec={'op':'BORROW_METADATA','state_id':state_id,'owner':r.owner,'timestamp_ns':now_ns()}; self.receipts.append(rec); return rec
    def move(self,state_id,token,new_owner):
        r=self.assert_owned(state_id,token); old=r.owner; r.owner=new_owner; r.version+=1; r.token=digest({'state_id':state_id,'owner':new_owner,'version':r.version}); rec={'op':'MOVE','state_id':state_id,'old_owner':old,'new_owner':new_owner,'token':r.token,'timestamp_ns':now_ns()}; self.receipts.append(rec); return r
    def clone(self,state,token):
        self.assert_owned(state.state_id,token)
        if state.kind!=StateKind.CLASSICAL.value: raise NoCloningError('live nonclassical state cannot be cloned')
        return {'classical_copy_of':state.state_id}
    def consume(self,state_id,token,reason='CONSUMED'):
        r=self.assert_owned(state_id,token); r.status=OwnershipState.CONSUMED.value; r.version+=1; rec={'op':'CONSUME','state_id':state_id,'reason':reason,'timestamp_ns':now_ns()}; self.receipts.append(rec); return rec
