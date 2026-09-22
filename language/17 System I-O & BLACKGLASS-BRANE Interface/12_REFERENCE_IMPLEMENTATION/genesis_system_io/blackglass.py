from __future__ import annotations
from typing import Any
from .errors import fail
from .util import digest_obj, canonical_json
from .storage import CASStore

class BlackglassHeartReference:
    def __init__(self,cas:CASStore):
        self.cas=cas; self.proposals:dict[str,dict[str,Any]]={}; self.durable:dict[str,dict[str,Any]]={}; self.sequence=0
    def direct_write(self,*_args,**_kwargs): fail("BLACKGLASS_DIRECT_WRITE_FORBIDDEN")
    def propose(self,payload:Any,provenance_root:str)->dict[str,Any]:
        self.sequence+=1
        if isinstance(payload,bytes): blob=payload
        elif isinstance(payload,str): blob=payload.encode("utf-8")
        else: blob=canonical_json(payload)
        payload_ref=self.cas.put(blob)
        base={"sequence":self.sequence,"payload_ref":payload_ref,"provenance_root":provenance_root,"status":"STAGED"}
        proposal_id="proposal:"+digest_obj(base)
        proposal={**base,"proposal_id":proposal_id}
        self.proposals[proposal_id]=proposal
        return proposal
    def admit(self,proposal_id:str,authority:bool)->dict[str,Any]:
        if not authority: fail("BLACKGLASS_ADMISSION_AUTHORITY")
        if proposal_id not in self.proposals: fail("BLACKGLASS_PROPOSAL_UNKNOWN",proposal_id)
        p=self.proposals[proposal_id]
        durable_id="heart:"+digest_obj({"proposal":proposal_id,"payload_ref":p["payload_ref"]})
        rec={"durable_id":durable_id,"proposal_id":proposal_id,"payload_ref":p["payload_ref"],"status":"COMMITTED"}
        self.durable[durable_id]=rec
        return rec
