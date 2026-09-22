from __future__ import annotations
from .model import SystemProgram
from .util import canonical_json

def disassemble(p:SystemProgram)->str:
    out=[f"GENESIS-SYSTEM {p.version} MODULE {p.module}"]
    for c in sorted(p.capabilities): out.append(f"CAP {c}")
    for e in sorted(p.endpoints.values(),key=lambda x:x.name): out.append(f"ENDPOINT {e.name} {e.kind.value} {e.mode.value} root={e.root}")
    for m in sorted(p.ports.values(),key=lambda x:x.alias): out.append(f"PORT {m.alias} role={m.role} module={m.module_id} dim={m.internal_dimension} contract={m.contract_version}")
    for i,x in enumerate(p.instructions): out.append(f"{i:04d} {x.op.name} {canonical_json(x.attrs).decode('utf-8')}")
    return "\n".join(out)+"\n"
