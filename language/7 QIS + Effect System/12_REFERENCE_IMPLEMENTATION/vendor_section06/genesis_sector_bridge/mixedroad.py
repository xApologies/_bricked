from dataclasses import asdict
import copy
from genesis_portal_engine.model import PortalRequest,PortalAddress
from .model import MixedActionPlan,MixedRoadPlan,MixedRoadResult,MixedRoadState,BridgeRequest
from .util import digest_obj,file_sha256,now_ns
from .audit import audit_mixed_road_receipt
from .ledger import BridgeLedger
from .errors import *

class MixedSectorRoadEngine:
    def __init__(self,portal_engine,bridge_engine,road_capacity_manager,output_dir,ledger_path=None):
        from pathlib import Path
        self.portal=portal_engine; self.bridge=bridge_engine; self.capacity=road_capacity_manager; self.output_dir=Path(output_dir); self.output_dir.mkdir(parents=True,exist_ok=True); self.ledger=BridgeLedger(ledger_path or self.output_dir/'MIXED_ROAD_LEDGER.jsonl')
    def _portal_req(self,req,inst,chain,src,tgt,expected=None):
        return PortalRequest(inst,chain,src,tgt,sector=src.sector,transport_mode='RE_REALIZE',preservation=req.preservation,resolution_required=req.resolution_required,bandwidth_required=req.bandwidth_required,capacity_units_required=req.capacity_units_required,chirality_class=req.chirality_class,residue_class=req.residue_class,route_policy=req.route_policy,closure_target='TARGET_ADDRESS',expected_source_content_root=expected,metadata={'mixed_road':req.road_name,**req.metadata})
    def _bridge_req(self,req,inst,chain,address,target_sector):
        return BridgeRequest(inst,chain,address,address.sector,target_sector,req.bridge_preservation,metadata={'mixed_road':req.road_name,**req.metadata})
    def plan(self,req):
        if not req.waypoints: raise MixedRoadPreflightError('requires waypoints')
        first=self._portal_req(req,req.source_instance,req.source_segment_chain,req.source_address,PortalAddress(req.source_address.domain_id,sector=req.source_address.sector))
        ch,rr=self.portal._source_roots(first)
        actions=[]; holds={}; current=req.source_address; colors=[]; sectors=[current.sector]; idx=0
        for target in req.waypoints:
            if target.sector not in ('QFT','GR'): raise MixedRoadPreflightError('mixed road sectors must be QFT or GR')
            if current.sector!=target.sector:
                bp=self.bridge.plan(self._bridge_req(req,req.source_instance,req.source_segment_chain,current,target.sector))
                nextaddr=PortalAddress(current.domain_id,current.boundary_id,current.logical_location,target.sector,current.recursive_order,current.fabric_tag)
                actions.append(MixedActionPlan(idx,'BRIDGE',asdict(current),asdict(nextaddr),{'bridge_plan':asdict(bp)})); idx+=1; current=nextaddr; sectors.append(current.sector)
            if (current.domain_id,current.boundary_id,current.logical_location)!=(target.domain_id,target.boundary_id,target.logical_location):
                pr=self._portal_req(req,req.source_instance,req.source_segment_chain,current,target)
                cp=self.portal.graph.select(pr,self.capacity.base.available)
                actions.append(MixedActionPlan(idx,'PORTAL',asdict(current),asdict(target),{'corridor':asdict(cp)})); idx+=1
                for eid in cp.edge_ids:holds[eid]=max(holds.get(eid,0),req.capacity_units_required)
                colors.extend(cp.color_trajectory); current=target
        canonical={'source_instance_id':req.source_instance['instance_id'],'source_content_root':ch['content_root'],'source_address':asdict(req.source_address),'waypoints':[asdict(x) for x in req.waypoints],'actions':[asdict(x) for x in actions],'preservation':asdict(req.preservation),'bridge_preservation':asdict(req.bridge_preservation)}
        road_id=digest_obj(canonical)
        return MixedRoadPlan(road_id,req.road_name,req.source_instance['instance_id'],ch['content_root'],rr,asdict(req.source_address),[asdict(x) for x in req.waypoints],[asdict(x) for x in actions],holds,sectors,colors,[MixedRoadState.DECLARED.value,MixedRoadState.PREFLIGHTED.value])
    def execute(self,req):
        plan=self.plan(req); lifecycle=list(plan.lifecycle); current=copy.deepcopy(req.source_instance); chain=list(req.source_segment_chain); address=req.source_address; results=[]; source_hashes={str(p):file_sha256(p) for p in req.source_segment_chain}; fabric_hash=file_sha256(self.portal.fabric.path)
        try:
            self.capacity.begin_road(plan.road_id,plan.hold_requirements); lifecycle += [MixedRoadState.BUS_RESERVED.value,MixedRoadState.RUNNING.value]
            for ap in plan.actions:
                if ap['kind']=='BRIDGE':
                    br=self.bridge.execute(self._bridge_req(req,current,chain,address,ap['target_address']['sector'])); current=br.instance; address=br.address; results.append({'kind':'BRIDGE','result':br}); lifecycle.append(MixedRoadState.ACTION_CLOSED.value)
                else:
                    target=PortalAddress(**ap['target_address']); expected=plan.source_content_root if not results else None
                    # source root can be recomputed from current; expected final invariant is audited end-to-end
                    pr=self._portal_req(req,current,chain,address,target,expected if all(x['kind']=='BRIDGE' for x in results) else None)
                    pres=self.portal.execute(pr); current=pres.destination_instance; chain=list(current.get('segment_chain',[pres.destination_segment_path])); address=target; results.append({'kind':'PORTAL','result':pres}); lifecycle.append(MixedRoadState.ACTION_CLOSED.value)
            lifecycle.append(MixedRoadState.END_TO_END_AUDIT.value)
            # recompute final root through Portal engine helper using current address/sector
            probe=self._portal_req(req,current,chain,address,address)
            final_ch,final_rr=self.portal._source_roots(probe)
            if req.require_end_to_end_content_identity and final_ch['content_root']!=plan.source_content_root: raise MixedRoadExecutionError('end-to-end content root changed')
            if {str(p):file_sha256(p) for p in req.source_segment_chain}!=source_hashes: raise MixedRoadExecutionError('source segments mutated')
            if file_sha256(self.portal.fabric.path)!=fabric_hash: raise MixedRoadExecutionError('base fabric mutated')
            action_receipts=[]; bridges=[]; portals=[]; edges=[]; colors=[]; sector_traj=[req.source_address.sector]
            for x in results:
                rr=x['result'].receipt; action_receipts.append(rr)
                if x['kind']=='BRIDGE': bridges.append(rr); sector_traj.append(rr['target_sector'])
                else: portals.append(rr); edges.extend(rr['corridor']['edge_ids']); colors.extend(rr['corridor']['color_trajectory'])
            lifecycle.append(MixedRoadState.CLOSED.value)
            receipt={'kind':'MIXED_SECTOR_RAINBOW_ROAD_CLOSURE_RECEIPT','status':'CLOSED','road_id':plan.road_id,'road_name':plan.road_name,'source_instance_id':req.source_instance['instance_id'],'final_instance_id':current['instance_id'],'canonical_mmo_id':current.get('canonical_mmo_id'),'source_address':plan.source_address,'final_address':asdict(address),'waypoints':plan.waypoints,'actions':plan.actions,'action_receipts':action_receipts,'portal_receipts':portals,'bridge_receipts':bridges,'source_content_root':plan.source_content_root,'final_content_root':final_ch['content_root'],'source_residue_root':plan.source_residue_root,'final_residue_root':final_rr,'sector_trajectory':sector_traj,'corridor_edge_trajectory':edges,'rainbow_trajectory':colors,'base_fabric_sha256':fabric_hash,'physics_status':'SOFTWARE_REFERENCE_MIXED_SECTOR_TRANSPORT','lifecycle':list(lifecycle),'timestamp_ns':now_ns()}
            audit=audit_mixed_road_receipt(receipt); receipt['audit']=audit
            if not audit['pass']: raise MixedRoadExecutionError('mixed road audit '+str(audit['findings']))
            final=copy.deepcopy(current); final['history']=list(final.get('history',[]))+[{'event':'MIXED_SECTOR_RAINBOW_ROAD_CLOSED','road_id':plan.road_id,'timestamp_ns':now_ns()}]; final['provenance']=list(final.get('provenance',[]))+[{'mixed_sector_road_receipt':receipt}]; final['current_sector']=address.sector
            bm=copy.deepcopy(final.get('brane_m5',{})); bm.setdefault('D',{})['mixed_road_id']=plan.road_id; bm['D']['sector_trajectory']=sector_traj; bm.setdefault('Chi',{})['bridge_relation_ids']=[r['common_ancestry']['relation_id'] for r in bridges]; bm['Chi']['current_sector']=address.sector; bm.setdefault('R',{})['mixed_sector_road_closed']=True; bm.setdefault('P',{})['mixed_sector_road_receipt']=receipt; final['brane_m5']=bm
            lifecycle.append(MixedRoadState.INHERITED.value); receipt['lifecycle']=list(lifecycle); self.ledger.append(receipt); self.capacity.end_road(plan.road_id,'CLOSED')
            import json
            (self.output_dir/(plan.road_id+'.mixedroad.json')).write_text(json.dumps({'plan':asdict(plan),'receipt':receipt,'final_instance':final},indent=2,sort_keys=True),encoding='utf-8')
            return MixedRoadResult(final,address,asdict(plan),receipt,results)
        except Exception as exc:
            partial=bool(results); status=MixedRoadState.FAILED_PARTIAL.value if partial else MixedRoadState.FAILED.value
            fail={'kind':'MIXED_SECTOR_RAINBOW_ROAD_FAILURE_RECEIPT','status':status,'road_id':plan.road_id,'closed_action_count':len(results),'closed_action_kinds':[x['kind'] for x in results],'completion_frontier':asdict(address),'error_type':type(exc).__name__,'error':str(exc),'lifecycle':lifecycle+[status],'timestamp_ns':now_ns()}; self.ledger.append(fail)
            try:self.capacity.end_road(plan.road_id,'FAILED')
            except:pass
            if isinstance(exc,MixedRoadError): exc.receipt=fail; raise
            raise MixedRoadExecutionError(str(exc),fail) from exc
