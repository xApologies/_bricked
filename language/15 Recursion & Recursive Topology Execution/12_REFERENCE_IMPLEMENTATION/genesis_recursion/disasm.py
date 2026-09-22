from .model import Op
import json

def disassemble(p):
    starts={f.start:name for name,f in p.functions.items()}; starts[p.main_start]='__main__'
    lines=[f'; Genesis Recursive Bytecode {p.module} {p.version}']
    for pc,i in enumerate(p.instructions):
        if pc in starts: lines.append(f'\n.func {starts[pc]}:')
        a=' '.join(f'r{x}' for x in i.args); out=f'r{i.out} = ' if i.out is not None else ''; attrs=(' '+json.dumps(i.attrs,sort_keys=True,separators=(',',':'))) if i.attrs else ''
        lines.append(f'{pc:04d}: {out}{i.op.name} {a}{attrs}'.rstrip())
    return '\n'.join(lines)+'\n'
