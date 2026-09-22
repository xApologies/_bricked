from dataclasses import dataclass
from .errors import BridgeQuantumBoundaryError
from .util import digest,now_ns

@dataclass
class StructuralInvariantCapsule:
    canonical_mmo_id:str
    source_instance_id:str
    content_root:str
    residue_root:str
    representation_id:str
    common_ancestry_witness:str
    provenance_refs:list

class QuantumBridgePolicy:
    def require_structural_only(self,state,bridge_receipt):
        if state.kind in ('PURE','JOINT','DENSITY','DECOHERED'):
            return {'admitted':True,'quantum_state_preserved':False,'policy':'STRUCTURAL_ONLY','reason':'Section 06 bridge is not typed as quantum channel'}
        return {'admitted':True,'quantum_state_preserved':False,'policy':'STRUCTURAL_ONLY'}
    def assert_preserve_quantum(self,state,bridge_receipt):
        raise BridgeQuantumBoundaryError('QFT/GR structural bridge does not establish quantum-coherence preservation')
    def capsule(self,instance,bridge_receipt):
        ca=bridge_receipt.get('common_ancestry',{})
        return StructuralInvariantCapsule(instance.get('canonical_mmo_id'),instance.get('instance_id'),bridge_receipt.get('source_content_root'),bridge_receipt.get('source_residue_root'),instance.get('representation_id'),ca.get('fabric_witness_id') or bridge_receipt.get('fabric_witness_id'),[bridge_receipt.get('bridge_id')])
