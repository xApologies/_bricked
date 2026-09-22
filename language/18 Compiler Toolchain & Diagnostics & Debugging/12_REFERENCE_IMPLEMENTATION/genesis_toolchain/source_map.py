from __future__ import annotations
from .model import Span,SourceMapEntry

def source_lines(text:str)->dict[int,str]: return {i+1:l for i,l in enumerate(text.splitlines())}

def parse_instruction_source(value:str|None, fallback_source:str)->tuple[str,int]:
    if not value: return fallback_source,1
    head,sep,tail=value.rpartition(":")
    if sep and tail.isdigit(): return head,int(tail)
    return value,1

def build_source_map(program,text:str,source_name:str):
    lines=source_lines(text); out=[]
    for i,ins in enumerate(program.instructions):
        src,line=parse_instruction_source(ins.source,source_name)
        txt=lines.get(line,"")
        col=(len(txt)-len(txt.lstrip())+1) if txt else 1
        out.append(SourceMapEntry(i,ins.op.name,src,line,col,txt))
    return out

def span_for_line(text:str,source:str,line:int)->Span:
    lines=source_lines(text); raw=lines.get(line,"")
    col=(len(raw)-len(raw.lstrip())+1) if raw else 1
    return Span(source,line,col,line,len(raw)+1 if raw else col,raw)
