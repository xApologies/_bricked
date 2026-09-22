from .state import diagnostics,pure_fidelity
from .entanglement import is_entangled_reference

def audit_transition(source,target,preservation):
    a,b=diagnostics(source),diagnostics(target); findings=[]
    if preservation.preserve_norm and source.amplitudes and target.amplitudes and abs((a['norm'] or 0)-(b['norm'] or 0))>1e-8: findings.append('norm drift')
    if preservation.preserve_trace and abs(a['trace']-b['trace'])>1e-8: findings.append('trace drift')
    if preservation.preserve_coherence and b['coherence_l1']+1e-8 < max(a['coherence_l1'],preservation.min_coherence): findings.append('coherence below preservation')
    fidelity=None
    if source.amplitudes and target.amplitudes and len(source.amplitudes)==len(target.amplitudes):
        fidelity=pure_fidelity(source,target)
        if fidelity+1e-8 < preservation.min_fidelity: findings.append('fidelity below threshold')
    if preservation.preserve_entanglement and is_entangled_reference(source) and not is_entangled_reference(target): findings.append('entanglement lost')
    return {'pass':not findings,'findings':findings,'source':a,'target':b,'fidelity':fidelity}
