from pathlib import Path
from dataclasses import asdict
import copy,hashlib
from genesis_transform_engine.view import TransformView
from vendor.genesis_geometric_engine.segment import GeometricOverlayWriter,GeometricOverlaySegment
from .model import PortalPlan,PortalResult,PortalState
from .residue import residue_root,characterize
from .util import digest_obj,file_sha256,now_ns
from .brane import PortalBraneAdapter
from .ledger import PortalLedger
from .errors import *

class PortalEngine:
    def __init__(self,fabric,allocator,corridor_graph,capacity_ledger,output_dir,ledger_path=None):
        self.fabric=fabric; self.allocator=allocator; self.graph=corridor_graph; self.capacity=capacity_ledger; self.output_dir=Path(output_dir); self.output_dir.mkdir(parents=True,exist_ok=True); self.ledger=PortalLedger(ledger_path or self.output_dir/'PORTAL_LEDGER.jsonl')
    def _segment_hashes(self,chain): return {str(p):file_sha256(p) for p in chain}
    def _source_roots(self,req):
        v=TransformView(self.fabric,req.source_segment_chain)
        try:
            ch=characterize(v,req.source_instance); rr=residue_root(v,req.source_instance['region']['start'],req.source_instance['region']['count'],req.preservation.fields)
        finally:v.close()
        return ch,rr
    def plan(self,req):
        if req.source_instance['fabric_tag']!=self.fabric.fabric_tag: raise PortalError('source fabric mismatch')
        if req.source_address.sector!=req.sector or req.target_address.sector!=req.sector: raise SectorMismatch('address sector')
        ch,rr=self._source_roots(req)
        if req.expected_source_content_root and req.expected_source_content_root!=ch['content_root']: raise SourceStaleError('source content root mismatch')
        corridor=self.graph.select(req,self.capacity.available)
        canonical={'source':req.source_instance['instance_id'],'source_content_root':ch['content_root'],'source_address':asdict(req.source_address),'target_address':asdict(req.target_address),'sector':req.sector,'corridor':asdict(corridor),'preservation':asdict(req.preservation),'R':req.resolution_required,'B':req.bandwidth_required,'capacity':req.capacity_units_required}
        portal_id=digest_obj(canonical); dest_id=digest_obj({'portal':portal_id,'source':req.source_instance['instance_id']})[:32]
        route_res=self.capacity.reserve(corridor.edge_ids,req.capacity_units_required,portal_id)
        try: dest_res,region=self.allocator.reserve(req.source_instance['region']['count'],dest_id,guard=0)
        except Exception:
            self.capacity.release(route_res,'DESTINATION_ALLOCATION_FAILED'); raise
        lifecycle=[PortalState.DECLARED.value,PortalState.VALIDATED.value,PortalState.CAPACITY_RESERVED.value,PortalState.DESTINATION_RESERVED.value]
        return PortalPlan(portal_id,req.source_instance['instance_id'],dest_id,asdict(req.source_address),asdict(req.target_address),req.sector,req.transport_mode,ch['content_root'],rr,asdict(corridor),route_res,dest_res,{'start':region.start,'count':region.count,'alignment':region.alignment,'guard_before':region.guard_before,'guard_after':region.guard_after},asdict(req.preservation),lifecycle)
    def _destination_meta(self,source,plan,seg_path,seg_hash,receipt):
        d=copy.deepcopy(source); d['instance_id']=plan.destination_instance_id; d['parent_instance_id']=source['instance_id']; d['region']=plan.destination_region; d['segment_path']=str(seg_path); d['segment_sha256']=seg_hash; d['segment_chain']=[str(seg_path)]; d['state']='LIVE'
        d['history']=list(source.get('history',[]))+[{'event':'PORTAL_CLOSED','portal_id':plan.portal_id,'source_instance_id':source['instance_id'],'target_domain':plan.target_address['domain_id'],'timestamp_ns':now_ns()}]
        d['provenance']=list(source.get('provenance',[]))+[{'portal_receipt':receipt}]
        d['brane_m5']=PortalBraneAdapter().adapt(source,d,asdict(plan),receipt); return d
    def execute(self,req):
        plan=None
        source_hashes=self._segment_hashes(req.source_segment_chain); fabric_hash=file_sha256(self.fabric.path)
        try:
            plan=self.plan(req); plan.lifecycle += [PortalState.OPEN.value,PortalState.TRANSFERRING.value]
            source_view=TransformView(self.fabric,req.source_segment_chain)
            ds=plan.destination_region['start']; count=plan.destination_region['count']; ss=req.source_instance['region']['start']
            mmo_digest=hashlib.sha256(req.source_instance['canonical_mmo_id'].encode()).hexdigest(); inst_digest=hashlib.sha256(plan.destination_instance_id.encode()).hexdigest(); src_digest=hashlib.sha256(plan.source_content_root.encode()).hexdigest()
            seg_path=self.output_dir/(plan.destination_instance_id+'.gos'); wr=GeometricOverlayWriter(seg_path,self.fabric.fabric_tag,ds,count,mmo_digest,inst_digest,src_digest)
            try:
                for off in range(count): wr.write(ds+off,source_view.read_index(ss+off))
                payload_hash=wr.finalize()
            except Exception:
                wr.abort(); raise
            finally: source_view.close()
            plan.lifecycle.append(PortalState.ARRIVED.value)
            seg=GeometricOverlaySegment(seg_path,verify=True)
            try:
                class SingleView:
                    def __init__(self,s): self.s=s
                    def read_index(self,i): return self.s.read_index(i)
                dv=SingleView(seg); dest_content=residue_root(dv,ds,count,['__FULL_CELL__']); dest_residue=residue_root(dv,ds,count,req.preservation.fields)
            finally: seg.close()
            if dest_content!=plan.source_content_root: raise TransportIntegrityError('content root changed')
            if dest_residue!=plan.source_residue_root: raise ResidueMismatch('invariant residue changed')
            if plan.corridor['domains'][-1]!=req.target_address.domain_id: raise TargetClosureError('wrong target')
            if req.preservation.preserve_canonical_mmo and not req.source_instance.get('canonical_mmo_id'): raise TargetClosureError('missing MMO identity')
            if req.preservation.preserve_representation and not req.source_instance.get('representation_id'): raise TargetClosureError('missing representation identity')
            if self._segment_hashes(req.source_segment_chain)!=source_hashes: raise TransportIntegrityError('source segment mutated')
            if file_sha256(self.fabric.path)!=fabric_hash: raise TransportIntegrityError('base fabric mutated')
            alloc_receipt=self.allocator.commit(plan.destination_reservation_id)
            plan.lifecycle.append(PortalState.CLOSED.value)
            receipt={'kind':'PORTAL_CLOSURE_RECEIPT','status':'CLOSED','portal_id':plan.portal_id,'source_instance_id':req.source_instance['instance_id'],'destination_instance_id':plan.destination_instance_id,'canonical_mmo_id':req.source_instance['canonical_mmo_id'],'representation_id':req.source_instance['representation_id'],'source_address':plan.source_address,'target_address':plan.target_address,'sector':plan.sector,'corridor':plan.corridor,'route_reservation_id':plan.route_reservation_id,'destination_allocation':alloc_receipt,'source_content_root':plan.source_content_root,'destination_content_root':dest_content,'source_residue_root':plan.source_residue_root,'destination_residue_root':dest_residue,'chirality_class':req.chirality_class,'resolution_required':req.resolution_required,'bandwidth_required':req.bandwidth_required,'route_min_resolution':plan.corridor['min_resolution'],'route_min_bandwidth':plan.corridor['min_bandwidth'],'destination_segment_sha256':file_sha256(seg_path),'destination_payload_hash':payload_hash,'source_segment_hashes':source_hashes,'base_fabric_sha256':fabric_hash,'lifecycle':list(plan.lifecycle),'timestamp_ns':now_ns()}
            dest=self._destination_meta(req.source_instance,plan,seg_path,receipt['destination_segment_sha256'],receipt)
            plan.lifecycle.append(PortalState.INHERITED.value); receipt['lifecycle']=list(plan.lifecycle)
            self.capacity.release(plan.route_reservation_id,'CLOSED'); self.ledger.append(receipt)
            return PortalResult(dest,asdict(plan),receipt,str(seg_path))
        except Exception as exc:
            if plan is not None:
                try:self.capacity.release(plan.route_reservation_id,'FAILED')
                except:pass
                try:self.allocator.abort(plan.destination_reservation_id)
                except:pass
                fail={'kind':'PORTAL_FAILURE_RECEIPT','status':'FAILED','portal_id':plan.portal_id,'source_instance_id':req.source_instance['instance_id'],'target_address':plan.target_address,'error_type':type(exc).__name__,'error':str(exc),'lifecycle':list(plan.lifecycle)+[PortalState.FAILED.value],'timestamp_ns':now_ns()}; self.ledger.append(fail)
            raise
