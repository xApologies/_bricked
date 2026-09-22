from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any

class TypeTag(str, Enum):
    VOID='VOID'; BOOL='BOOL'; INT='INT'; FLOAT='FLOAT'; TEXT='TEXT'; HASH='HASH'; SECTOR='SECTOR'
    FABRIC_ADDR='FABRIC_ADDR'; REGION='REGION'; FABRIC='FABRIC'; MMO='MMO'; GEOMETRIC='GEOMETRIC'
    RELATION='RELATION'; ADMISSION='ADMISSION'; TRANSFORM='TRANSFORM'; PORTAL='PORTAL'; ROAD='ROAD'
    BRIDGE='BRIDGE'; QSTATE='QSTATE'; QRESULT='QRESULT'; M5='M5'; RECEIPT='RECEIPT'; ANY='ANY'

class Effect(str, Enum):
    READ_FABRIC='READ_FABRIC'; WRITE_OVERLAY='WRITE_OVERLAY'; ALLOCATE='ALLOCATE'; RELATE='RELATE'; ADMIT='ADMIT'
    TRANSFORM='TRANSFORM'; TRANSPORT='TRANSPORT'; CLOSE='CLOSE'; INHERIT='INHERIT'; PROJECT='PROJECT'
    TRANSDUCE='TRANSDUCE'; MEASURE='MEASURE'; QUANTUM_LINEAR='QUANTUM_LINEAR'; PROVENANCE='PROVENANCE'; CONTROL='CONTROL'

class Opcode(IntEnum):
    NOP=0x0000; CONST=0x0001; MOVE=0x0002; HASH=0x0003
    FABRIC_MOUNT=0x0010; FABRIC_ALLOC=0x0011; FABRIC_READ=0x0012; FABRIC_WRITE_OVERLAY=0x0013
    GEO_INSTANTIATE=0x0020; GEO_FORK=0x0021; RELATE=0x0022; ADMIT=0x0023; TRANSFORM=0x0024; INHERIT=0x0025
    PORTAL_OPEN=0x0030; PORTAL_TRANSPORT=0x0031; PORTAL_CLOSE=0x0032; ROAD_BEGIN=0x0033; ROAD_APPEND=0x0034; ROAD_CLOSE=0x0035
    BRIDGE_SECTOR=0x0040
    Q_PREPARE=0x0050; Q_SUPERPOSE=0x0051; Q_ENTANGLE=0x0052; Q_CHANNEL=0x0053; Q_MEASURE=0x0054
    BRANE_LIFT=0x0060; PROVENANCE_SEAL=0x0061; ASSERT_CLOSURE=0x0062; EMIT_RECEIPT=0x0063
    JUMP=0x0070; BRANCH=0x0071; CALL=0x0072; RETURN=0x0073; HALT=0x0074

@dataclass(frozen=True)
class Instruction:
    op: Opcode
    out: int | None = None
    args: tuple[int, ...] = ()
    attrs: dict[str, Any] = field(default_factory=dict)
    source: str | None = None
    result_type: TypeTag = TypeTag.ANY

@dataclass
class Program:
    name: str
    version: str = '0.1.0'
    instructions: list[Instruction] = field(default_factory=list)
    exports: list[int] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class TaggedValue:
    type: TypeTag
    value: Any
    linear_state: str | None = None

@dataclass
class ExecutionResult:
    halted: bool
    registers: dict[int, TaggedValue]
    exports: dict[int, TaggedValue]
    receipt: dict[str, Any]
