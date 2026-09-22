from __future__ import annotations
from .model import BoundaryReceipt
from .util import digest_obj,object_ref,canonical_json

def make_receipt(sequence:int,op:str,target:str,status:str,input_value=None,output_value=None,prev_root:str="0"*64,detail=None):
    def ref(v):
        if v is None: return None
        if isinstance(v,str) and v.startswith("sha256:"): return v
        if isinstance(v,bytes): return object_ref(v)
        return "sha256:"+digest_obj(v)
    body={"sequence":sequence,"operation":op,"target":target,"status":status,"input_ref":ref(input_value),"output_ref":ref(output_value),"previous":prev_root,"detail":detail or {}}
    request_id="sysreq:"+digest_obj(body)
    provenance_root=digest_obj({**body,"request_id":request_id})
    return BoundaryReceipt(sequence,request_id,op,target,status,body["input_ref"],body["output_ref"],provenance_root,detail or {})
