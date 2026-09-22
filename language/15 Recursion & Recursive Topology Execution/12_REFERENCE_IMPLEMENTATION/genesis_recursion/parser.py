from __future__ import annotations
import re
from .model import *
from .util import strip_comment,split_args,norm_type
from .errors import ParseError
IDENT=r'[A-Za-z_][A-Za-z0-9_]*'

def _err(msg,code,file,line): raise ParseError(msg,code,file,line)

def _lines(text):
    out=[]
    for n,raw in enumerate(text.splitlines(),1):
        s=strip_comment(raw).strip()
        if not s: continue
        if s=='} else {': out.append((n,'}')); out.append((n,'else {')); continue
        out.append((n,s))
    return out

def _params(text,file,line):
    out=[]; seen=set()
    for item in split_args(text):
        if ':' not in item:_err('parameter requires type','RECURSION_PARAM',file,line)
        n,t=item.split(':',1); n=n.strip(); t=norm_type(t)
        if not re.fullmatch(IDENT,n) or n in seen:_err('invalid/duplicate parameter','RECURSION_PARAM',file,line)
        seen.add(n); out.append(Param(n,t))
    return out

def _stmt(line,file,ln):
    m=re.fullmatch(rf'let\s+({IDENT})\s*:\s*([^=]+?)\s*=\s*(.+)',line)
    if m:return LetStmt(m.group(1),norm_type(m.group(2)),m.group(3).strip(),ln)
    m=re.fullmatch(rf'(recur|call)\s+({IDENT})\((.*)\)\s+as\s+({IDENT})',line)
    if m:return CallStmt(m.group(2),split_args(m.group(3)),m.group(4),m.group(1)=='recur',ln)
    m=re.fullmatch(rf'return\s+({IDENT})',line)
    if m:return ReturnStmt(m.group(1),ln)
    m=re.fullmatch(rf'export\s+({IDENT})\s*:\s*(.+)',line)
    if m:return ExportStmt(m.group(1),norm_type(m.group(2)),ln)
    _err(f'unknown statement {line!r}','RECURSION_SYNTAX',file,ln)

def _block(lines,i,file):
    body=[]
    while i<len(lines):
        ln,line=lines[i]
        if line=='}': return body,i+1
        if line=='else {':_err('orphan else','RECURSION_SYNTAX',file,ln)
        m=re.fullmatch(rf'if\s+({IDENT})\s*\{{',line)
        if m:
            tb,j=_block(lines,i+1,file); eb=[]
            if j<len(lines) and lines[j][1]=='else {': eb,j=_block(lines,j+1,file)
            body.append(IfStmt(m.group(1),tb,eb,ln)); i=j; continue
        body.append(_stmt(line,file,ln)); i+=1
    _err('unclosed block','RECURSION_SYNTAX',file,lines[-1][0] if lines else 1)

def parse_source(text,file='<memory>'):
    ls=_lines(text)
    if not ls or ls[0][1]!='genesis 0.4.0':_err('expected `genesis 0.4.0`','GEN_VERSION',file,ls[0][0] if ls else 1)
    if len(ls)<2:_err('missing module','MODULE_HEADER',file,1)
    mm=re.fullmatch(rf'module\s+({IDENT}(?:\.{IDENT})*)\s*\{{',ls[1][1])
    if not mm:_err('bad module header','MODULE_HEADER',file,ls[1][0])
    funcs=[]; main=[]; i=2
    while i<len(ls):
        ln,line=ls[i]
        if line=='}':
            if i!=len(ls)-1:_err('content after module close','MODULE_CLOSE',file,ln)
            return ModuleAST(mm.group(1),funcs,main,file)
        fm=re.fullmatch(rf'rec\s+fn\s+({IDENT})\((.*)\)\s*->\s*([^\s]+)\s+(.+)\s*\{{',line)
        if fm:
            name=fm.group(1); ps=_params(fm.group(2),file,ln); rt=norm_type(fm.group(3)); contract=fm.group(4).strip()
            metric=None; maxd=None; fuel=None; key=None; mode=None
            m=re.fullmatch(rf'decreases\s+({IDENT})\s+max_depth\s+(\d+)',contract)
            if m: mode='DECREASING'; metric=m.group(1); maxd=int(m.group(2))
            m2=re.fullmatch(r'fuel\s+(\d+)',contract)
            if m2: mode='FUEL'; fuel=int(m2.group(1)); maxd=None
            m3=re.fullmatch(rf'visit_once\s+({IDENT})\s+max_depth\s+(\d+)',contract)
            if m3: mode='VISIT_ONCE'; key=m3.group(1); maxd=int(m3.group(2))
            if not mode:_err('recursive function requires decreases/fuel/visit_once contract','RECURSION_UNGUARDED',file,ln)
            names={p.name for p in ps}
            if metric and metric not in names:_err('decreases metric must be a parameter','RECURSION_METRIC',file,ln)
            if key and key not in names:_err('visit key must be a parameter','RECURSION_VISIT_KEY',file,ln)
            b,j=_block(ls,i+1,file)
            funcs.append(RecFunction(name,ps,rt,mode,b,ln,metric,maxd,fuel,key)); i=j; continue
        main.append(_stmt(line,file,ln)); i+=1
    _err('missing module close','MODULE_CLOSE',file,ls[-1][0])
