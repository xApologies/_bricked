from dataclasses import asdict
from genesis_portal_engine.model import PreservationContract
from genesis_portal_engine.residue import residue_root,characterize
from genesis_transform_engine.view import TransformView
from .model import SectorRepresentation
from .util import digest_obj

class RepresentationEngine:
    def __init__(self,fabric): self.fabric=fabric
    def characterize(self,instance,chain,fields=None):
        fields=fields or ['__FULL_CELL__']
        # Sections 03-05 already carry a verified post-state root in the BRANE lift.
        # For full-cell bridge readout this is an admissible cache: Bridge does not change
        # cells and re-verifies source files/fabric hashes separately. Synthetic/legacy
        # objects without the cache fall back to a full TransformView scan.
        cached=(instance.get('brane_m5',{}).get('Chi',{}).get('post_state_root') or instance.get('brane_m5',{}).get('Chi',{}).get('content_root') or
                instance.get('brane_m5',{}).get('P',{}).get('transformation_receipt',{}).get('post_state_root'))
        if cached and fields==['__FULL_CELL__']:
            return {'content_root':cached,'cache':'BRANE_POST_STATE_ROOT'},cached
        v=TransformView(self.fabric,chain)
        try:
            ch=characterize(v,instance); rr=residue_root(v,instance['region']['start'],instance['region']['count'],fields)
        finally:v.close()
        return ch,rr
    def fabric_witness(self,instance,content_root,residue_root):
        return digest_obj({'canonical_mmo_id':instance.get('canonical_mmo_id'),'instance_id':instance.get('instance_id'),'source_representation_id':instance.get('representation_id'),'fabric_tag':instance.get('fabric_tag'),'region':instance.get('region'),'content_root':content_root,'residue_root':residue_root})
    def read(self,instance,chain,address,sector,profile='REFERENCE',residue_fields=None):
        ch,rr=self.characterize(instance,chain,residue_fields); fw=self.fabric_witness(instance,ch['content_root'],rr)
        common={'source_instance_id':instance['instance_id'],'canonical_mmo_id':instance.get('canonical_mmo_id'),'source_representation_id':instance.get('representation_id'),'content_root':ch['content_root'],'residue_root':rr,'fabric_witness_id':fw,'address':asdict(address),'projection_profile':profile,'invariants':{'canonical_mmo_id':instance.get('canonical_mmo_id'),'content_root':ch['content_root'],'residue_root':rr}}
        if sector=='QFT':
            payload={'state_kind':'FIELD_HANDOFF_DESCRIPTOR','coherence':'UNSPECIFIED','superposition':'UNSPECIFIED','entanglement_refs':[],'measurement':'UNSPECIFIED','channel_class':'UNSPECIFIED','canonical_q_handoff':'REFERENCE_ONLY'}
        elif sector=='GR':
            payload={'manifold_class':instance.get('mapping_profile','GEOMETRIC'),'boundary_class':'REFERENCE_ONLY','topology_witness':digest_obj({'content_root':ch['content_root'],'region':instance.get('region')}),'orientation_history':'REFERENCE_ONLY','connection_status':'OPEN_TYPING','curvature_status':'OPEN_TYPING','metric_readout_status':'REFERENCE_ONLY','holonomy_witnesses':[]}
        else: raise ValueError('unsupported sector '+str(sector))
        rid=digest_obj({'fabric_witness_id':fw,'sector':sector,'profile':profile,'address':asdict(address)})
        return SectorRepresentation(rid,sector,payload=payload,physics_status='SOFTWARE_REFERENCE_READOUT',**common)
