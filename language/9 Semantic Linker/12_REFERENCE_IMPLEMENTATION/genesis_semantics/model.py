from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class TypeExpr:
    kind: str
    params: tuple[str,...]=()
    def __str__(self):
        return self.kind if not self.params else f"{self.kind}<{','.join(self.params)}>"

@dataclass
class Diagnostic:
    code: str
    message: str
    node: str|None=None
    module: str|None=None
    severity: str='ERROR'
    def as_dict(self): return {'code':self.code,'message':self.message,'node':self.node,'module':self.module,'severity':self.severity}

@dataclass
class CheckResult:
    ok: bool
    diagnostics: list[Diagnostic]=field(default_factory=list)
    value_types: dict[str,TypeExpr]=field(default_factory=dict)
    effects: set[str]=field(default_factory=set)
    witnesses: dict[str,Any]=field(default_factory=dict)
    def as_dict(self):
        return {'ok':self.ok,'diagnostics':[d.as_dict() for d in self.diagnostics], 'value_types':{k:str(v) for k,v in sorted(self.value_types.items())}, 'effects':sorted(self.effects), 'witnesses':self.witnesses}

@dataclass
class LinkResult:
    gir: dict
    program: Any
    bytecode: bytes
    receipt: dict
    proofs: list[dict]
    check: CheckResult
