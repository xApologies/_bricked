import struct,hashlib,json
from .model import *
from .util import canonical_bytes
from .errors import BytecodeError
MAGIC=b'GVC2'; MAJOR=0; MINOR=2
HEADER=struct.Struct('>4sHHII32s'); REC=struct.Struct('>HHHHI')
def encode(program):
    meta=canonical_bytes({'name':program.name,'version':program.version,'exports':program.exports,'metadata':program.metadata}); rec=[]
    for i in program.instructions:
        pl=canonical_bytes({'args':list(i.args),'attrs':i.attrs,'source':i.source,'result_type':i.result_type.value}); out=0xFFFF if i.out is None else i.out
        rec.append(REC.pack(int(i.op),out,len(i.args),0,len(pl))+pl)
    body=meta+b''.join(rec); return HEADER.pack(MAGIC,MAJOR,MINOR,len(program.instructions),len(meta),hashlib.sha256(body).digest())+body
def decode(data):
    if len(data)<HEADER.size: raise BytecodeError('truncated header','BYTECODE')
    magic,maj,minr,count,mlen,digest=HEADER.unpack(data[:HEADER.size]); body=data[HEADER.size:]
    if magic!=MAGIC or (maj,minr)!=(MAJOR,MINOR): raise BytecodeError('unsupported bytecode','BYTECODE')
    if hashlib.sha256(body).digest()!=digest: raise BytecodeError('digest mismatch','BYTECODE')
    md=json.loads(body[:mlen]); pos=mlen; ins=[]
    for _ in range(count):
        if pos+REC.size>len(body): raise BytecodeError('truncated record','BYTECODE')
        op,out,argc,flags,plen=REC.unpack(body[pos:pos+REC.size]); pos+=REC.size
        p=json.loads(body[pos:pos+plen]); pos+=plen; args=tuple(p.get('args',[]))
        if len(args)!=argc: raise BytecodeError('argc mismatch','BYTECODE')
        ins.append(Instruction(Opcode(op),None if out==0xFFFF else out,args,p.get('attrs',{}),p.get('source'),TypeTag(p.get('result_type','ANY'))))
    if pos!=len(body): raise BytecodeError('trailing bytes','BYTECODE')
    return Program(md['name'],md.get('version','0.2.0'),ins,list(md.get('exports',[])),dict(md.get('metadata',{})))
