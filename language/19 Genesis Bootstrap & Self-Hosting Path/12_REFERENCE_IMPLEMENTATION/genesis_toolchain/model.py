from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any

class Severity(str, Enum):
    NOTE="NOTE"; WARNING="WARNING"; ERROR="ERROR"

@dataclass(frozen=True)
class Span:
    source: str
    line: int
    column: int = 1
    end_line: int | None = None
    end_column: int | None = None
    text: str | None = None
    def as_dict(self): return asdict(self)

@dataclass(frozen=True)
class Diagnostic:
    severity: Severity
    code: str
    message: str
    span: Span | None = None
    notes: tuple[str,...] = ()
    diagnostic_id: str = ""
    def as_dict(self):
        d=asdict(self); d["severity"]=self.severity.value; return d

@dataclass(frozen=True)
class SourceMapEntry:
    instruction_index: int
    opcode: str
    source: str
    line: int
    column: int
    text: str
    def as_dict(self): return asdict(self)

@dataclass(frozen=True)
class ArtifactDigest:
    name: str
    sha256: str
    size: int
    def as_dict(self): return asdict(self)

@dataclass(frozen=True)
class BuildManifest:
    build_id: str
    toolchain_version: str
    target: str
    profile: str
    source_name: str
    source_digest: str
    program_id: str
    proof_root: str
    instruction_count: int
    options: dict[str,Any]
    artifacts: tuple[ArtifactDigest,...] = ()
    def as_dict(self):
        d=asdict(self); d["artifacts"]=[a.as_dict() for a in self.artifacts]; return d

@dataclass
class BuildResult:
    ok: bool
    manifest: BuildManifest | None = None
    diagnostics: list[Diagnostic] = field(default_factory=list)
    output_dir: str | None = None
    artifact_paths: dict[str,str] = field(default_factory=dict)

@dataclass(frozen=True)
class TraceEvent:
    instruction_index: int
    opcode: str
    source: str | None
    register_delta: tuple[str,...]
    registers: dict[str,Any]
    receipt: dict[str,Any] | None
    provenance_root: str
    def as_dict(self): return asdict(self)

@dataclass(frozen=True)
class Breakpoint:
    kind: str
    value: str

@dataclass
class TraceRun:
    status: str
    events: list[TraceEvent]
    registers: dict[str,Any]
    receipts: list[dict[str,Any]]
    receipt_root: str
    durable: dict[str,Any]
