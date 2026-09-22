import json

def disassemble(program):
    lines=[]
    for pc,i in enumerate(program.instructions):
        out='-' if i.out is None else f'r{i.out}:{i.result_type.value}'
        args=','.join(f'r{x}' for x in i.args)
        attrs=json.dumps(i.attrs,sort_keys=True,separators=(',',':'))
        src=f' ; {i.source}' if i.source else ''
        lines.append(f'{pc:04d} {out:<18} {i.op.name:<22} [{args}] {attrs}{src}')
    return '\n'.join(lines)+'\n'
