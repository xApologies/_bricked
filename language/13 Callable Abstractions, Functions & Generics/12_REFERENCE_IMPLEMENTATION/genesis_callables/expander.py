from __future__ import annotations
import re
from dataclasses import replace
from .model import ExpansionRecord
from .errors import CallableError
from .util import parse_call_head, replace_identifier, replace_type_vars, sha256_obj
from genesis_frontend import parse_source
from genesis_frontend.lower import OPS
from genesis_frontend.vendor.genesis_semantics.effects import effects_for_op
from genesis_frontend.vendor.genesis_semantics.typesys import parse_type, compatible

IDENT_RX=re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

def _base_parse_line(module,line,file='<callable>'):
    src=f'genesis 0.1.0\nmodule {module} {{\n{line}\n}}\n'
    ast=parse_source(src,file)
    if len(ast.statements)!=1: raise CallableError('function body line did not produce exactly one base statement','CALLABLE_BODY')
    return ast.statements[0]

def _serialize(st):
    a=st.attrs or {}
    attr=(' @'+__import__('json').dumps(a,sort_keys=True,separators=(',',':'))) if a else ''
    out=st.out; args=st.args; t=st.declared_type
    k=st.kind
    if k=='mount': s=f'en {out} : {t or "FABRIC"} = mount {a["uri"]!r}'.replace(chr(39),chr(34))
    elif k=='alloc': s=f'en {out} : {t or "REGION"} = alloc {args[0]} cells {a["cells"]}'
    elif k=='instantiate': s=f'en {out} : {t or "GEOMETRIC"} = instantiate {args[0]} {args[1]} mmo {a["mmo"]["handle"]}'
    elif k=='fork': s=f'en {out} : {t or "GEOMETRIC"} = fork {args[0]}'
    elif k=='rel': s=f'rel {args[0]} -> {a["target"]!r} as {out}'.replace("'",'"')
    elif k=='admit': s=f'admit {args[0]} as {out}'
    elif k=='transform': s=f'transform {args[0]} with {args[1]} as {out}'
    elif k=='inherit': s=f'ar {args[0]} as {out}'
    elif k=='portal':
        s=f'portal {a["sector"]} {args[0]} with {args[1]} as {out} corridor {a["corridor"]!r}'.replace("'",'"')
        if a.get('bridge'): s+=f' bridge {str(a["bridge"]).lstrip("%")}'
    elif k=='transport': s=f've {args[1]} through {args[0]} -> {a["destination"]!r} as {out}'.replace("'",'"')
    elif k=='portal_close': s=f'tor {args[0]} with {args[1]} as {out}'
    elif k=='road_begin': s=f'road begin {args[0]} as {out}'
    elif k=='road_append': s=f'road append {args[0]} {args[1]} as {out}'
    elif k=='road_close': s=f'road close {args[0]} {args[1]} as {out}'
    elif k=='bridge': s=f'bridge {args[0]} {a["from"]} -> {a["to"]} as {out}'
    elif k.startswith('q_'):
        sub=k[2:]
        if sub=='entangle': s=f'q entangle {args[0]} {args[1]} as {out}'
        else: s=f'q {sub} {args[0]} as {out}'
    elif k=='lift': s=f'lift {args[0]} as {out}'
    elif k=='seal': s=f'seal {args[0]} as {out}'
    elif k=='assert_closure': s=f'assert closure {args[0]} as {out}'
    elif k=='emit_receipt': s=f'emit receipt as {out}'
    else: raise CallableError(f'unsupported function-body statement kind {k}','CALLABLE_BODY')
    # Remove attrs consumed into syntax from trailing JSON to avoid duplication/conflict.
    consumed={
      'mount':{'uri'},'alloc':{'cells'},'instantiate':{'mmo'},'rel':{'target'},'portal':{'sector','corridor','bridge'},'transport':{'destination'},'bridge':{'from','to'}
    }.get(k,set())
    remain={kk:vv for kk,vv in a.items() if kk not in consumed}
    if remain: s+=' @'+__import__('json').dumps(remain,sort_keys=True,separators=(',',':'))
    return s

def function_local_outputs(fn):
    outs=[]
    for line in fn.body:
        if parse_call_head(line):
            outs.append(parse_call_head(line)[3]); continue
        st=_base_parse_line(fn.module,line,fn.source_file)
        if st.out: outs.append(st.out)
    return outs

def function_direct_effects(fn):
    e=set()
    for line in fn.body:
        if parse_call_head(line): continue
        st=_base_parse_line(fn.module,line,fn.source_file)
        e |= effects_for_op(OPS[st.kind])
    return e

class Expander:
    def __init__(self,modules):
        self.modules={m.module:m for m in modules}; self.functions={}; self.records=[]; self.counter=0
        for m in modules:
            for f in m.functions: self.functions[f.qname()]=f
        self._validate_exports_imports()
        self._validate_recursion()

    def _validate_exports_imports(self):
        for m in self.modules.values():
            for imp in m.function_imports:
                q=f'{imp.module}::{imp.symbol}'
                if q not in self.functions: raise CallableError(f'unresolved callable import {q}','CALLABLE_IMPORT_UNRESOLVED',m.file,imp.line)
                if not self.functions[q].public: raise CallableError(f'function {q} is not public','CALLABLE_NOT_PUBLIC',m.file,imp.line)

    def _resolve(self,module,ref):
        if '::' in ref:
            q=ref
        else:
            local=f'{module}::{ref}'
            if local in self.functions: q=local
            else:
                m=self.modules[module]; found=[x for x in m.function_imports if x.local==ref]
                if len(found)!=1: raise CallableError(f'unknown callable {ref}','CALLABLE_UNRESOLVED',m.file,None)
                q=f'{found[0].module}::{found[0].symbol}'
        if q not in self.functions: raise CallableError(f'unknown callable {q}','CALLABLE_UNRESOLVED')
        return self.functions[q]

    def _call_dependencies(self,fn):
        deps=[]
        for line in fn.body:
            c=parse_call_head(line)
            if c: deps.append(self._resolve(fn.module,c[0]).qname())
        return deps

    def _validate_recursion(self):
        graph={q:self._call_dependencies(f) for q,f in self.functions.items()}; visiting=set(); done=set()
        def dfs(q,path):
            if q in visiting: raise CallableError(' -> '.join(path+[q]),'RECURSION_UNSUPPORTED')
            if q in done:return
            visiting.add(q)
            for r in graph[q]: dfs(r,path+[q])
            visiting.remove(q); done.add(q)
        for q in sorted(graph): dfs(q,[])

    def _sub_type(self,t,tmap): return replace_type_vars(t,tmap)

    def _validate_specialization(self,fn,type_args,file,line):
        if len(type_args)!=len(fn.generics):
            raise CallableError(f'{fn.qname()} expects {len(fn.generics)} type args, got {len(type_args)}','GENERIC_ARITY',file,line)
        tmap={g.name:t for g,t in zip(fn.generics,type_args)}
        for g,t in zip(fn.generics,type_args):
            try:
                if not compatible(g.bound,t): raise CallableError(f'{g.name}={t} does not satisfy bound {g.bound}','GENERIC_BOUND',file,line)
                parse_type(t)
            except ValueError as e: raise CallableError(str(e),'GENERIC_TYPE',file,line)
        return tmap

    def _expand_call(self,caller_module,fn,type_args,value_args,out,file,line,stack):
        if len(value_args)!=len(fn.params): raise CallableError(f'{fn.qname()} expects {len(fn.params)} args, got {len(value_args)}','CALL_ARITY',file,line)
        tmap=self._validate_specialization(fn,type_args,file,line)
        self.counter+=1; serial=self.counter
        pre={'function':fn.as_dict(),'type_args':list(type_args)}; spec='gmono-'+sha256_obj(pre)[:24]
        call_id=f'gcall-{sha256_obj({"module":caller_module,"file":file,"line":line,"serial":serial,"spec":spec})[:24]}'
        prefix=f'__c{serial}_{fn.name}_'
        localouts=function_local_outputs(fn)
        vmap={p.name:a for p,a in zip(fn.params,value_args)}
        for x in localouts: vmap[x]=prefix+x
        if fn.return_value not in localouts:
            raise CallableError(f'{fn.qname()} return must be a locally produced value in callable ABI v0.1','RETURN_NOT_LOCAL',fn.source_file,fn.line)
        # Bind the return-producing local directly to caller's requested output.
        vmap[fn.return_value]=out
        emitted=[]; actual=set(); expanded_outputs=[]
        for bodyline in fn.body:
            c=parse_call_head(bodyline)
            if c:
                nref,ntypes,nargs,nout=c
                nfn=self._resolve(fn.module,nref)
                mapped_types=tuple(self._sub_type(x,tmap) for x in ntypes)
                mapped_args=tuple(vmap.get(x,x) for x in nargs)
                mapped_out=vmap.get(nout,prefix+nout); vmap[nout]=mapped_out
                sublines,subeffects,subouts=self._expand_call(caller_module,nfn,mapped_types,mapped_args,mapped_out,file,line,stack+[fn.qname()])
                emitted.extend(sublines); actual |= subeffects; expanded_outputs.extend(subouts); continue
            # First type substitution, then value substitution, parse into canonical base statement, and alpha-rename.
            typed=replace_type_vars(bodyline,tmap)
            valued=replace_identifier(typed,vmap)
            st=_base_parse_line(caller_module,valued,file)
            emitted.append(_serialize(st)); expanded_outputs.append(st.out) if st.out else None
            actual |= effects_for_op(OPS[st.kind])
        if not actual.issubset(fn.effects):
            raise CallableError(f'{fn.qname()} actual effects {sorted(actual)} exceed declaration {sorted(fn.effects)}','FUNCTION_EFFECT_EXCEEDED',fn.source_file,fn.line)
        rec=ExpansionRecord(call_id,caller_module,fn.qname(),spec,list(type_args),list(value_args),out,[x for x in expanded_outputs if x],sorted(fn.effects),sorted(actual),file,line)
        self.records.append(rec)
        return emitted,actual,expanded_outputs

    def expand_module(self,m):
        lines=['genesis 0.1.0',f'module {m.module} {{']
        for ln,line in m.base_lines:
            c=parse_call_head(line)
            if not c:
                lines.append('  '+line); continue
            ref,targs,args,out=c; fn=self._resolve(m.module,ref)
            expanded,_,_=self._expand_call(m.module,fn,targs,args,out,m.file,ln,[])
            for x in expanded: lines.append('  '+x)
        lines.append('}')
        return '\n'.join(lines)+'\n'
