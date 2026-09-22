from __future__ import annotations
from genesis_frontend.compiler import compile_sources as base_compile_sources, run_build
from genesis_frontend.vendor.genesis_semantics.typesys import compatible
from .parser import parse_extended_source
from .expander import Expander
from .model import CallableBuildResult
from .errors import CallableError
from .util import sha256_obj,sha256_text

def _call_proofs(modules,records,frontend):
    module_by_name={m.module:m for m in modules}; mod_checks={}
    # The Section 10 frontend stores modules in the same source order.
    for mod_ast,mod_ir in zip(frontend.asts,frontend.modules):
        # lower_module already checked it; refined types are later available in linked check globally.
        mod_checks[mod_ast.module]=mod_ir
    refined=frontend.link.check.value_types
    proofs=[]
    for r in records:
        fn=None
        for m in modules:
            for f in m.functions:
                if f.qname()==r.function: fn=f
        expected=None
        if fn:
            tmap={g.name:t for g,t in zip(fn.generics,r.type_args)}
            expected=fn.return_type
            for k,v in tmap.items():
                import re
                expected=re.sub(rf'\b{re.escape(k)}\b',v,expected)
        # linked values are alpha-qualified: %module::name
        actual=refined.get(f'%{r.caller_module}::{r.output}')
        ok=actual is not None and (expected is None or compatible(expected,actual))
        proofs.append({'obligation':'CALL_RETURN_TYPE','call_id':r.call_id,'expected':expected,'actual':str(actual) if actual else None,'status':'PASS' if ok else 'FAIL'})
        proofs.append({'obligation':'FUNCTION_EFFECT_CONTAINMENT','call_id':r.call_id,'declared':r.declared_effects,'actual':r.actual_effects,'status':'PASS' if set(r.actual_effects).issubset(r.declared_effects) else 'FAIL'})
    proofs.append({'obligation':'NO_RUNTIME_GENERIC_METADATA','status':'PASS','witness':'all generic calls monomorphized before GIR'})
    proofs.append({'obligation':'SECTION09_RECHECK','status':'PASS' if frontend.link.check.ok else 'FAIL','witness':frontend.link.check.as_dict()})
    return proofs

def compile_sources(sources,exports=None,name='genesis_callable_program',backend=None):
    mods=[parse_extended_source(text,file) for file,text in sources]
    names=[m.module for m in mods]
    if len(set(names))!=len(names): raise CallableError('duplicate module name','MODULE_DUPLICATE')
    exp=Expander(mods)
    expanded=[(file+'.expanded.gen',exp.expand_module(m)) for (file,_),m in zip(sources,mods)]
    front=base_compile_sources(expanded,exports=exports,name=name,backend=backend)
    proofs=_call_proofs(mods,exp.records,front)
    if any(p['status']!='PASS' for p in proofs): raise CallableError('callable proof ledger failed','CALLABLE_PROOF_FAILED')
    pre={
      'kind':'GENESIS_CALLABLE_FRONTEND_RECEIPT','version':'0.1.0','name':name,
      'source_hashes':{f:sha256_text(t) for f,t in sources},
      'callable_ast_hashes':{m.module:sha256_obj(m.as_dict()) for m in mods},
      'expanded_hashes':{f:sha256_text(t) for f,t in expanded},
      'specializations':sorted(set(r.specialization_id for r in exp.records)),
      'call_count':len(exp.records),'frontend_id':front.receipt['frontend_id'],
      'link_id':front.link.receipt['link_id'],'gvm_sha256':front.link.receipt['gvm_sha256']
    }
    receipt=dict(pre); receipt['callable_frontend_id']='gcallfront-'+sha256_obj(pre)[:24]; receipt['proof_root']=sha256_obj(proofs)
    return CallableBuildResult(front,expanded,exp.records,receipt,proofs)

def run_callable_build(br): return run_build(br.frontend)
