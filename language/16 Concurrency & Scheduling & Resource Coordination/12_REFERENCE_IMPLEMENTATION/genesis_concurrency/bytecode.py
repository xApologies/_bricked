from __future__ import annotations
import struct,json,hashlib
from .model import *
from .util import canonical_json
from .verifier import verify
from .errors import ConcurrencyError
MAGIC=b'GCON16\0\0'; VERSION=1

def to_obj(p):
    return {'module':p.module,'version':p.version,'resources':{k:v.as_dict() for k,v in sorted(p.resources.items())},'templates':{k:v.as_dict() for k,v in sorted(p.templates.items())},'spawns':[x.__dict__ for x in p.spawns],'joins':p.joins,'metadata':p.metadata}
def from_obj(o):
    rs={k:ResourceSpec(**v) for k,v in o['resources'].items()};ts={}
    for k,v in o['templates'].items():
        ops=[TaskOp(Op(x['op']),x.get('attrs',{}),x.get('source')) for x in v['ops']]
        ts[k]=TaskTemplate(v['name'],v['priority'],v['quantum'],ops,v.get('kind','STANDARD'),v.get('recursion'))
    p=ConcurrentProgram(o['module'],o['version'],rs,ts,[SpawnSpec(**x) for x in o['spawns']],list(o['joins']),dict(o.get('metadata',{})));verify(p);return p
def encode(p):
    verify(p);body=canonical_json(to_obj(p));dig=hashlib.sha256(body).digest();return MAGIC+struct.pack('>II',VERSION,len(body))+dig+body
def decode(data):
    if len(data)<48 or data[:8]!=MAGIC:raise ConcurrencyError('bad GCON bytecode header','CONCURRENCY_BYTECODE')
    ver,n=struct.unpack('>II',data[8:16]);
    if ver!=VERSION:raise ConcurrencyError('unsupported GCON bytecode version','CONCURRENCY_BYTECODE')
    dig=data[16:48];body=data[48:48+n]
    if len(body)!=n or hashlib.sha256(body).digest()!=dig:raise ConcurrencyError('GCON bytecode digest mismatch','CONCURRENCY_BYTECODE_TAMPER')
    return from_obj(json.loads(body))
