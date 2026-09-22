from dataclasses import dataclass, field
from typing import Any

@dataclass
class Diagnostic:
    code:str; message:str; file:str='<memory>'; line:int=0; column:int=1
    def __str__(self): return f'{self.code} {self.file}:{self.line}:{self.column}: {self.message}'
    def as_dict(self): return {'code':self.code,'message':self.message,'file':self.file,'line':self.line,'column':self.column}

class FrontendError(Exception):
    def __init__(self, diagnostic):
        self.diagnostic=diagnostic if isinstance(diagnostic,Diagnostic) else Diagnostic('FRONTEND',str(diagnostic))
        super().__init__(str(self.diagnostic))

@dataclass
class ImportDecl:
    module:str; symbol:str; local:str; type:str; line:int
    def as_dict(self): return vars(self)

@dataclass
class ExportDecl:
    local:str; type:str; line:int
    def as_dict(self): return vars(self)

@dataclass
class Statement:
    kind:str; out:str|None; args:list[str]=field(default_factory=list); attrs:dict[str,Any]=field(default_factory=dict)
    declared_type:str|None=None; line:int=0; surface:str=''
    def as_dict(self): return {'kind':self.kind,'out':self.out,'args':self.args,'attrs':self.attrs,'declared_type':self.declared_type,'line':self.line,'surface':self.surface}

@dataclass
class ModuleAST:
    version:str; module:str; imports:list[ImportDecl]; statements:list[Statement]; exports:list[ExportDecl]; file:str='<memory>'
    def as_dict(self): return {'ast':'GENESIS-AST','version':self.version,'module':self.module,'file':self.file,'imports':[x.as_dict() for x in self.imports],'statements':[x.as_dict() for x in self.statements],'exports':[x.as_dict() for x in self.exports]}
