from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import IntEnum
from typing import Any

class Op(IntEnum):
    CONST=0x0001; MOVE=0x0002
    DATA_EQ=0x0085; BOOL_NOT=0x0086; BOOL_AND=0x0087; BOOL_OR=0x0088
    INT_ADD=0x0089; INT_SUB=0x008A; INT_LT=0x008B; INT_LE=0x008C
    JUMP=0x0070; BRANCH=0x0071; HALT=0x0074
    RCALL=0x0090; RRETURN=0x0091; RECURSION_CLOSE=0x0092
    HISTORY_ENTER=0x0093; HISTORY_CHECK=0x0094; FUEL_GUARD=0x0095
    YIELD_RECURSION=0x0096; RESUME_RECURSION=0x0097

@dataclass(frozen=True)
class Instruction:
    op: Op
    out: int|None=None
    args: tuple[int,...]=()
    attrs: dict[str,Any]=field(default_factory=dict)
    result_type: str='ANY'
    source: str|None=None

@dataclass
class FunctionInfo:
    name:str
    params:list[tuple[str,str,int]]
    return_type:str
    start:int
    end:int
    mode:str
    metric_param:str|None=None
    max_depth:int|None=None
    fuel:int|None=None
    visit_key:str|None=None
    source_line:int=0

    def as_dict(self): return asdict(self)

@dataclass
class RecursiveProgram:
    module:str
    version:str
    instructions:list[Instruction]
    functions:dict[str,FunctionInfo]
    main_start:int
    exports:dict[str,int]
    metadata:dict[str,Any]=field(default_factory=dict)

@dataclass
class RecursiveExecutionResult:
    halted:bool
    exports:dict[str,Any]
    receipt:dict[str,Any]
    frames:list[dict[str,Any]]
    steps:int

@dataclass
class Param: name:str; typ:str
@dataclass
class LetStmt: name:str; typ:str; expr:str; line:int
@dataclass
class CallStmt: function:str; args:list[str]; out:str; recursive:bool; line:int
@dataclass
class ReturnStmt: value:str; line:int
@dataclass
class ExportStmt: value:str; typ:str; line:int
@dataclass
class IfStmt: cond:str; then_body:list[Any]; else_body:list[Any]; line:int
@dataclass
class RecFunction:
    name:str; params:list[Param]; return_type:str; mode:str; body:list[Any]; line:int
    metric_param:str|None=None; max_depth:int|None=None; fuel:int|None=None; visit_key:str|None=None
@dataclass
class ModuleAST:
    module:str; functions:list[RecFunction]; body:list[Any]; file:str='<memory>'; version:str='0.4.0'
