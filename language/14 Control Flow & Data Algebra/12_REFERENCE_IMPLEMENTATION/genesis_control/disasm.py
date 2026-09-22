import json
def disassemble(program):
    lines=[f'GVM/CF {program.version} {program.name}']
    for pc,i in enumerate(program.instructions):
        out='-' if i.out is None else f'r{i.out}'; args=' '.join(f'r{x}' for x in i.args)
        attrs=json.dumps(i.attrs,sort_keys=True,separators=(',',':'))
        lines.append(f'{pc:04d} {i.op.name:<18} {out:<5} {args:<16} {i.result_type.value:<10} {attrs}')
    return '\n'.join(lines)+'\n'
