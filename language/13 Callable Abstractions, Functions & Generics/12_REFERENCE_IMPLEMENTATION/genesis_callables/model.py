from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class GenericParam:
    name: str
    bound: str = 'ANY'
    def as_dict(self): return {'name': self.name, 'bound': self.bound}

@dataclass(frozen=True)
class FunctionParam:
    name: str
    type: str
    def as_dict(self): return {'name': self.name, 'type': self.type}

@dataclass
class FunctionDef:
    module: str
    name: str
    generics: list[GenericParam]
    params: list[FunctionParam]
    return_type: str
    effects: set[str]
    body: list[str]
    return_value: str
    public: bool = False
    source_file: str = '<memory>'
    line: int = 0
    def qname(self): return f'{self.module}::{self.name}'
    def as_dict(self):
        return {
            'module': self.module, 'name': self.name,
            'generics': [x.as_dict() for x in self.generics],
            'params': [x.as_dict() for x in self.params],
            'return_type': self.return_type, 'effects': sorted(self.effects),
            'body': list(self.body), 'return_value': self.return_value,
            'public': self.public, 'source_file': self.source_file, 'line': self.line,
        }

@dataclass(frozen=True)
class FunctionImport:
    module: str
    symbol: str
    local: str
    line: int
    def as_dict(self): return vars(self)

@dataclass
class ExtendedModule:
    version: str
    module: str
    base_lines: list[tuple[int,str]]
    functions: list[FunctionDef]
    function_imports: list[FunctionImport]
    file: str = '<memory>'
    def as_dict(self):
        return {
            'ast': 'GENESIS-CALLABLE-AST', 'version': self.version, 'module': self.module,
            'file': self.file, 'base_lines': [{'line':n,'text':s} for n,s in self.base_lines],
            'functions': [f.as_dict() for f in self.functions],
            'function_imports': [x.as_dict() for x in self.function_imports],
        }

@dataclass
class CallSite:
    caller_module: str
    function_ref: str
    type_args: tuple[str,...]
    args: tuple[str,...]
    out: str
    line: int
    call_id: str
    source_file: str
    def as_dict(self): return vars(self)

@dataclass
class ExpansionRecord:
    call_id: str
    caller_module: str
    function: str
    specialization_id: str
    type_args: list[str]
    value_args: list[str]
    output: str
    expanded_outputs: list[str]
    declared_effects: list[str]
    actual_effects: list[str]
    source_file: str
    source_line: int
    def as_dict(self): return vars(self)

@dataclass
class CallableBuildResult:
    frontend: Any
    expanded_sources: list[tuple[str,str]]
    expansion_records: list[ExpansionRecord]
    callable_receipt: dict
    callable_proofs: list[dict]
