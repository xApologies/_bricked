from enum import Enum
from dataclasses import dataclass

class Effect(str,Enum):
    READ='READ'; ADMISSIBILITY_WRITE='ADMISSIBILITY_WRITE'; CHIRALITY_WRITE='CHIRALITY_WRITE'; OCCUPANCY_WRITE='OCCUPANCY_WRITE'
    PERSISTENCE_WRITE='PERSISTENCE_WRITE'; LOCALITY_WRITE='LOCALITY_WRITE'; TRANSLATION_WRITE='TRANSLATION_WRITE'; FLAGS_WRITE='FLAGS_WRITE'
    ADJACENCY_WRITE='ADJACENCY_WRITE'; LINEAGE_WRITE='LINEAGE_WRITE'; IDENTITY_TAG_WRITE='IDENTITY_TAG_WRITE'

@dataclass(frozen=True)
class CapabilityProfile:
    name:str
    allowed:frozenset
    def admits(self,effects): return set(effects).issubset(self.allowed)

BASE={Effect.READ,Effect.ADMISSIBILITY_WRITE,Effect.PERSISTENCE_WRITE,Effect.LOCALITY_WRITE,Effect.TRANSLATION_WRITE,Effect.FLAGS_WRITE,Effect.ADJACENCY_WRITE,Effect.LINEAGE_WRITE}
CAPABILITIES={
 'GENERIC_LIVE':CapabilityProfile('GENERIC_LIVE',frozenset(BASE|{Effect.CHIRALITY_WRITE,Effect.OCCUPANCY_WRITE})),
 'PIPELINE_T':CapabilityProfile('PIPELINE_T',frozenset(BASE|{Effect.CHIRALITY_WRITE,Effect.OCCUPANCY_WRITE})),
 'PIPELINE_R':CapabilityProfile('PIPELINE_R',frozenset(BASE)),
 'PROJECTION_ONLY':CapabilityProfile('PROJECTION_ONLY',frozenset({Effect.READ})),
 'ADMIN_DERIVATION':CapabilityProfile('ADMIN_DERIVATION',frozenset(set(Effect))),
}
