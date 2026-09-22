from __future__ import annotations
from .parser import parse_source
from .verifier import verify
from .util import sha256_obj

def compile_source(text:str,file='<memory>'):
    p=parse_source(text,file); v=verify(p); p.metadata['verification']=v
    stable={'module':p.module,'version':p.version,'resources':{k:x.as_dict() for k,x in sorted(p.resources.items())},'templates':{k:x.as_dict() for k,x in sorted(p.templates.items())},'spawns':[x.__dict__ for x in p.spawns],'joins':p.joins}
    p.metadata['program_id']='gcon-'+sha256_obj(stable)[:32]
    return p
