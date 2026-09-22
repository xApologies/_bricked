from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum, IntEnum
from typing import Any

class TaskState(str, Enum):
    NEW="NEW"; READY="READY"; RUNNING="RUNNING"; BLOCKED="BLOCKED"; SUSPENDED="SUSPENDED"; CLOSED="CLOSED"; FAILED="FAILED"; CANCELLED="CANCELLED"

class ClaimMode(str, Enum): SHARED="SHARED"; EXCLUSIVE="EXCLUSIVE"

class Op(IntEnum):
    WORK=0x00A0; ACQUIRE=0x00A1; RELEASE=0x00A2; YIELD=0x00A3; TASK_CLOSE=0x00A4
    RECURSION_SLICE=0x00A5; ASSERT=0x00A6

@dataclass(frozen=True)
class TaskOp:
    op: Op
    attrs: dict[str, Any] = field(default_factory=dict)
    source: str | None = None

@dataclass
class ResourceSpec:
    name: str
    capacity: int = 1
    kind: str = "FABRIC"
    def as_dict(self): return asdict(self)

@dataclass
class TaskTemplate:
    name: str
    priority: int
    quantum: int
    ops: list[TaskOp]
    kind: str = "STANDARD"
    recursion: dict[str, Any] | None = None
    def as_dict(self):
        d=asdict(self); d["ops"]=[{"op":int(x.op),"attrs":x.attrs,"source":x.source} for x in self.ops]; return d

@dataclass
class SpawnSpec:
    template: str
    handle: str

@dataclass
class ConcurrentProgram:
    module: str
    version: str
    resources: dict[str, ResourceSpec]
    templates: dict[str, TaskTemplate]
    spawns: list[SpawnSpec]
    joins: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class TaskRuntime:
    task_id: str
    template: str
    priority: int
    quantum: int
    ops: list[TaskOp]
    state: TaskState = TaskState.NEW
    pc: int = 0
    work_remaining: int = 0
    ready_seq: int = 0
    wait_seq: int = 0
    waiting_resource: str | None = None
    leases: dict[str, dict[str, Any]] = field(default_factory=dict)
    history_root: str = "0"*64
    local_steps: int = 0
    recursion: dict[str, Any] | None = None
    close_receipt: dict[str, Any] | None = None

@dataclass
class ScheduleResult:
    status: str
    tasks: dict[str, dict[str, Any]]
    events: list[dict[str, Any]]
    receipt: dict[str, Any]
    logical_ticks: int
