from __future__ import annotations
import json
from .model import Op

def disassemble(p):
    lines=[f'GCON {p.version} module {p.module}']
    for n,r in sorted(p.resources.items()):lines.append(f'RESOURCE {n} capacity={r.capacity} kind={r.kind}')
    for n,t in sorted(p.templates.items()):
        lines.append(f'TASK {n} priority={t.priority} quantum={t.quantum} kind={t.kind}')
        for i,op in enumerate(t.ops):lines.append(f'  {i:04d} {Op(op.op).name} {json.dumps(op.attrs,sort_keys=True,separators=(",",":"))}')
    for s in p.spawns:lines.append(f'SPAWN {s.template} AS {s.handle}')
    if p.joins:lines.append('JOIN '+' '.join(p.joins))
    return '\n'.join(lines)+'\n'
