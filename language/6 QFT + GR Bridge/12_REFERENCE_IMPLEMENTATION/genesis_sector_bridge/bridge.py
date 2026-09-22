from dataclasses import asdict
import copy
from genesis_portal_engine.model import PortalAddress
from .model import BridgePlan,BridgeResult,BridgeState
from .representation import RepresentationEngine
from .ancestry import common_ancestry
from .audit import audit_bridge_receipt
from .brane import BridgeBraneAdapter
from .ledger import BridgeLedger
from .errors import *
from .util import digest_obj,file_sha256,now_ns

class SectorBridgeEngine:
    SUPPORTED={('QFT','GR'),('GR','QFT')}
    def __init__(self,fabric,output_dir,ledger_path=None):
        from pathlib import Path
        self.fabric=fabric; self.output_dir=Path(output_dir); self.output_dir.mkdir(parents=True,exist_ok=True); self.ledger=BridgeLedger(ledger_path or self.output_dir/'BRIDGE_LEDGER.jsonl'); self.reps=RepresentationEngine(fabric)
    def _validate(self,req):
        if req.source_sector==req.target_sector: raise UnsupportedSectorPair('bridge requires sector change')
        if (req.source_sector,req.target_sector) not in self.SUPPORTED: raise UnsupportedSectorPair(str((req.source_sector,req.target_sector)))
        if req.address.sector!=req.source_sector: raise UnsupportedSectorPair('source address sector mismatch')
    def plan(self,req):
        self._validate(req); lifecycle=[BridgeState.DECLARED.value,BridgeState.CHARACTERIZED.value]
        prof_s=req.projection_profile_qft if req.source_sector=='QFT' else req.projection_profile_gr
        prof_t=req.projection_profile_qft if req.target_sector=='QFT' else req.projection_profile_gr
        s=self.reps.read(req.source_instance,req.source_segment_chain,req.address,req.source_sector,prof_s)
        lifecycle.append(BridgeState.SOURCE_VIEW.value)
        tgt_addr=PortalAddress(req.address.domain_id,req.address.boundary_id,req.address.logical_location,req.target_sector,req.address.recursive_order,req.address.fabric_tag)
        t=self.reps.read(req.source_instance,req.source_segment_chain,tgt_addr,req.target_sector,prof_t)
        lifecycle.append(BridgeState.TARGET_VIEW.value)
        ca=common_ancestry(s,t); lifecycle.append(BridgeState.ANCESTRY_VERIFIED.value)
        bridge_id=digest_obj({'source_view':s.representation_view_id,'target_view':t.representation_view_id,'relation':ca['relation_id'],'preservation':asdict(req.preservation),'metadata':req.metadata})
        return BridgePlan(bridge_id,req.source_sector,req.target_sector,req.source_instance['instance_id'],asdict(req.address),asdict(s),asdict(t),s.fabric_witness_id,ca['relation_id'],asdict(req.preservation),lifecycle)
    def execute(self,req):
        source_hashes={str(p):file_sha256(p) for p in req.source_segment_chain}; fabric_hash=file_sha256(self.fabric.path)
        try:
            plan=self.plan(req); s=type('R',(),plan.source_view); t=type('R',(),plan.target_view)
            # reconstruct relation using dicts to avoid type assumptions
            ca={'kind':'R_QG_COMMON_ANCESTRY','relation_id':plan.common_ancestry_relation_id,'admitted':True,'fabric_witness_id':plan.fabric_witness_id,'qft_view_id':plan.source_view['representation_view_id'] if req.source_sector=='QFT' else plan.target_view['representation_view_id'],'gr_view_id':plan.target_view['representation_view_id'] if req.target_sector=='GR' else plan.source_view['representation_view_id'],'canonical_mmo_id':req.source_instance.get('canonical_mmo_id'),'content_root':plan.source_view['content_root'],'residue_root':plan.source_view['residue_root']}
            if req.preservation.preserve_content_root and plan.source_view['content_root']!=plan.target_view['content_root']: raise BridgeContentDrift('content')
            if req.preservation.preserve_residue_root and plan.source_view['residue_root']!=plan.target_view['residue_root']: raise BridgeResidueDrift('residue')
            if {str(p):file_sha256(p) for p in req.source_segment_chain}!=source_hashes: raise BridgeSourceMutated('segments')
            if file_sha256(self.fabric.path)!=fabric_hash: raise BridgeFabricMutated('fabric')
            plan.lifecycle.append(BridgeState.CLOSED.value)
            receipt={'kind':'SECTOR_BRIDGE_CLOSURE_RECEIPT','status':'CLOSED','bridge_id':plan.bridge_id,'source_sector':req.source_sector,'target_sector':req.target_sector,'source_instance_id':req.source_instance['instance_id'],'canonical_mmo_id':req.source_instance.get('canonical_mmo_id'),'source_representation_id':req.source_instance.get('representation_id'),'address':plan.address,'source_representation_view_id':plan.source_view['representation_view_id'],'target_representation_view_id':plan.target_view['representation_view_id'],'fabric_witness_id':plan.fabric_witness_id,'common_ancestry':ca,'source_content_root':plan.source_view['content_root'],'target_content_root':plan.target_view['content_root'],'source_residue_root':plan.source_view['residue_root'],'target_residue_root':plan.target_view['residue_root'],'preservation':plan.preservation,'source_segment_hashes':source_hashes,'base_fabric_sha256':fabric_hash,'physics_status':'SOFTWARE_REFERENCE_TRANSDUCTION','lifecycle':list(plan.lifecycle),'timestamp_ns':now_ns()}
            audit=audit_bridge_receipt(receipt); receipt['audit']=audit
            if not audit['pass']: raise SectorBridgeError('bridge audit '+str(audit['findings']))
            out=copy.deepcopy(req.source_instance); out['history']=list(out.get('history',[]))+[{'event':'SECTOR_BRIDGE_CLOSED','bridge_id':plan.bridge_id,'source_sector':req.source_sector,'target_sector':req.target_sector,'timestamp_ns':now_ns()}]; out['provenance']=list(out.get('provenance',[]))+[{'sector_bridge_receipt':receipt}]; out['current_sector']=req.target_sector; out['brane_m5']=BridgeBraneAdapter().adapt(out,receipt)
            plan.lifecycle.append(BridgeState.INHERITED.value); receipt['lifecycle']=list(plan.lifecycle); self.ledger.append(receipt)
            target_address=PortalAddress(req.address.domain_id,req.address.boundary_id,req.address.logical_location,req.target_sector,req.address.recursive_order,req.address.fabric_tag)
            import json
            (self.output_dir/(plan.bridge_id+'.bridge.json')).write_text(json.dumps({'plan':asdict(plan),'receipt':receipt,'instance':out},indent=2,sort_keys=True),encoding='utf-8')
            return BridgeResult(out,target_address,plan.source_view,plan.target_view,asdict(plan),receipt)
        except Exception as exc:
            fail={'kind':'SECTOR_BRIDGE_FAILURE_RECEIPT','status':'FAILED','source_instance_id':req.source_instance.get('instance_id'),'source_sector':req.source_sector,'target_sector':req.target_sector,'error_type':type(exc).__name__,'error':str(exc),'timestamp_ns':now_ns()}; self.ledger.append(fail); raise
