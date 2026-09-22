import math,copy
from .model import QuantumState,StateKind
from .util import digest,cpair,cfrom,now_ns
from .linalg import density_from_state,trace,purity,coherence_l1
from .errors import NormalizationError,StateValidationError

class StateFactory:
    @staticmethod
    def pure(basis,amps,source_instance_id=None,canonical_mmo_id=None,members=None,metadata=None):
        if len(basis)!=len(amps) or not basis: raise StateValidationError('basis/amplitude mismatch')
        amps=[complex(x) for x in amps]; norm=sum(abs(x)**2 for x in amps)
        if norm<=0: raise NormalizationError('zero norm')
        amps=[x/math.sqrt(norm) for x in amps]
        payload={'kind':'PURE','basis':list(basis),'amps':[cpair(x) for x in amps],'source':source_instance_id,'mmo':canonical_mmo_id,'members':members or [],'metadata':metadata or {}}
        sid=digest(payload)
        kind=StateKind.JOINT.value if members and len(members)>1 else StateKind.PURE.value
        return QuantumState(sid,kind,list(basis),[cpair(x) for x in amps],[],list(members or []),source_instance_id,canonical_mmo_id,'QFT',[{'event':'STATE_CREATED','timestamp_ns':now_ns()}],metadata or {})
    @staticmethod
    def density(basis,rho,source_instance_id=None,canonical_mmo_id=None,members=None,kind='DENSITY',metadata=None):
        n=len(basis)
        if len(rho)!=n or any(len(r)!=n for r in rho): raise StateValidationError('density shape')
        rr=[[complex(x) for x in row] for row in rho]
        tr=trace(rr)
        if abs(tr-1)>1e-8: raise NormalizationError('density trace != 1')
        for i in range(n):
            for j in range(n):
                if abs(rr[i][j]-rr[j][i].conjugate())>1e-8: raise StateValidationError('density not Hermitian')
        payload={'kind':kind,'basis':list(basis),'rho':[[cpair(x) for x in row] for row in rr],'source':source_instance_id,'mmo':canonical_mmo_id,'members':members or [],'metadata':metadata or {}}
        sid=digest(payload)
        return QuantumState(sid,kind,list(basis),[],[[cpair(x) for x in row] for row in rr],list(members or []),source_instance_id,canonical_mmo_id,'QFT',[{'event':'DENSITY_CREATED','timestamp_ns':now_ns()}],metadata or {})

def ampvec(state): return [cfrom(x) for x in state.amplitudes]
def rhomat(state):
    if state.density: return [[cfrom(x) for x in row] for row in state.density]
    return density_from_state(ampvec(state))
def diagnostics(state):
    rho=rhomat(state)
    norm=sum(abs(x)**2 for x in ampvec(state)) if state.amplitudes else None
    return {'state_id':state.state_id,'kind':state.kind,'norm':norm,'trace':float(trace(rho).real),'purity':purity(rho),'coherence_l1':coherence_l1(rho),'member_count':len(state.members)}
def pure_fidelity(a,b):
    av,bv=ampvec(a),ampvec(b)
    if len(av)!=len(bv): raise StateValidationError('fidelity dimension')
    return float(abs(sum(x.conjugate()*y for x,y in zip(av,bv)))**2)
