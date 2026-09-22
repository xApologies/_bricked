from dataclasses import dataclass,field
from enum import Enum
from typing import Optional

class StateKind(str,Enum):
    CLASSICAL='CLASSICAL'; PURE='PURE'; DENSITY='DENSITY'; JOINT='JOINT'; MEASURED='MEASURED'; DECOHERED='DECOHERED'; CONSUMED='CONSUMED'
class OwnershipState(str,Enum): OWNED='OWNED'; MOVED='MOVED'; MEASURED='MEASURED'; CONSUMED='CONSUMED'
class ChannelClass(str,Enum): IDENTITY='IDENTITY'; UNITARY='UNITARY'; ISOMETRIC_REFERENCE='ISOMETRIC_REFERENCE'; CPTP_REFERENCE='CPTP_REFERENCE'; DEPHASING='DEPHASING'; PROJECTIVE='PROJECTIVE'; CLASSICALIZE='CLASSICALIZE'; STRUCTURAL_TRANSDUCTION='STRUCTURAL_TRANSDUCTION'
class Effect(str,Enum): READ_META='READ_META'; SUPERPOSE='SUPERPOSE'; ENTANGLE='ENTANGLE'; UNITARY='UNITARY'; CHANNEL='CHANNEL'; DEPHASE='DEPHASE'; MEASURE='MEASURE'; CLASSICALIZE='CLASSICALIZE'; QFT_PORTAL_TRANSPORT='QFT_PORTAL_TRANSPORT'; STRUCTURAL_TRANSDUCE='STRUCTURAL_TRANSDUCE'; RECOVER='RECOVER'

@dataclass
class QuantumState:
    state_id:str
    kind:str
    basis:list
    amplitudes:list=field(default_factory=list)
    density:list=field(default_factory=list)
    members:list=field(default_factory=list)
    source_instance_id:Optional[str]=None
    canonical_mmo_id:Optional[str]=None
    sector:str='QFT'
    provenance:list=field(default_factory=list)
    metadata:dict=field(default_factory=dict)

@dataclass
class OwnershipRecord:
    state_id:str
    token:str
    owner:str
    status:str='OWNED'
    version:int=0

@dataclass
class QuantumPreservation:
    preserve_norm:bool=True
    preserve_trace:bool=True
    preserve_coherence:bool=False
    preserve_entanglement:bool=False
    min_fidelity:float=0.0
    min_coherence:float=0.0

@dataclass
class QuantumEffectEnvelope:
    state_id:str
    channel_class:str
    channel_id:str
    ownership_token:str
    source_address:dict
    target_address:dict
    preservation:QuantumPreservation=field(default_factory=QuantumPreservation)
    entanglement_relation_ids:list=field(default_factory=list)
    metadata:dict=field(default_factory=dict)
