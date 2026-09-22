from __future__ import annotations
from dataclasses import dataclass,asdict
from typing import Any

@dataclass(frozen=True)
class StageRecord:
    stage:int
    source_sha256:str
    bytecode_sha256:str
    bytecode_ref:str
    program_id:str
    proof_root:str
    compiler_id:str
    prior_stage_sha256:str|None
    def as_dict(self): return asdict(self)

@dataclass(frozen=True)
class BootstrapResult:
    status:str
    fixed_point:bool
    self_hosted:bool
    source_sha256:str
    stages:tuple[StageRecord,...]
    frontier_root:str
    receipt_root:str
    def as_dict(self)->dict[str,Any]:
        d=asdict(self); d["stages"]=[s.as_dict() for s in self.stages]; return d
