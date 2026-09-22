from __future__ import annotations
from .parser import parse_source
from .verifier import verify
from .util import digest_obj

def compile_source(text:str,source:str="<memory>"):
    p=parse_source(text,source)
    proof=verify(p)
    p.metadata["verification"]=proof
    p.metadata["program_id"]="sysprog:"+digest_obj({"module":p.module,"version":p.version,"caps":sorted(p.capabilities),"endpoints":{k:v.as_dict() for k,v in sorted(p.endpoints.items())},"ports":{k:v.as_dict() for k,v in sorted(p.ports.items())},"instructions":[i.as_dict() for i in p.instructions]})
    return p
