from .model import Diagnostic,FrontendError
from .util import coarse_type,sha256_obj
from .vendor.genesis_semantics import check_module
from .vendor.genesis_semantics.effects import effects_for_op

OPS={
'mount':'FABRIC_MOUNT','alloc':'FABRIC_ALLOC','instantiate':'GEO_INSTANTIATE','fork':'GEO_FORK','rel':'RELATE','admit':'ADMIT','transform':'TRANSFORM','inherit':'INHERIT','portal':'PORTAL_OPEN','transport':'PORTAL_TRANSPORT','portal_close':'PORTAL_CLOSE','road_begin':'ROAD_BEGIN','road_append':'ROAD_APPEND','road_close':'ROAD_CLOSE','bridge':'BRIDGE_SECTOR','q_prepare':'Q_PREPARE','q_superpose':'Q_SUPERPOSE','q_entangle':'Q_ENTANGLE','q_channel':'Q_CHANNEL','q_measure':'Q_MEASURE','lift':'BRANE_LIFT','seal':'PROVENANCE_SEAL','assert_closure':'ASSERT_CLOSURE','emit_receipt':'EMIT_RECEIPT'
}
TYPES={
'FABRIC_MOUNT':'FABRIC','FABRIC_ALLOC':'REGION','GEO_INSTANTIATE':'GEOMETRIC','GEO_FORK':'GEOMETRIC','RELATE':'RELATION','ADMIT':'ADMISSION','TRANSFORM':'GEOMETRIC','INHERIT':'RECEIPT','PORTAL_OPEN':'PORTAL','PORTAL_TRANSPORT':'GEOMETRIC','PORTAL_CLOSE':'RECEIPT','ROAD_BEGIN':'ROAD','ROAD_APPEND':'ROAD','ROAD_CLOSE':'RECEIPT','BRIDGE_SECTOR':'BRIDGE','Q_PREPARE':'QSTATE','Q_SUPERPOSE':'QSTATE','Q_ENTANGLE':'QSTATE','Q_CHANNEL':'QSTATE','Q_MEASURE':'QRESULT','BRANE_LIFT':'M5','PROVENANCE_SEAL':'RECEIPT','ASSERT_CLOSURE':'BOOL','EMIT_RECEIPT':'RECEIPT'
}

def _v(name): return name if isinstance(name,str) and name.startswith('%') else '%'+name

def lower_module(ast):
    nodes=[]; edges=[]; effects=set(); source_map=[]; previous=None
    for idx,st in enumerate(ast.statements,1):
        op=OPS[st.kind]; nid=f'{idx:03d}_{op.lower()}'
        attrs=dict(st.attrs); args=[_v(x) for x in st.args]
        out=_v(st.out) if st.out else None
        typ=coarse_type(st.declared_type) if st.declared_type else TYPES[op]
        n={'id':nid,'op':op,'type':typ}
        if args:n['args']=args
        if out:n['out']=out
        if attrs:n['attrs']=attrs
        nodes.append(n); effects |= effects_for_op(op)
        if previous is not None: edges.append({'from':previous,'to':nid,'kind':'effect_order'})
        previous=nid
        source_map.append({'node':nid,'file':ast.file,'line':st.line,'surface':st.surface})
    mod={
      'ir':'GIR-MODULE','version':'0.1.0','module':ast.module,
      'imports':[{'from':x.module,'symbol':x.symbol,'local':_v(x.local),'type':x.type} for x in ast.imports],
      'exports':[{'symbol':x.local,'value':_v(x.local),'type':x.type} for x in ast.exports],
      'effects':sorted(effects),
      'gir':{'nodes':nodes,'edges':edges},
      'frontend':{'section':'10','source_file':ast.file,'source_map':source_map,'ast_hash':sha256_obj(ast.as_dict())}
    }
    cr=check_module(mod)
    if not cr.ok:
        msg='; '.join(f'{d.code}:{d.message}' for d in cr.diagnostics)
        raise FrontendError(Diagnostic('SEMANTIC_CHECK',msg,ast.file,0))
    return mod,cr
