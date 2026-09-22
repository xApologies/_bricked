from __future__ import annotations
import re
from .model import *
from .util import strip_comment,split_top,normalize_type
from .errors import ControlError
IDENT=r'[A-Za-z_][A-Za-z0-9_]*'

def _err(msg,code,file,line): raise ControlError(msg,code,file,line)

def _logical_lines(text):
    out=[]
    for n,raw in enumerate(text.splitlines(),1):
        s=strip_comment(raw).strip()
        if not s: continue
        if s=='} else {': out.append((n,'}')); out.append((n,'else {')); continue
        out.append((n,s))
    return out

def _parse_decl(line,file,ln):
    m=re.fullmatch(rf'record\s+({IDENT})\s*\{{(.*)\}}',line)
    if m:
        fields={}
        for x in split_top(m.group(2)):
            if ':' not in x:_err('record field requires type','DATA_DECL',file,ln)
            n,t=x.split(':',1); n=n.strip(); t=normalize_type(t)
            if not re.fullmatch(IDENT,n) or n in fields:_err('invalid/duplicate record field','DATA_DECL',file,ln)
            fields[n]=t
        return TypeDecl('record',m.group(1),fields=fields,line=ln)
    m=re.fullmatch(rf'enum\s+({IDENT})\s*\{{(.*)\}}',line)
    if m:
        variants={}
        for x in split_top(m.group(2)):
            vm=re.fullmatch(rf'({IDENT})(?:\((.+)\))?',x)
            if not vm or vm.group(1) in variants:_err('invalid/duplicate enum variant','DATA_DECL',file,ln)
            variants[vm.group(1)]=normalize_type(vm.group(2)) if vm.group(2) else None
        return TypeDecl('enum',m.group(1),variants=variants,line=ln)
    return None

def _parse_simple(line,file,ln):
    m=re.fullmatch(rf'let\s+({IDENT})\s*:\s*(.+?)\s*=\s*(.+)',line)
    if m:return LetStmt(m.group(1),normalize_type(m.group(2)),m.group(3).strip(),ln)
    m=re.fullmatch(rf'export\s+({IDENT})\s*:\s*(.+)',line)
    if m:return ExportStmt(m.group(1),normalize_type(m.group(2)),ln)
    return BaseStmt(line,ln)

def _parse_block(lines,i,file):
    body=[]
    while i<len(lines):
        ln,line=lines[i]
        if line=='}': return body,i+1
        if line=='else {': _err('orphan else','CONTROL_SYNTAX',file,ln)
        m=re.fullmatch(rf'if\s+({IDENT})\s*\{{',line)
        if m:
            thenb,j=_parse_block(lines,i+1,file); elseb=[]
            if j<len(lines) and lines[j][1]=='else {': elseb,j=_parse_block(lines,j+1,file)
            body.append(IfStmt(m.group(1),thenb,elseb,ln)); i=j; continue
        m=re.fullmatch(r'repeat\s+(\d+)\s*\{',line)
        if m:
            b,j=_parse_block(lines,i+1,file); body.append(RepeatStmt(int(m.group(1)),b,ln)); i=j; continue
        m=re.fullmatch(rf'match\s+({IDENT})\s*\{{',line)
        if m:
            cases=[]; j=i+1
            while j<len(lines):
                cln,cline=lines[j]
                if cline=='}': j+=1; break
                cm=re.fullmatch(rf'({IDENT}|_)(?:\(({IDENT})\))?\s*=>\s*\{{',cline)
                if not cm:_err('malformed match case','CONTROL_SYNTAX',file,cln)
                cb,nj=_parse_block(lines,j+1,file); cases.append(MatchCase(cm.group(1),cm.group(2),cb,cln)); j=nj
            else:_err('unclosed match','CONTROL_SYNTAX',file,ln)
            body.append(MatchStmt(m.group(1),cases,ln)); i=j; continue
        if line.endswith('{'):_err(f'unknown block header {line}','CONTROL_SYNTAX',file,ln)
        body.append(_parse_simple(line,file,ln)); i+=1
    _err('unclosed block','CONTROL_SYNTAX',file,lines[-1][0] if lines else 1)

def parse_source(text,file='<memory>'):
    lines=_logical_lines(text)
    if not lines:_err('empty source','GEN_VERSION',file,1)
    if lines[0][1]!='genesis 0.3.0':_err('expected `genesis 0.3.0`','GEN_VERSION',file,lines[0][0])
    if len(lines)<2:_err('missing module','MODULE_HEADER',file,lines[0][0])
    m=re.fullmatch(rf'module\s+({IDENT}(?:\.{IDENT})*)\s*\{{',lines[1][1])
    if not m:_err('bad module header','MODULE_HEADER',file,lines[1][0])
    declarations={}; filtered=lines[:2]; i=2
    depth=0
    while i<len(lines):
        ln,line=lines[i]
        if depth==0:
            d=_parse_decl(line,file,ln)
            if d:
                if d.name in declarations:_err('duplicate data type','DATA_DECL',file,ln)
                declarations[d.name]=d; i+=1; continue
        filtered.append((ln,line))
        # declarations are only removed at module top-level; this light depth tracker prevents accidental removal inside blocks
        if line.endswith('{') and line not in ('else {',): depth+=1
        if line=='}' and depth>0: depth-=1
        i+=1
    body,end=_parse_block(filtered,2,file)
    if end!=len(filtered):_err('content after module close','MODULE_CLOSE',file,filtered[end][0])
    return ModuleAST(m.group(1),declarations,body,file)
