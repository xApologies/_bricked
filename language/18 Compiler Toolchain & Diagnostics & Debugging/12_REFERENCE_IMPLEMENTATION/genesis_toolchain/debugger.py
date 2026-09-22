from __future__ import annotations
from .model import Breakpoint,TraceRun,TraceEvent
from .source_map import parse_instruction_source

class DebugSession:
    def __init__(self,run:TraceRun): self.run=run; self.cursor=-1; self.breakpoints=[]
    def add_line_breakpoint(self,source:str,line:int): self.breakpoints.append(Breakpoint("line",f"{source}:{line}"))
    def add_opcode_breakpoint(self,opcode:str): self.breakpoints.append(Breakpoint("opcode",opcode.upper()))
    def reset(self): self.cursor=-1
    def step(self)->TraceEvent|None:
        if self.cursor+1>=len(self.run.events): return None
        self.cursor+=1; return self.run.events[self.cursor]
    def current(self)->TraceEvent|None:
        return self.run.events[self.cursor] if 0<=self.cursor<len(self.run.events) else None
    def continue_run(self)->TraceEvent|None:
        while True:
            ev=self.step()
            if ev is None or self._matches(ev): return ev
    def seek(self,index:int)->TraceEvent:
        if index<0 or index>=len(self.run.events): raise IndexError(index)
        self.cursor=index; return self.run.events[index]
    def registers(self): return {} if self.current() is None else dict(self.current().registers)
    def receipt(self): return None if self.current() is None else self.current().receipt
    def _matches(self,ev:TraceEvent)->bool:
        for bp in self.breakpoints:
            if bp.kind=="opcode" and ev.opcode==bp.value: return True
            if bp.kind=="line" and ev.source:
                src,line=parse_instruction_source(ev.source,"")
                if f"{src}:{line}"==bp.value: return True
        return False
