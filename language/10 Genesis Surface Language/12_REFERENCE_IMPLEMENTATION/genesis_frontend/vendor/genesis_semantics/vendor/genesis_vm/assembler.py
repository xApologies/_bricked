from .model import Program, Instruction, Opcode, TypeTag

def assemble(obj):
    ins=[]
    for x in obj['instructions']:
        ins.append(Instruction(
            Opcode[x['op']],x.get('out'),tuple(x.get('args',[])),dict(x.get('attrs',{})),x.get('source'),TypeTag(x.get('result_type','ANY'))
        ))
    return Program(obj.get('name','assembled'),obj.get('version','0.1.0'),ins,list(obj.get('exports',[])),dict(obj.get('metadata',{})))
