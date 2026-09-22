import random
from .state import ampvec,StateFactory
from .util import now_ns,digest
from .errors import MeasurementError

class MeasurementEngine:
    def __init__(self,ownership): self.ownership=ownership
    def measure_basis(self,state,token,rng=None):
        self.ownership.assert_owned(state.state_id,token)
        if not state.amplitudes: raise MeasurementError('reference basis measurement requires pure state')
        rng=rng or random.Random()
        probs=[abs(x)**2 for x in ampvec(state)]; x=rng.random(); c=0.0; idx=len(probs)-1
        for i,p in enumerate(probs):
            c+=p
            if x<=c: idx=i; break
        out=state.basis[idx]; self.ownership.consume(state.state_id,token,'MEASURED')
        amps=[0j]*len(probs); amps[idx]=1+0j
        post=StateFactory.pure(state.basis,amps,state.source_instance_id,state.canonical_mmo_id,state.members,{'measurement_parent':state.state_id,'outcome':out}); post.kind='MEASURED'
        rec={'kind':'MEASUREMENT_RECEIPT','measurement_id':digest({'state':state.state_id,'outcome':out,'index':idx}),'source_state_id':state.state_id,'post_state_id':post.state_id,'outcome':out,'outcome_index':idx,'probability':probs[idx],'classical_result':True,'timestamp_ns':now_ns()}
        return out,post,rec
