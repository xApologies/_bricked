from .model import Diagnostic
from .effects import effects_for_op, OP_EFFECTS

FEATURE_BY_OP={
'PORTAL_OPEN':'portal','PORTAL_TRANSPORT':'portal','PORTAL_CLOSE':'portal',
'ROAD_BEGIN':'rainbow_road','ROAD_APPEND':'rainbow_road','ROAD_CLOSE':'rainbow_road',
'BRIDGE_SECTOR':'sector_bridge',
'Q_PREPARE':'quantum_linear','Q_SUPERPOSE':'quantum_linear','Q_ENTANGLE':'quantum_linear','Q_CHANNEL':'quantum_linear','Q_MEASURE':'quantum_linear',
'EMIT_RECEIPT':'provenance_receipts','PROVENANCE_SEAL':'provenance_receipts'
}

def reference_backend_capabilities():
    return {'backend_id':'python-reference-backend','abi':'0.1','ops':sorted(OP_EFFECTS),'effects':sorted(set().union(*OP_EFFECTS.values())), 'sectors':['GENERIC','QFT','GR'], 'features':['portal','rainbow_road','sector_bridge','quantum_linear','provenance_receipts','brane_lift','immutable_fabric_overlay']}

def check_capabilities(gir,manifest):
    ds=[]
    if str(manifest.get('abi'))!='0.1': ds.append(Diagnostic('BACKEND_ABI_MISMATCH',f"backend ABI {manifest.get('abi')} != required 0.1"))
    ops=set(manifest.get('ops',[])); eff=set(manifest.get('effects',[])); sectors=set(x.upper() for x in manifest.get('sectors',[])); features=set(manifest.get('features',[]))
    req_ops={n.get('op') for n in gir.get('nodes',[])}
    for x in sorted(req_ops-ops): ds.append(Diagnostic('CAPABILITY_OP_MISSING',f'backend missing op {x}'))
    req_eff=set()
    for x in req_ops: req_eff |= effects_for_op(x)
    for x in sorted(req_eff-eff): ds.append(Diagnostic('CAPABILITY_EFFECT_MISSING',f'backend missing effect {x}'))
    req_sec=set()
    for n in gir.get('nodes',[]):
        if n.get('op')=='PORTAL_OPEN': req_sec.add(str(n.get('attrs',{}).get('sector','GENERIC')).upper())
        if n.get('op')=='BRIDGE_SECTOR':
            req_sec.add(str(n.get('attrs',{}).get('from','')).upper()); req_sec.add(str(n.get('attrs',{}).get('to','')).upper())
    req_sec.discard('')
    for x in sorted(req_sec-sectors): ds.append(Diagnostic('CAPABILITY_SECTOR_MISSING',f'backend missing sector {x}'))
    req_features={FEATURE_BY_OP[x] for x in req_ops if x in FEATURE_BY_OP}
    if any(n.get('op')=='BRANE_LIFT' for n in gir.get('nodes',[])): req_features.add('brane_lift')
    for x in sorted(req_features-features): ds.append(Diagnostic('CAPABILITY_FEATURE_MISSING',f'backend missing feature {x}'))
    return {'ok':not ds,'diagnostics':[d.as_dict() for d in ds],'required_ops':sorted(req_ops),'required_effects':sorted(req_eff),'required_sectors':sorted(req_sec),'required_features':sorted(req_features)}
