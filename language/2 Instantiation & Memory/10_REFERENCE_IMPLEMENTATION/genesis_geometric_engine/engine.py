from pathlib import Path
import hashlib, json, os
from dataclasses import asdict
from .model import InstantiationPlan, GeometricInstance
from .util import digest_obj, stable_json, now_ns
from .segment import GeometricOverlayWriter, GeometricOverlaySegment
from .brane import BraneM5Adapter
from .errors import InstantiationError

class InstantiationEngine:
    def __init__(self,fabric,allocator,output_dir):
        self.fabric=fabric; self.allocator=allocator; self.output_dir=Path(output_dir); self.output_dir.mkdir(parents=True,exist_ok=True)
    def plan(self,bundle,profile,guard=0):
        core={'mmo':bundle.canonical_mmo_id,'repr':bundle.representation_id,'fabric_tag':self.fabric.fabric_tag,'profile':profile.name,'source_hashes':bundle.source_hashes}
        plan_id=digest_obj(core); instance_id=digest_obj({'plan':plan_id,'ordinal':len(self.allocator.entries)})[:32]
        req=profile.required_cells(bundle)
        rid,region=self.allocator.reserve(req,instance_id,guard=guard)
        return InstantiationPlan(plan_id,instance_id,bundle.canonical_mmo_id,bundle.representation_id,self.fabric.fabric_tag,bundle.grid_shape,profile.name,list(profile.roles),profile.cells_per_voxel,req,region,bundle.source_hashes),rid
    def materialize(self,bundle,profile,plan,reservation_id,verify_stride=4096):
        if plan.region is None: raise InstantiationError('unbound plan')
        mmo_digest=hashlib.sha256(bundle.canonical_mmo_id.encode()).hexdigest(); inst_digest=hashlib.sha256(plan.instance_id.encode()).hexdigest()
        src_digest=hashlib.sha256(stable_json(bundle.source_hashes)).hexdigest()
        seg_path=self.output_dir/(plan.instance_id+'.gos')
        writer=GeometricOverlayWriter(seg_path,self.fabric.fabric_tag,plan.region.start,plan.region.count,mmo_digest,inst_digest,src_digest)
        try:
            xN,yN,zN=bundle.grid_shape; cpv=profile.cells_per_voxel; seed=plan.instance_id
            linear=0
            for x in range(xN):
              for y in range(yN):
                for z in range(zN):
                  cells=profile.encode_voxel(bundle,x,y,z,seed)
                  if len(cells)!=cpv: raise InstantiationError('profile emitted wrong cell count')
                  base=plan.region.start+linear*cpv
                  for off,cell in enumerate(cells): writer.write(base+off,cell)
                  linear+=1
            payload_hash=writer.finalize()
        except Exception:
            writer.abort(); self.allocator.abort(reservation_id); raise
        # verify segment and sample readback
        seg=GeometricOverlaySegment(seg_path,verify=True)
        try:
            if seg.record_count != plan.required_cells: raise InstantiationError('record count mismatch')
            for recno in range(0,seg.record_count,max(1,int(verify_stride))):
                idx=plan.region.start+recno
                if seg.read_index(idx) is None: raise InstantiationError('sample readback failed')
        finally: seg.close()
        alloc_receipt=self.allocator.commit(reservation_id)
        file_hash=hashlib.sha256(seg_path.read_bytes()).hexdigest()
        receipts=[{'kind':'INSTANTIATION_PLAN','plan_id':plan.plan_id,'timestamp_ns':now_ns()},
                  {'kind':'SEGMENT_COMMIT','payload_hash':payload_hash,'file_sha256':file_hash,'record_count':plan.required_cells,'timestamp_ns':now_ns()},
                  {'kind':'REGION_COMMIT','allocation':alloc_receipt,'timestamp_ns':now_ns()}]
        inst=GeometricInstance(plan.instance_id,bundle.canonical_mmo_id,bundle.representation_id,self.fabric.fabric_tag,plan.region,profile.name,list(profile.roles),profile.cells_per_voxel,str(seg_path),file_hash,'COMMITTED',None,[],[{'source_hashes':bundle.source_hashes}])
        inst.state='LIVE'; inst.history.append({'event':'LIVE','timestamp_ns':now_ns(),'segment_sha256':file_hash})
        m5=BraneM5Adapter().adapt(bundle,plan,inst,receipts); inst.brane_m5=m5
        return inst,receipts
    def manifest(self,inst): return inst.to_dict()
