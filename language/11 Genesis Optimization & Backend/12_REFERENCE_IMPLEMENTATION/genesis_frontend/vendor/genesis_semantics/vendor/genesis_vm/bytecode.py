import struct, hashlib, json
from .model import Program, Instruction, Opcode, TypeTag
from .util import canonical_bytes
from .errors import BytecodeError

MAGIC=b'GVM1'; MAJOR=0; MINOR=1
HEADER=struct.Struct('>4sHHII32s')
REC=struct.Struct('>HHHHI')

def _metadata(program):
    return {
        'name':program.name,'version':program.version,'exports':program.exports,
        'metadata':program.metadata,
    }

def _payload(i):
    return {'args':list(i.args),'attrs':i.attrs,'source':i.source,'result_type':i.result_type.value}

def encode(program):
    meta=canonical_bytes(_metadata(program)); records=[]
    for i in program.instructions:
        pl=canonical_bytes(_payload(i)); out=0xFFFF if i.out is None else i.out
        records.append(REC.pack(int(i.op),out,len(i.args),0,len(pl))+pl)
    body=meta+b''.join(records); digest=hashlib.sha256(body).digest()
    return HEADER.pack(MAGIC,MAJOR,MINOR,len(program.instructions),len(meta),digest)+body

def decode(data):
    if len(data)<HEADER.size: raise BytecodeError('truncated header')
    magic,maj,minr,count,mlen,digest=HEADER.unpack(data[:HEADER.size])
    if magic!=MAGIC: raise BytecodeError('bad magic')
    if (maj,minr)!=(MAJOR,MINOR): raise BytecodeError('unsupported version')
    body=data[HEADER.size:]
    if hashlib.sha256(body).digest()!=digest: raise BytecodeError('digest mismatch')
    if len(body)<mlen: raise BytecodeError('truncated metadata')
    md=json.loads(body[:mlen]); pos=mlen; ins=[]
    for _ in range(count):
        if pos+REC.size>len(body): raise BytecodeError('truncated record')
        op,out,argc,flags,plen=REC.unpack(body[pos:pos+REC.size]); pos+=REC.size
        if pos+plen>len(body): raise BytecodeError('truncated payload')
        p=json.loads(body[pos:pos+plen]); pos+=plen
        args=tuple(p.get('args',[]))
        if len(args)!=argc: raise BytecodeError('argc mismatch')
        try: opcode=Opcode(op)
        except ValueError: raise BytecodeError(f'unknown opcode {op}')
        ins.append(Instruction(opcode,None if out==0xFFFF else out,args,p.get('attrs',{}),p.get('source'),TypeTag(p.get('result_type','ANY'))))
    if pos!=len(body): raise BytecodeError('trailing bytes')
    return Program(md['name'],md.get('version','0.1.0'),ins,list(md.get('exports',[])),dict(md.get('metadata',{})))
