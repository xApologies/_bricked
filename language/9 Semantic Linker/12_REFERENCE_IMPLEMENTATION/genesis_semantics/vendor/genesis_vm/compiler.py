from .model import Program, Instruction, Opcode, TypeTag
from .isa import result_type
from .graph import schedule_gir
from .errors import GIRCompileError
from .util import sha256_obj


def _type(x):
    try: return TypeTag(x)
    except Exception: return TypeTag.ANY

def compile_gir(gir):
    if gir.get('ir')!='GIR': raise GIRCompileError('not GIR')
    scheduled=schedule_gir(gir)
    regs={}; nextreg=0; ins=[]
    for n in scheduled:
        opname=n['op']
        try: op=Opcode[opname]
        except KeyError: raise GIRCompileError(f'unknown op {opname}')
        args=[]
        attrs=dict(n.get('attrs',{}))
        literals=[]
        for a in n.get('args',[]):
            if isinstance(a,str) and a.startswith('%'):
                args.append(regs[a])
            else:
                literals.append(a)
        if literals:
            attrs['_literal_args']=literals
        outreg=None
        rt=_type(n.get('type',result_type(op).value))
        if n.get('out'):
            outreg=nextreg; regs[n['out']]=outreg; nextreg+=1
        ins.append(Instruction(op=op,out=outreg,args=tuple(args),attrs=attrs,source=n['id'],result_type=rt))
    exports=[]
    for x in gir.get('exports',[]):
        if x not in regs: raise GIRCompileError(f'unknown export {x}')
        exports.append(regs[x])
    normalized_gir=dict(gir)
    normalized_gir['nodes']=sorted(gir.get('nodes',[]), key=lambda n:n.get('id',''))
    normalized_gir['edges']=sorted(gir.get('edges',[]), key=lambda e:(e.get('from',''),e.get('to',''),e.get('kind','')))
    md={
        'ir':'GVM','lowered_from':'GIR','gir_hash':sha256_obj(normalized_gir),'value_registers':regs,
        'source_name':gir.get('name','unnamed'),'required_backend_abi':'0.1'
    }
    p=Program(name=gir.get('name','unnamed'),version=gir.get('version','0.1.0'),instructions=ins,exports=exports,metadata=md)
    return p
