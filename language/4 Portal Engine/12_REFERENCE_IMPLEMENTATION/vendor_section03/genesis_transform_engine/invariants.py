from .errors import InvariantViolation

FIELDS={'occupancy_pattern':'preserve_occupancy','complement_pattern':'preserve_occupancy','handedness':'preserve_handedness','chi':'preserve_chi','sigma':'preserve_sigma','rho':'preserve_rho','lambda_':'preserve_lambda','tau':'preserve_tau','adjacency_index':'preserve_adjacency','identity_tag':'preserve_identity_tags'}

def check_invariants(parent_inst,child_meta,changed,parent_get,child_get,contract):
    results=[]
    def chk(name,ok):
        results.append({'invariant':name,'pass':bool(ok)})
        if not ok: raise InvariantViolation(name)
    if contract.preserve_canonical_mmo: chk('canonical_mmo_id',parent_inst['canonical_mmo_id']==child_meta['canonical_mmo_id'])
    if contract.preserve_fabric_region: chk('fabric_region',parent_inst['region']==child_meta['region'] and parent_inst['fabric_tag']==child_meta['fabric_tag'])
    if contract.require_no_changes: chk('read_only_no_change',len(changed)==0)
    for field,attr in FIELDS.items():
        if getattr(contract,attr):
            ok=all(getattr(parent_get(i),field)==getattr(child_get(i),field) for i in changed)
            chk(field,ok)
    return results
