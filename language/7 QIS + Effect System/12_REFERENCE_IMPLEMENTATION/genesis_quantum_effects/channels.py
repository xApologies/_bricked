import math
from .model import ChannelClass
from .state import StateFactory,ampvec,rhomat,diagnostics
from .linalg import matvec,matmul,dagger,add,scalar,validate_kraus,is_unitary,trace
from .errors import ChannelValidationError
from .util import digest,now_ns

class QuantumChannel:
    def __init__(self,channel_class,operators=None,name=None):
        self.channel_class=str(channel_class.value if hasattr(channel_class,'value') else channel_class); self.operators=operators or []; self.name=name or self.channel_class
        self.channel_id=digest({'class':self.channel_class,'ops':[[[[float(complex(x).real),float(complex(x).imag)] for x in row] for row in op] for op in self.operators],'name':self.name})
        self.validate()
    def validate(self):
        if self.channel_class==ChannelClass.UNITARY.value:
            if len(self.operators)!=1 or not is_unitary(self.operators[0]): raise ChannelValidationError('invalid unitary')
        elif self.channel_class in (ChannelClass.CPTP_REFERENCE.value,ChannelClass.DEPHASING.value): validate_kraus(self.operators)
        elif self.channel_class==ChannelClass.IDENTITY.value: pass
        return True
    def apply(self,state):
        if self.channel_class==ChannelClass.IDENTITY.value:
            if state.amplitudes: return StateFactory.pure(state.basis,ampvec(state),state.source_instance_id,state.canonical_mmo_id,state.members,{'channel_id':self.channel_id,'parent_state_id':state.state_id,'identity_successor':True})
            return StateFactory.density(state.basis,rhomat(state),state.source_instance_id,state.canonical_mmo_id,state.members,state.kind,{'channel_id':self.channel_id,'parent_state_id':state.state_id,'identity_successor':True})
        if self.channel_class==ChannelClass.UNITARY.value and state.amplitudes:
            out=matvec(self.operators[0],ampvec(state)); return StateFactory.pure(state.basis,out,state.source_instance_id,state.canonical_mmo_id,state.members,{'channel_id':self.channel_id,'parent_state_id':state.state_id})
        rho=rhomat(state); n=len(rho); acc=[[0j for _ in range(n)] for _ in range(n)]
        for K in self.operators: acc=add(acc,matmul(matmul(K,rho),dagger(K)))
        kind='DECOHERED' if self.channel_class==ChannelClass.DEPHASING.value else 'DENSITY'
        return StateFactory.density(state.basis,acc,state.source_instance_id,state.canonical_mmo_id,state.members,kind,{'channel_id':self.channel_id,'parent_state_id':state.state_id})

def identity_channel(): return QuantumChannel(ChannelClass.IDENTITY,[], 'IDENTITY')
def hadamard_channel():
    s=1/math.sqrt(2); return QuantumChannel(ChannelClass.UNITARY,[[[s,s],[s,-s]]],'H')
def phase_flip_channel(): return QuantumChannel(ChannelClass.UNITARY,[[[1,0],[0,-1]]],'Z')
def dephasing_channel(p=0.5):
    if p<0 or p>1: raise ChannelValidationError('p range')
    a=math.sqrt(1-p); b=math.sqrt(p)
    I=[[a,0],[0,a]]; Z=[[b,0],[0,-b]]
    return QuantumChannel(ChannelClass.DEPHASING,[I,Z],f'DEPHASE({p})')
