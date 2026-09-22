from dataclasses import asdict
import copy
from genesis_portal_engine.model import PortalRequest
from genesis_portal_engine.util import file_sha256
from .model import RoadState,RoadLegPlan,RainbowRoadPlan,RainbowRoadResult
from .util import digest_obj,now_ns
from .ledger import RoadLedger
from .errors import *
from .audit import audit_road_receipt

class RainbowRoadEngine:
    def __init__(self,portal_engine,road_capacity_manager,output_dir,ledger_path=None,registry=None):
        self.portal=portal_engine; self.capacity=road_capacity_manager; self.output_dir=__import__('pathlib').Path(output_dir); self.output_dir.mkdir(parents=True,exist_ok=True); self.ledger=RoadLedger(ledger_path or self.output_dir/'RAINBOW_ROAD_LEDGER.jsonl'); self.registry=registry
    def _validate(self,req):
        if not req.waypoints: raise EmptyRoadError('road requires at least one waypoint')
        if req.source_address.sector!=req.sector: raise RoadSectorMismatch('source sector mismatch')
        for a in req.waypoints:
            if a.sector!=req.sector: raise RoadSectorMismatch('waypoint sector mismatch')
        if req.preservation is None: raise RoadCompositionError('preservation contract required')
    def _portal_req(self,req,inst,chain,src,tgt,expected=None):
        return PortalRequest(inst,chain,src,tgt,sector=req.sector,transport_mode='RE_REALIZE',preservation=req.preservation,resolution_required=req.resolution_required,bandwidth_required=req.bandwidth_required,capacity_units_required=req.capacity_units_required,chirality_class=req.chirality_class,residue_class=req.residue_class,route_policy=req.route_policy,closure_target='TARGET_ADDRESS',expected_source_content_root=expected,metadata={'rainbow_road':req.road_name,**req.metadata})
    def plan(self,req):
        self._validate(req)
        first=self._portal_req(req,req.source_instance,req.source_segment_chain,req.source_address,req.waypoints[0])
        ch,rr=self.portal._source_roots(first)
        legs=[]; src=req.source_address; holds={}; total=0.; mr=1e99; mb=1e99; colors=[]; edges=[]
        for i,tgt in enumerate(req.waypoints):
            pr=self._portal_req(req,req.source_instance,req.source_segment_chain,src,tgt)
            cp=self.portal.graph.select(pr,self.capacity.base.available)
            legs.append(RoadLegPlan(i,asdict(src),asdict(tgt),asdict(cp)))
            total+=cp.total_cost; mr=min(mr,cp.min_resolution); mb=min(mb,cp.min_bandwidth); colors.extend(cp.color_trajectory); edges.extend(cp.edge_ids)
            for eid in cp.edge_ids: holds[eid]=max(holds.get(eid,0),req.capacity_units_required)
            src=tgt
        canonical={'source_instance':req.source_instance['instance_id'],'source_content_root':ch['content_root'],'source_address':asdict(req.source_address),'waypoints':[asdict(x) for x in req.waypoints],'sector':req.sector,'chirality_class':req.chirality_class,'residue_class':req.residue_class,'preservation':asdict(req.preservation),'R':req.resolution_required,'B':req.bandwidth_required,'capacity':req.capacity_units_required,'corridors':[x.corridor for x in legs]}
        road_id=digest_obj(canonical)
        witness=digest_obj({'planned_edges':edges,'colors':colors,'chirality_class':req.chirality_class,'sector':req.sector,'source_root':ch['content_root']})
        p=RainbowRoadPlan(road_id,req.road_name,req.source_instance['instance_id'],ch['content_root'],rr,asdict(req.source_address),[asdict(x) for x in req.waypoints],req.sector,req.chirality_class,req.residue_class,asdict(req.preservation),[asdict(x) for x in legs],holds,total,mr,mb,colors,witness,[RoadState.DECLARED.value,RoadState.PREFLIGHTED.value])
        if self.registry:self.registry.register_plan(p,req.road_name)
        return p
    def execute(self,req):
        plan=self.plan(req); completed=[]; current=req.source_instance; chain=list(req.source_segment_chain); lifecycle=list(plan.lifecycle); source_hashes={str(p):file_sha256(p) for p in chain}; fabric_hash=file_sha256(self.portal.fabric.path)
        try:
            self.capacity.begin_road(plan.road_id,plan.hold_requirements); lifecycle.append(RoadState.BUS_RESERVED.value); lifecycle.append(RoadState.RUNNING.value)
            for lp in plan.leg_plans:
                from genesis_portal_engine.model import PortalAddress
                src=PortalAddress(**lp['source_address']); tgt=PortalAddress(**lp['target_address'])
                expected=plan.source_content_root if not completed else completed[-1].receipt['destination_content_root']
                pr=self._portal_req(req,current,chain,src,tgt,expected)
                res=self.portal.execute(pr)
                if res.receipt['corridor']['edge_ids']!=lp['corridor']['edge_ids']: raise RoadRouteDrift(f"leg {lp['index']} route drift")
                completed.append(res); current=res.destination_instance; chain=list(current.get('segment_chain',[res.destination_segment_path])); lifecycle.append(RoadState.LEG_CLOSED.value)
            lifecycle.append(RoadState.END_TO_END_AUDIT.value)
            if req.require_end_to_end_content_identity and completed[-1].receipt['destination_content_root']!=plan.source_content_root: raise RoadClosureError('end-to-end content root changed')
            if req.preservation.preserve_canonical_mmo and current.get('canonical_mmo_id')!=req.source_instance.get('canonical_mmo_id'): raise RoadClosureError('canonical MMO changed')
            if req.preservation.preserve_representation and current.get('representation_id')!=req.source_instance.get('representation_id'): raise RoadClosureError('representation changed')
            if {str(p):file_sha256(p) for p in req.source_segment_chain}!=source_hashes: raise RoadClosureError('source segments mutated')
            if file_sha256(self.portal.fabric.path)!=fabric_hash: raise RoadClosureError('base fabric mutated')
            portal_receipts=[x.receipt for x in completed]; edges=[e for p in portal_receipts for e in p['corridor']['edge_ids']]; colors=[c for p in portal_receipts for c in p['corridor']['color_trajectory']]
            witness=digest_obj({'portal_ids':[p['portal_id'] for p in portal_receipts],'edges':edges,'colors':colors,'chirality_class':req.chirality_class,'sector':req.sector,'source_root':plan.source_content_root,'final_root':portal_receipts[-1]['destination_content_root']})
            lifecycle.append(RoadState.CLOSED.value)
            receipt={'kind':'RAINBOW_ROAD_CLOSURE_RECEIPT','status':'CLOSED','road_id':plan.road_id,'road_name':plan.road_name,'source_instance_id':req.source_instance['instance_id'],'final_instance_id':current['instance_id'],'canonical_mmo_id':current.get('canonical_mmo_id'),'representation_id':current.get('representation_id'),'source_address':plan.source_address,'waypoints':plan.waypoints,'sector':plan.sector,'chirality_class':plan.chirality_class,'residue_class':plan.residue_class,'portal_ids':[p['portal_id'] for p in portal_receipts],'portal_receipts':portal_receipts,'source_content_root':plan.source_content_root,'final_content_root':portal_receipts[-1]['destination_content_root'],'source_residue_root':plan.source_residue_root,'final_residue_root':portal_receipts[-1]['destination_residue_root'],'road_min_resolution':plan.min_resolution,'road_min_bandwidth':plan.min_bandwidth,'total_cost':plan.total_cost,'rainbow_trajectory':colors,'corridor_edge_trajectory':edges,'transport_holonomy_witness':witness,'planned_transport_witness':plan.transport_holonomy_witness,'intermediate_instance_ids':[p['destination_instance_id'] for p in portal_receipts[:-1]],'lifecycle':list(lifecycle),'base_fabric_sha256':fabric_hash,'timestamp_ns':now_ns()}
            audit=audit_road_receipt(receipt); receipt['audit']=audit
            if not audit['pass']: raise RoadClosureError('road receipt audit failed '+str(audit['findings']))
            final=copy.deepcopy(current); final['history']=list(final.get('history',[]))+[{'event':'RAINBOW_ROAD_CLOSED','road_id':plan.road_id,'portal_ids':receipt['portal_ids'],'timestamp_ns':now_ns()}]; final['provenance']=list(final.get('provenance',[]))+[{'rainbow_road_receipt':receipt}]
            bm=copy.deepcopy(final.get('brane_m5',{})); bm.setdefault('D',{})['road_id']=plan.road_id; bm['D']['portal_ids']=receipt['portal_ids']; bm['D']['waypoint_domains']=[a['domain_id'] for a in plan.waypoints]; bm.setdefault('Chi',{})['transport_holonomy_witness']=witness; bm['Chi']['road_sector']=plan.sector; bm.setdefault('R',{})['rainbow_road_closed']=True; bm.setdefault('P',{})['rainbow_road_receipt']=receipt; final['brane_m5']=bm
            lifecycle.append(RoadState.INHERITED.value); receipt['lifecycle']=list(lifecycle); self.ledger.append(receipt); self.capacity.end_road(plan.road_id,'CLOSED')
            out=self.output_dir/(plan.road_id+'.road.json'); out.write_text(__import__('json').dumps({'plan':asdict(plan),'receipt':receipt,'final_instance':final},indent=2,sort_keys=True),encoding='utf-8')
            return RainbowRoadResult(final,asdict(plan),receipt,completed)
        except Exception as exc:
            partial=bool(completed); status=RoadState.FAILED_PARTIAL.value if partial else RoadState.FAILED.value
            fail={'kind':'RAINBOW_ROAD_FAILURE_RECEIPT','status':status,'road_id':plan.road_id,'road_name':plan.road_name,'source_instance_id':req.source_instance['instance_id'],'closed_portal_ids':[x.receipt['portal_id'] for x in completed],'closed_portal_receipts':[x.receipt for x in completed],'completion_frontier':(completed[-1].receipt['target_address'] if completed else plan.source_address),'failed_leg_index':len(completed),'error_type':type(exc).__name__,'error':str(exc),'lifecycle':lifecycle+[status],'timestamp_ns':now_ns()}
            self.ledger.append(fail)
            try:self.capacity.end_road(plan.road_id,'FAILED')
            except:pass
            raise RoadExecutionError(str(exc),fail) from exc
