from __future__ import annotations
import re
from dataclasses import dataclass
from .model import *
from .parser import parse_source
from .util import norm_type,sha256_obj
from .errors import CompileError

@dataclass
class _Value:
    reg:int; typ:str; prov:tuple|None=None

class _Builder:
    def __init__(self,name,file,fn=None):
        self.name=name; self.file=file; self.fn=fn; self.ins=[]; self.env={}; self.nextreg=0; self.exports={}
        if fn:
            for p in fn.params:
                r=self.newreg(); prov=('metric',0) if fn.metric_param==p.name else None
                self.env[p.name]=_Value(r,p.typ,prov)
    def newreg(self):
        r=self.nextreg; self.nextreg+=1
        if r>=256: raise CompileError('frame register budget exceeded','RECURSION_REGISTER_BUDGET',self.file,0)
        return r
    def emit(self,op,out=None,args=(),attrs=None,typ='ANY',line=0):
        self.ins.append(Instruction(op,out,tuple(args),attrs or {},typ,f'{self.file}:{line}')); return len(self.ins)-1
    def bind(self,name,typ,line,prov=None):
        if name in self.env: raise CompileError(f'duplicate identity {name}','RECURSION_DUPLICATE',self.file,line)
        r=self.newreg(); self.env[name]=_Value(r,norm_type(typ),prov); return r
    def val(self,name,line):
        if name not in self.env: raise CompileError(f'unknown identity {name}','RECURSION_IDENTITY',self.file,line)
        return self.env[name]
    def expr(self,e,declared,line,out):
        dt=norm_type(declared); e=e.strip()
        if re.fullmatch(r'-?\d+',e):
            if dt!='INT': raise CompileError('integer literal type mismatch','RECURSION_TYPE',self.file,line)
            v=int(e); self.emit(Op.CONST,out,attrs={'value':v},typ='INT',line=line); return ('const',v)
        if e in ('true','false'):
            if dt!='BOOL': raise CompileError('bool literal type mismatch','RECURSION_TYPE',self.file,line)
            self.emit(Op.CONST,out,attrs={'value':e=='true'},typ='BOOL',line=line); return ('const_bool',e=='true')
        m=re.fullmatch(r'move\s+([A-Za-z_][A-Za-z0-9_]*)',e)
        if m:
            x=self.val(m.group(1),line)
            if dt!=x.typ: raise CompileError('move type mismatch','RECURSION_TYPE',self.file,line)
            self.emit(Op.MOVE,out,[x.reg],typ=dt,line=line); return x.prov
        m=re.fullmatch(r'(add|sub|lt|le|eq|and|or)\s+([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z_][A-Za-z0-9_]*)',e)
        if m:
            op,a,b=m.groups(); av=self.val(a,line); bv=self.val(b,line)
            if op in ('add','sub','lt','le') and (av.typ!='INT' or bv.typ!='INT'): raise CompileError('integer operator requires INT','RECURSION_TYPE',self.file,line)
            if op in ('and','or') and (av.typ!='BOOL' or bv.typ!='BOOL'): raise CompileError('boolean operator requires BOOL','RECURSION_TYPE',self.file,line)
            if op=='eq' and av.typ!=bv.typ: raise CompileError('eq operands must match','RECURSION_TYPE',self.file,line)
            rt='INT' if op in ('add','sub') else 'BOOL'
            if dt!=rt: raise CompileError('operator result type mismatch','RECURSION_TYPE',self.file,line)
            opcode={'add':Op.INT_ADD,'sub':Op.INT_SUB,'lt':Op.INT_LT,'le':Op.INT_LE,'eq':Op.DATA_EQ,'and':Op.BOOL_AND,'or':Op.BOOL_OR}[op]
            self.emit(opcode,out,[av.reg,bv.reg],typ=rt,line=line)
            if op in ('add','sub'):
                # affine provenance relative to the declared metric
                if av.prov and av.prov[0]=='metric' and bv.prov and bv.prov[0]=='const':
                    return ('metric',av.prov[1]+(bv.prov[1] if op=='add' else -bv.prov[1]))
                if av.prov and av.prov[0]=='const' and bv.prov and bv.prov[0]=='const':
                    return ('const',av.prov[1]+(bv.prov[1] if op=='add' else -bv.prov[1]))
            return None
        m=re.fullmatch(r'not\s+([A-Za-z_][A-Za-z0-9_]*)',e)
        if m:
            a=self.val(m.group(1),line)
            if a.typ!='BOOL' or dt!='BOOL': raise CompileError('not requires BOOL','RECURSION_TYPE',self.file,line)
            self.emit(Op.BOOL_NOT,out,[a.reg],typ='BOOL',line=line); return None
        raise CompileError(f'unsupported expression {e!r}','RECURSION_EXPR',self.file,line)

class Compiler:
    def __init__(self,ast): self.ast=ast; self.fmap={f.name:f for f in ast.functions}
    def _compile_block(self,b,stmts,allow_return):
        terminated=False
        for st in stmts:
            if terminated: raise CompileError('unreachable statement after return','RECURSION_UNREACHABLE',b.file if hasattr(b,'file') else self.ast.file,getattr(st,'line',0))
            if isinstance(st,LetStmt):
                r=b.bind(st.name,st.typ,st.line); p=b.expr(st.expr,st.typ,st.line,r); b.env[st.name].prov=p
            elif isinstance(st,CallStmt):
                if st.function not in self.fmap: raise CompileError(f'unknown function {st.function}','RECURSION_CALL_UNKNOWN',self.ast.file,st.line)
                fn=self.fmap[st.function]
                if st.recursive and (not b.fn or st.function!=b.fn.name): raise CompileError('recur may target only current function','RECURSION_RECUR_TARGET',self.ast.file,st.line)
                if not st.recursive and b.fn and st.function==b.fn.name: raise CompileError('self-call must use recur','RECURSION_RECUR_REQUIRED',self.ast.file,st.line)
                if len(st.args)!=len(fn.params): raise CompileError('call arity mismatch','RECURSION_ARITY',self.ast.file,st.line)
                vals=[b.val(x,st.line) for x in st.args]
                for v,p in zip(vals,fn.params):
                    if v.typ!=p.typ: raise CompileError('call argument type mismatch','RECURSION_TYPE',self.ast.file,st.line)
                attrs={'function':fn.name,'recursive':bool(st.recursive)}
                if st.recursive and fn.mode=='DECREASING':
                    mi=next(i for i,p in enumerate(fn.params) if p.name==fn.metric_param); pv=vals[mi].prov
                    if not pv or pv[0]!='metric' or pv[1]>=0: raise CompileError('recursive metric is not statically decreasing','RECURSION_NOT_DECREASING',self.ast.file,st.line)
                    attrs['measure_delta']=pv[1]; attrs['metric_arg_index']=mi
                if st.recursive and fn.mode=='VISIT_ONCE': attrs['visit_arg_index']=next(i for i,p in enumerate(fn.params) if p.name==fn.visit_key)
                out=b.bind(st.out,fn.return_type,st.line)
                b.emit(Op.RCALL,out,[v.reg for v in vals],attrs,fn.return_type,st.line)
            elif isinstance(st,ReturnStmt):
                if not allow_return: raise CompileError('return outside recursive function','RECURSION_RETURN_CONTEXT',self.ast.file,st.line)
                v=b.val(st.value,st.line)
                if v.typ!=b.fn.return_type: raise CompileError('return type mismatch','RECURSION_TYPE',self.ast.file,st.line)
                b.emit(Op.RECURSION_CLOSE,None,[v.reg],{'function':b.fn.name},'VOID',st.line)
                b.emit(Op.RRETURN,None,[v.reg],{'function':b.fn.name},'VOID',st.line); terminated=True
            elif isinstance(st,ExportStmt):
                if allow_return: raise CompileError('export only permitted in module main','RECURSION_EXPORT_CONTEXT',self.ast.file,st.line)
                v=b.val(st.value,st.line)
                if v.typ!=st.typ: raise CompileError('export type mismatch','RECURSION_TYPE',self.ast.file,st.line)
                b.exports[st.value]=v.reg
            elif isinstance(st,IfStmt):
                c=b.val(st.cond,st.line)
                if c.typ!='BOOL': raise CompileError('if requires BOOL','RECURSION_TYPE',self.ast.file,st.line)
                # Branches share values defined before the branch. Branch-local values do not escape.
                pre=dict(b.env)
                br=b.emit(Op.BRANCH,None,[c.reg],{'true':None,'false':None},'VOID',st.line)
                true_start=len(b.ins); b.env=dict(pre); tterm=self._compile_block(b,st.then_body,allow_return); tj=None
                if not tterm: tj=b.emit(Op.JUMP,None,(),{'target':None},'VOID',st.line)
                false_start=len(b.ins); b.env=dict(pre); fterm=self._compile_block(b,st.else_body,allow_return)
                end=len(b.ins)
                b.ins[br]=Instruction(Op.BRANCH,None,(c.reg,),{'true':true_start,'false':false_start},'VOID',b.ins[br].source)
                if tj is not None: b.ins[tj]=Instruction(Op.JUMP,None,(),{'target':end},'VOID',b.ins[tj].source)
                b.env=pre
                terminated=tterm and fterm
            else: raise CompileError('unknown AST statement','RECURSION_AST',self.ast.file,getattr(st,'line',0))
        return terminated
    def compile(self):
        pieces=[]; infos={}; call_graph={f.name:set() for f in self.ast.functions}
        # functions first
        for fn in self.ast.functions:
            if fn.max_depth is not None and not 1<=fn.max_depth<=4096: raise CompileError('max depth out of range','RECURSION_DEPTH',self.ast.file,fn.line)
            if fn.fuel is not None and not 1<=fn.fuel<=4096: raise CompileError('fuel out of range','RECURSION_FUEL',self.ast.file,fn.line)
            b=_Builder(fn.name,self.ast.file,fn)
            term=self._compile_block(b,fn.body,True)
            if not term: raise CompileError(f'function {fn.name} has path without return','RECURSION_RETURN_MISSING',self.ast.file,fn.line)
            pieces.append((fn.name,b,fn))
            for i in b.ins:
                if i.op==Op.RCALL: call_graph[fn.name].add(i.attrs['function'])
        # reject mutual cycles; self edges are legal under contracts
        visiting=set(); done=set()
        def dfs(q,path):
            if q in visiting:
                if path and path[-1]==q:return
                raise CompileError('mutual recursion unsupported in v0.1','RECURSION_MUTUAL_UNSUPPORTED',self.ast.file,0)
            if q in done:return
            visiting.add(q)
            for r in call_graph.get(q,set()):
                if r==q: continue
                dfs(r,path+[q])
            visiting.remove(q); done.add(q)
        for q in call_graph: dfs(q,[])
        mb=_Builder('__main__',self.ast.file,None); self._compile_block(mb,self.ast.body,False); mb.emit(Op.HALT,None,(),{},'VOID',0); pieces.append(('__main__',mb,None))
        allins=[]
        for name,b,fn in pieces:
            off=len(allins)
            # patch local branch/jump targets to global PCs
            for ins in b.ins:
                attrs=dict(ins.attrs)
                if ins.op==Op.BRANCH:
                    attrs['true']=off+attrs['true']; attrs['false']=off+attrs['false']
                if ins.op==Op.JUMP: attrs['target']=off+attrs['target']
                allins.append(Instruction(ins.op,ins.out,ins.args,attrs,ins.result_type,ins.source))
            if fn:
                infos[name]=FunctionInfo(name,[(p.name,p.typ,i) for i,p in enumerate(fn.params)],fn.return_type,off,off+len(b.ins),fn.mode,fn.metric_param,fn.max_depth,fn.fuel,fn.visit_key,fn.line)
            else: main_start=off; main_exports=dict(b.exports)
        meta={'section':'15','compiler':'GENESIS_RECURSION_COMPILER_V0_1','call_graph':{k:sorted(v) for k,v in call_graph.items()}}
        prog=RecursiveProgram(self.ast.module,'0.4.0',allins,infos,main_start,main_exports,meta)
        from .verifier import verify
        prog.metadata['verification']=verify(prog)
        prog.metadata['program_id']='grec-'+sha256_obj({'module':prog.module,'instructions':[(int(i.op),i.out,i.args,i.attrs,i.result_type) for i in prog.instructions]})[:32]
        return prog

def compile_source(text,file='<memory>'): return Compiler(parse_source(text,file)).compile()
