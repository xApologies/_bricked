from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum, IntEnum
from typing import Any

class EndpointKind(str, Enum):
    SOURCE="SOURCE"; DERIVED="DERIVED"; AUDIT="AUDIT"; BLACKGLASS="BLACKGLASS"; DEVICE="DEVICE"

class EndpointMode(str, Enum):
    READ="READ"; READ_WRITE="READ_WRITE"; APPEND="APPEND"; PROPOSE="PROPOSE"; REQUEST="REQUEST"

class Op(IntEnum):
    READ=0x00B0; WRITE_DERIVED=0x00B1; APPEND_AUDIT=0x00B2; CAS_PUT=0x00B3; CAS_GET=0x00B4
    BRANE_MOUNT=0x00B5; BRANE_REALIZE=0x00B6; BLACKGLASS_PROPOSE=0x00B7; BLACKGLASS_ADMIT=0x00B8
    DEVICE_REQUEST=0x00B9; ASSERT_EQ=0x00BA; SYS_CLOSE=0x00BB

@dataclass(frozen=True)
class EndpointSpec:
    name: str; kind: EndpointKind; mode: EndpointMode; root: str
    def as_dict(self):
        d=asdict(self); d["kind"]=self.kind.value; d["mode"]=self.mode.value; return d

@dataclass(frozen=True)
class PortManifest:
    alias: str; role: str; module_id: str; version: str; internal_dimension: int; contract_version: str
    canonical_state_policy: str; rewrite_policy: str; capabilities: tuple[str,...]
    chirality_model: str="declared"; provenance_model: str="declared"
    def as_dict(self):
        d=asdict(self); d["capabilities"]=list(self.capabilities); return d

@dataclass(frozen=True)
class Instruction:
    op: Op; attrs: dict[str,Any]=field(default_factory=dict); source: str|None=None
    def as_dict(self): return {"op":int(self.op),"attrs":self.attrs,"source":self.source}

@dataclass
class SystemProgram:
    module: str; version: str; capabilities: set[str]; endpoints: dict[str,EndpointSpec]; ports: dict[str,PortManifest]
    instructions: list[Instruction]; metadata: dict[str,Any]=field(default_factory=dict)

@dataclass(frozen=True)
class BoundaryReceipt:
    sequence: int; request_id: str; operation: str; target: str; status: str
    input_ref: str|None; output_ref: str|None; provenance_root: str; detail: dict[str,Any]=field(default_factory=dict)
    def as_dict(self): return asdict(self)

@dataclass
class RunResult:
    status: str; registers: dict[str,Any]; receipts: list[dict[str,Any]]; receipt_root: str; durable: dict[str,Any]
