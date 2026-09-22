import re
from .model import TypeExpr

ALIASES={'GEO':'GEOMETRIC','QRESULT':'QRESULT','QSTATE':'QSTATE','ANY':'ANY'}

def parse_type(text):
    if isinstance(text,TypeExpr): return text
    if text is None: return TypeExpr('ANY')
    s=str(text).strip()
    m=re.fullmatch(r'([A-Za-z_][A-Za-z0-9_]*)(?:<([^<>]*)>)?',s)
    if not m: raise ValueError(f'invalid type expression {text!r}')
    kind=ALIASES.get(m.group(1).upper(),m.group(1).upper())
    params=tuple(x.strip().upper() for x in (m.group(2) or '').split(',') if x.strip())
    return TypeExpr(kind,params)

def compatible(required,actual):
    r=parse_type(required); a=parse_type(actual)
    if r.kind in ('ANY','RESOURCE'): return True
    if r.kind!=a.kind: return False
    if not r.params: return True
    if len(r.params)>len(a.params): return False
    for rp,ap in zip(r.params,a.params):
        if rp not in ('*','ANY') and rp!=ap: return False
    return True

def kind_is(t,kind): return parse_type(t).kind==kind.upper()
def sector_of(t):
    t=parse_type(t)
    if t.kind=='GEOMETRIC' and len(t.params)>=2: return t.params[1]
    if t.kind=='PORTAL' and t.params: return t.params[0]
    if t.kind=='BRIDGE' and len(t.params)>=2: return t.params[1]
    return None

def state_of(t):
    t=parse_type(t)
    if t.kind=='GEOMETRIC' and t.params: return t.params[0]
    if t.kind=='PORTAL' and len(t.params)>=2: return t.params[1]
    if t.kind in ('ROAD','QSTATE') and t.params: return t.params[0]
    return None

def erase_type(t): return parse_type(t).kind
