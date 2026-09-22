import json,shlex,re
from .model import Diagnostic,FrontendError,ImportDecl,ExportDecl,Statement,ModuleAST
from .util import strip_comment,split_attrs

IDENT=re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
QNAME=re.compile(r'^[A-Za-z_][A-Za-z0-9_.]*$')

def _err(code,msg,file,line): raise FrontendError(Diagnostic(code,msg,file,line))
def _id(x,file,line):
    if not IDENT.fullmatch(x): _err('SYNTAX',f'invalid identifier {x!r}',file,line)
    return x

def _tokens(core,file,line):
    try: return shlex.split(core,posix=True)
    except ValueError as e: _err('SYNTAX',str(e),file,line)

def parse_source(text,file='<memory>'):
    raw=text.splitlines(); clean=[]
    for n,line in enumerate(raw,1):
        s=strip_comment(line).strip()
        if s: clean.append((n,s))
    if not clean: _err('GEN_VERSION','empty source',file,1)
    n,s=clean[0]
    if s!='genesis 0.1.0': _err('GEN_VERSION','expected `genesis 0.1.0`',file,n)
    if len(clean)<2: _err('MODULE_HEADER','missing module',file,n)
    mn,ms=clean[1]
    m=re.fullmatch(r'module\s+([A-Za-z_][A-Za-z0-9_.]*)\s*\{',ms)
    if not m: _err('MODULE_HEADER','expected `module <name> {`',file,mn)
    module=m.group(1); imports=[]; exports=[]; statements=[]; produced=set(); closed=False
    for idx,(ln,line) in enumerate(clean[2:],start=2):
        if line=='}':
            if idx!=len(clean)-1: _err('MODULE_CLOSE','content after module close',file,ln)
            closed=True; break
        try: core,attrs=split_attrs(line)
        except json.JSONDecodeError as e: _err('ATTR_JSON',str(e),file,ln)
        t=_tokens(core,file,ln)
        if not t: continue
        if t[0]=='use':
            # use mod::symbol as local : TYPE
            if len(t)<6 or t[2]!='as' or t[4]!=':': _err('SYNTAX','use: expected `use module::symbol as local : TYPE`',file,ln)
            if '::' not in t[1]: _err('SYNTAX','use source must be module::symbol',file,ln)
            src,sym=t[1].split('::',1); local=_id(t[3],file,ln); typ=''.join(t[5:])
            imports.append(ImportDecl(src,sym,local,typ,ln)); continue
        if t[0]=='export':
            if len(t)<4 or t[2]!=':': _err('SYNTAX','export: expected `export name : TYPE`',file,ln)
            exports.append(ExportDecl(_id(t[1],file,ln),''.join(t[3:]),ln)); continue

        st=None
        if t[0]=='en':
            if len(t)<7 or t[2]!=':' or '=' not in t: _err('SYNTAX','en declaration malformed',file,ln)
            out=_id(t[1],file,ln); eq=t.index('='); typ=''.join(t[3:eq]); rhs=t[eq+1:]
            if not rhs:_err('SYNTAX','en declaration missing constructor',file,ln)
            if rhs[0]=='mount' and len(rhs)==2: st=Statement('mount',out,[],{'uri':rhs[1],**attrs},typ,ln,line)
            elif rhs[0]=='alloc' and len(rhs)==4 and rhs[2]=='cells':
                try: cells=int(rhs[3])
                except: _err('SYNTAX','cells must be integer',file,ln)
                st=Statement('alloc',out,[rhs[1]],{'cells':cells,**attrs},typ,ln,line)
            elif rhs[0]=='instantiate' and len(rhs)==5 and rhs[3]=='mmo':
                st=Statement('instantiate',out,[rhs[1],rhs[2]],{'mmo':{'class':'MMO','handle':rhs[4]},**attrs},typ,ln,line)
            elif rhs[0]=='fork' and len(rhs)==2: st=Statement('fork',out,[rhs[1]],attrs,typ,ln,line)
            else:_err('SYNTAX','unknown en constructor',file,ln)
        elif t[0]=='rel' and len(t)>=6 and t[2]=='->' and t[-2]=='as':
            st=Statement('rel',_id(t[-1],file,ln),[t[1]],{'target':t[3],**attrs},None,ln,line)
        elif t[0]=='admit' and len(t)==4 and t[2]=='as': st=Statement('admit',_id(t[3],file,ln),[t[1]],attrs,None,ln,line)
        elif t[0]=='transform' and len(t)==6 and t[2]=='with' and t[4]=='as': st=Statement('transform',_id(t[5],file,ln),[t[1],t[3]],attrs,None,ln,line)
        elif t[0]=='ar' and len(t)==4 and t[2]=='as': st=Statement('inherit',_id(t[3],file,ln),[t[1]],attrs,None,ln,line)
        elif t[0]=='portal':
            # portal GR geo with adm as p corridor "..." [bridge b]
            if len(t)<9 or t[3]!='with' or t[5]!='as' or t[7]!='corridor': _err('SYNTAX','portal statement malformed',file,ln)
            sec=t[1].upper();
            if sec not in ('GENERIC','QFT','GR'): _err('SYNTAX',f'unknown sector {sec}',file,ln)
            a={'sector':sec,'corridor':t[8],**attrs}
            if len(t)>9:
                if len(t)!=11 or t[9]!='bridge': _err('SYNTAX','portal bridge clause malformed',file,ln)
                a['bridge']='%'+_id(t[10],file,ln)
            st=Statement('portal',_id(t[6],file,ln),[t[2],t[4]],a,None,ln,line)
        elif t[0]=='ve' and len(t)==8 and t[2]=='through' and t[4]=='->' and t[6]=='as':
            st=Statement('transport',_id(t[7],file,ln),[t[3],t[1]],{'destination':t[5],**attrs},None,ln,line)
        elif t[0]=='tor' and len(t)==6 and t[2]=='with' and t[4]=='as': st=Statement('portal_close',_id(t[5],file,ln),[t[1],t[3]],attrs,None,ln,line)
        elif t[0]=='road':
            if len(t)==5 and t[1]=='begin' and t[3]=='as': st=Statement('road_begin',_id(t[4],file,ln),[t[2]],attrs,None,ln,line)
            elif len(t)==6 and t[1]=='append' and t[4]=='as': st=Statement('road_append',_id(t[5],file,ln),[t[2],t[3]],attrs,None,ln,line)
            elif len(t)==6 and t[1]=='close' and t[4]=='as': st=Statement('road_close',_id(t[5],file,ln),[t[2],t[3]],attrs,None,ln,line)
            else:_err('SYNTAX','road statement malformed',file,ln)
        elif t[0]=='bridge' and len(t)==7 and t[3]=='->' and t[5]=='as':
            st=Statement('bridge',_id(t[6],file,ln),[t[1]],{'from':t[2].upper(),'to':t[4].upper(),**attrs},None,ln,line)
        elif t[0]=='q':
            sub=t[1] if len(t)>1 else ''
            if sub in ('prepare','superpose','channel','measure') and len(t)==5 and t[3]=='as': st=Statement('q_'+sub,_id(t[4],file,ln),[t[2]],attrs,None,ln,line)
            elif sub=='entangle' and len(t)==6 and t[4]=='as': st=Statement('q_entangle',_id(t[5],file,ln),[t[2],t[3]],attrs,None,ln,line)
            else:_err('SYNTAX','quantum statement malformed',file,ln)
        elif t[0]=='lift' and len(t)==4 and t[2]=='as': st=Statement('lift',_id(t[3],file,ln),[t[1]],attrs,None,ln,line)
        elif t[0]=='seal' and len(t)==4 and t[2]=='as': st=Statement('seal',_id(t[3],file,ln),[t[1]],attrs,None,ln,line)
        elif t[0]=='assert' and len(t)==5 and t[1]=='closure' and t[3]=='as': st=Statement('assert_closure',_id(t[4],file,ln),[t[2]],attrs,None,ln,line)
        elif t[0]=='emit' and len(t)==5 and t[1]=='receipt' and t[2]=='as':
            # Accept canonical four tokens too after shlex weirdness guard below.
            st=Statement('emit_receipt',_id(t[3],file,ln),[],attrs,None,ln,line) if len(t)==4 else None
        elif t[0]=='emit' and len(t)==4 and t[1]=='receipt' and t[2]=='as': st=Statement('emit_receipt',_id(t[3],file,ln),[],attrs,None,ln,line)
        else:_err('STATEMENT_UNKNOWN',f'cannot parse statement: {line}',file,ln)
        if st is None:_err('SYNTAX',f'malformed statement: {line}',file,ln)
        if st.out:
            if st.out in produced or any(i.local==st.out for i in imports): _err('DUPLICATE_VALUE',f'duplicate local identity {st.out}',file,ln)
            produced.add(st.out)
        statements.append(st)
    if not closed:_err('MODULE_CLOSE','missing closing `}`',file,clean[-1][0])
    known=produced|{i.local for i in imports}
    for e in exports:
        if e.local not in known:_err('EXPORT_UNKNOWN',f'export {e.local} has no local value',file,e.line)
    return ModuleAST('0.1.0',module,imports,statements,exports,file)
