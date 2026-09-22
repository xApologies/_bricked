from __future__ import annotations
import re
from .model import Diagnostic,Severity
from .source_map import span_for_line
from .util import digest_obj

MESSAGES={
"SYSTEM_VERSION":"unsupported or malformed Genesis system version",
"SYSTEM_MODULE":"malformed module declaration",
"SYSTEM_MODULE_CLOSE":"module is not closed",
"SYSTEM_PARSE":"source statement could not be parsed",
"SYSTEM_ENDPOINT_DECL":"endpoint declaration is malformed",
"SYSTEM_ENDPOINT_DUPLICATE":"endpoint name is declared more than once",
"SYSTEM_ENDPOINT_UNKNOWN":"referenced endpoint is not declared",
"SYSTEM_ENDPOINT_MODE":"operation is not allowed by endpoint mode",
"SYSTEM_REGISTER_UNDEFINED":"register is used before it is defined",
"SYSTEM_REGISTER_REDEFINED":"register is defined more than once",
"SYSTEM_PROGRAM_UNCLOSED":"program must close before execution",
"SYSTEM_AFTER_CLOSE":"instruction occurs after program closure",
"SYSTEM_ASSERT_FAILED":"runtime equality assertion failed",
"BRANE_PORT_DECL":"BRANE port declaration is malformed",
"BRANE_PORT_DUPLICATE":"BRANE port alias is declared more than once",
"BRANE_PORT_INVALID":"BRANE port is invalid or unknown",
"BRANE_PORT_NOT_MOUNTED":"BRANE port must be mounted before realization",
"BRANE_CAPABILITY_UNAVAILABLE":"requested BRANE capability is not declared by the mounted port",
"BRANE_Z_CALLER_OWNED":"caller attempted to assign BRANE-owned realization coordinate Z",
}

def from_exception(exc:Exception,text:str,source_name:str)->Diagnostic:
    raw=str(exc); code=raw.split(":",1)[0].strip() or "GENESIS_TOOLCHAIN_FAILURE"
    line=_extract_line(raw)
    span=span_for_line(text,source_name,line) if line else None
    msg=MESSAGES.get(code,raw)
    notes=()
    if raw!=code and raw!=msg: notes=(raw,)
    payload={"severity":"ERROR","code":code,"message":msg,"span":span.as_dict() if span else None,"notes":notes}
    did="diag:"+digest_obj(payload)
    return Diagnostic(Severity.ERROR,code,msg,span,notes,did)

def _extract_line(raw:str)->int|None:
    m=re.search(r"line\s+(\d+)",raw)
    if m: return int(m.group(1))
    # parser often emits file:line
    m=re.search(r":(\d+)(?:\s|$)",raw)
    return int(m.group(1)) if m else None

def render(d:Diagnostic)->str:
    loc=""
    if d.span: loc=f"{d.span.source}:{d.span.line}:{d.span.column}: "
    out=f"{loc}{d.severity.value.lower()}[{d.code}]: {d.message}"
    if d.span and d.span.text:
        out += "\n  " + d.span.text
        out += "\n  " + " "*(max(0,d.span.column-1)) + "^"
    for n in d.notes: out += "\n  note: "+n
    return out
