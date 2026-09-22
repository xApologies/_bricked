from __future__ import annotations
import json,hashlib
from .model import *
from .util import canonical_json
from .errors import VerifyError
MAGIC=b'GREC15\x00'

def _obj(p):
    return {'module':p.module,'version':p.version,'instructions':[{'op':int(i.op),'out':i.out,'args':list(i.args),'attrs':i.attrs,'result_type':i.result_type,'source':i.source} for i in p.instructions],'functions':{k:v.as_dict() for k,v in p.functions.items()},'main_start':p.main_start,'exports':p.exports,'metadata':p.metadata}
def encode(p):
    payload=canonical_json(_obj(p)).encode(); return MAGIC+len(payload).to_bytes(8,'big')+payload+hashlib.sha256(payload).digest()
def decode(data):
    if not data.startswith(MAGIC): raise VerifyError('bad recursion bytecode magic','BYTECODE_MAGIC')
    n=int.from_bytes(data[len(MAGIC):len(MAGIC)+8],'big'); a=len(MAGIC)+8; payload=data[a:a+n]; digest=data[a+n:a+n+32]
    if len(payload)!=n or len(digest)!=32 or hashlib.sha256(payload).digest()!=digest: raise VerifyError('recursion bytecode digest mismatch','BYTECODE_DIGEST')
    o=json.loads(payload); ins=[Instruction(Op(x['op']),x['out'],tuple(x['args']),x['attrs'],x['result_type'],x.get('source')) for x in o['instructions']]
    fs={k:FunctionInfo(**v) for k,v in o['functions'].items()}
    p=RecursiveProgram(o['module'],o['version'],ins,fs,o['main_start'],o['exports'],o['metadata'])
    from .verifier import verify; verify(p); return p
