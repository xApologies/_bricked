from __future__ import annotations
import re
from .model import GenericParam,FunctionParam,FunctionDef,FunctionImport,ExtendedModule
from .errors import CallableError
from .util import split_top_level
from genesis_frontend.util import strip_comment

IDENT=r'[A-Za-z_][A-Za-z0-9_]*'
QNAME=r'[A-Za-z_][A-Za-z0-9_.]*'
FN_HEAD=re.compile(
    rf'^(pub\s+)?fn\s+({IDENT})(?:<(.+)>)?\s*\((.*)\)\s*->\s*([^\s]+)\s*(?:effects\s*\[(.*)\])?\s*\{{$'
)
USEFN=re.compile(rf'^usefn\s+({QNAME})::({IDENT})\s+as\s+({IDENT})$')

def _err(msg,code,file,line): raise CallableError(msg,code,file,line)

def _generic_list(text,file,line):
    if not text: return []
    out=[]; seen=set()
    for item in split_top_level(text):
        if ':' in item: n,b=item.split(':',1); n=n.strip(); b=b.strip()
        else: n=item.strip(); b='ANY'
        if not re.fullmatch(IDENT,n): _err(f'invalid generic parameter {n!r}','CALLABLE_SYNTAX',file,line)
        if n in seen: _err(f'duplicate generic parameter {n}','GENERIC_DUPLICATE',file,line)
        seen.add(n); out.append(GenericParam(n,b or 'ANY'))
    return out

def _param_list(text,file,line):
    if not text.strip(): return []
    out=[]; seen=set()
    for item in split_top_level(text):
        if ':' not in item: _err(f'parameter requires type: {item}','CALLABLE_SYNTAX',file,line)
        n,t=item.split(':',1); n=n.strip(); t=t.strip()
        if not re.fullmatch(IDENT,n): _err(f'invalid parameter {n!r}','CALLABLE_SYNTAX',file,line)
        if n in seen: _err(f'duplicate parameter {n}','PARAM_DUPLICATE',file,line)
        seen.add(n); out.append(FunctionParam(n,t))
    return out

def parse_extended_source(text,file='<memory>'):
    raw=text.splitlines(); clean=[]
    for n,line in enumerate(raw,1):
        s=strip_comment(line).strip()
        if s: clean.append((n,s))
    if not clean: _err('empty source','GEN_VERSION',file,1)
    if clean[0][1] not in ('genesis 0.1.0','genesis 0.2.0'):
        _err('expected `genesis 0.1.0` or `genesis 0.2.0`','GEN_VERSION',file,clean[0][0])
    version=clean[0][1].split()[1]
    if len(clean)<2: _err('missing module','MODULE_HEADER',file,clean[0][0])
    m=re.fullmatch(rf'module\s+({QNAME})\s*\{{',clean[1][1])
    if not m: _err('expected module header','MODULE_HEADER',file,clean[1][0])
    module=m.group(1)
    base=[]; funcs=[]; fimports=[]; names=set(); i=2; module_closed=False
    while i<len(clean):
        ln,line=clean[i]
        if line=='}':
            if i!=len(clean)-1: _err('content after module close','MODULE_CLOSE',file,ln)
            module_closed=True; break
        um=USEFN.fullmatch(line)
        if um:
            fimports.append(FunctionImport(um.group(1),um.group(2),um.group(3),ln)); i+=1; continue
        fm=FN_HEAD.fullmatch(line)
        if fm:
            public=bool(fm.group(1)); name=fm.group(2)
            if name in names: _err(f'duplicate function {name}','FUNCTION_DUPLICATE',file,ln)
            names.add(name)
            generics=_generic_list(fm.group(3),file,ln); params=_param_list(fm.group(4),file,ln)
            rtype=fm.group(5).strip(); effects=set(x.strip().upper() for x in split_top_level(fm.group(6) or '') if x.strip())
            body=[]; ret=None; i+=1; depth=1
            while i<len(clean):
                bl,bline=clean[i]
                # Nested function definitions are not admitted; braces inside attrs do not appear as standalone lines.
                if bline=='}':
                    depth-=1
                    if depth==0: break
                if FN_HEAD.fullmatch(bline): _err('nested functions are not supported','NESTED_FUNCTION',file,bl)
                if bline.startswith('return '):
                    if ret is not None: _err('multiple return statements','RETURN_MULTIPLE',file,bl)
                    rv=bline[7:].strip()
                    if not re.fullmatch(IDENT,rv): _err('return must name one value','RETURN_SYNTAX',file,bl)
                    ret=rv
                else: body.append(bline)
                i+=1
            if i>=len(clean) or clean[i][1]!='}': _err(f'unclosed function {name}','FUNCTION_CLOSE',file,ln)
            if ret is None: _err(f'function {name} requires return','RETURN_MISSING',file,ln)
            funcs.append(FunctionDef(module,name,generics,params,rtype,effects,body,ret,public,file,ln)); i+=1; continue
        base.append((ln,line)); i+=1
    if not module_closed: _err('missing closing `}`','MODULE_CLOSE',file,clean[-1][0])
    # Callable import aliases cannot collide with local function names or each other.
    aliases=set(names)
    for x in fimports:
        if x.local in aliases: _err(f'callable alias collision {x.local}','FUNCTION_DUPLICATE',file,x.line)
        aliases.add(x.local)
    return ExtendedModule(version,module,base,funcs,fimports,file)
