from copy import deepcopy
from .analysis import analyze_gir
from .passes import canonicalize,dedupe_edges,coalesce_alias_moves,dead_pure_elimination
from .util import sha256_obj
from genesis_frontend.vendor.genesis_semantics import check_gir
from genesis_frontend.vendor.genesis_semantics.capabilities import check_capabilities, reference_backend_capabilities

class OptimizationError(Exception): pass

PROFILES={
 'O0':[],
 'OAUDIT':[('canonicalize',canonicalize),('dedupe_edges',dedupe_edges)],
 'O1':[('canonicalize',canonicalize),('dedupe_edges',dedupe_edges),('coalesce_alias_moves',coalesce_alias_moves),('dead_pure_elimination',dead_pure_elimination),('canonicalize_final',canonicalize)],
}

def _barriers_ok(a,b):
    keys=['effectful_order','quantum_order','portal_road_order','bridge_order','provenance_order']
    return {k:(a[k]==b[k]) for k in keys}

def optimize_gir(gir,level='O1',backend=None):
    if level not in PROFILES: raise OptimizationError(f'unknown optimization level {level}')
    before=analyze_gir(gir); cur=deepcopy(gir); records=[]
    for name,fn in PROFILES[level]:
        h0=sha256_obj(cur); cur,detail=fn(cur); h1=sha256_obj(cur)
        records.append({'pass':name,'before':h0,'after':h1,**detail})
    after=analyze_gir(cur); barriers=_barriers_ok(before,after)
    if not all(barriers.values()): raise OptimizationError('semantic barrier order changed: '+str(barriers))
    chk=check_gir(cur,export_values=cur.get('exports',[]))
    if not chk.ok: raise OptimizationError('Section09 re-check failed: '+'; '.join(d.code+':'+d.message for d in chk.diagnostics))
    cap=check_capabilities(cur,backend or reference_backend_capabilities())
    if not cap['ok']: raise OptimizationError('backend capability re-check failed')
    pre={'kind':'GENESIS_OPTIMIZATION_RECEIPT','version':'0.1.0','level':level,'before_gir_hash':before['gir_hash'],'after_gir_hash':after['gir_hash'],'passes':records,'barriers':barriers,'before_nodes':before['nodes'],'after_nodes':after['nodes'],'backend':(backend or reference_backend_capabilities()).get('backend_id')}
    receipt=dict(pre); receipt['optimization_id']='gopt-'+sha256_obj(pre)[:24]
    return cur,receipt,{'before':before,'after':after,'static_check':chk,'capability':cap}
