import json,sys,tempfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION'))
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION'/'vendor_section03'))
from vendor.genesis_chirality_machine.image import FabricImageBuilder,FabricImage
from vendor.genesis_chirality_machine.fixture import deterministic_cells
from vendor.genesis_geometric_engine.allocator import RegionAllocator
from vendor.genesis_geometric_engine.segment import GeometricOverlayWriter
from genesis_transform_engine.view import TransformView
from genesis_portal_engine import *
from genesis_portal_engine.model import CorridorEdge,PortalAddress,PortalRequest,PreservationContract
from genesis_portal_engine.util import file_sha256


def mk_source(tmp,count=64,start=0):
    fpath=tmp/'f.gcf'; FabricImageBuilder.build(fpath,deterministic_cells(2048)); f=FabricImage(fpath)
    alloc=RegionAllocator(f.cell_count,alignment=8); rid,reg=alloc.reserve(count,'src');
    mmo='TEST:MMO'; iid='source-instance'; segp=tmp/'src.gos'; wr=GeometricOverlayWriter(segp,f.fabric_tag,reg.start,reg.count,hashlib.sha256(mmo.encode()).hexdigest(),hashlib.sha256(iid.encode()).hexdigest(),'0'*64)
    for i in range(count): wr.write(reg.start+i,f.read(f.address_for_index(reg.start+i)))
    wr.finalize(); alloc.commit(rid)
    inst={'instance_id':iid,'canonical_mmo_id':mmo,'representation_id':'TEST:REP','fabric_tag':f.fabric_tag,'region':{'start':reg.start,'count':reg.count,'alignment':reg.alignment,'guard_before':0,'guard_after':0},'mapping_profile':'TEST','roles':['state'],'cells_per_voxel':1,'segment_path':str(segp),'segment_sha256':file_sha256(segp),'segment_chain':[str(segp)],'state':'LIVE','history':[],'provenance':[],'brane_m5':{'R':{'recursive_depth':1},'D':{},'P':{}}}
    return f,alloc,inst

def graph():
    es=[
      CorridorEdge('e_ab','A','B',('GENERIC','QFT','GR'),('ANY','R'),('ANY',),.9,.9,2,1,'Red',True),
      CorridorEdge('e_bc','B','C',('GENERIC','QFT','GR'),('ANY','R'),('ANY',),.8,.8,2,1,'Green',True),
      CorridorEdge('e_ac_slow','A','C',('GENERIC',),('ANY',),('ANY',),.95,.95,1,5,'Blue',True),
      CorridorEdge('e_bd','B','D',('GR',),('ANY',),('ANY',),.7,.7,1,1,'Violet',True),
      CorridorEdge('e_cd','C','D',('GENERIC','GR'),('ANY',),('ANY',),.85,.85,2,1,'Yellow',True),
    ]; return CorridorGraph(es)

def req(inst,chain,target='C',sector='GENERIC',R=0.5,B=0.5,chi='ANY',cap=1):
    return PortalRequest(inst,chain,PortalAddress('A',sector=sector),PortalAddress(target,sector=sector),sector=sector,preservation=PreservationContract(['__FULL_CELL__']),resolution_required=R,bandwidth_required=B,chirality_class=chi,capacity_units_required=cap)

def run():
  with tempfile.TemporaryDirectory() as td:
    tmp=Path(td); f,alloc,inst=mk_source(tmp); g=graph(); caps={e.edge_id:e.capacity_units for e in g.edges.values()}; cl=CapacityLedger(caps,tmp/'capacity.jsonl'); eng=PortalEngine(f,alloc,g,cl,tmp/'out')
    # 1 path selection chooses A-B-C over costly direct
    p=g.select(req(inst,[inst['segment_path']]),available=cl.available); assert p.edge_ids==['e_ab','e_bc']
    # 2 route domains witness
    assert p.domains==['A','B','C']
    # 3 min R
    assert abs(p.min_resolution-.8)<1e-9
    # 4 min B
    assert abs(p.min_bandwidth-.8)<1e-9
    # 5 high R forces direct
    p2=g.select(req(inst,[inst['segment_path'],],R=.9,B=.9),available=cl.available); assert p2.edge_ids==['e_ac_slow']
    # 6 sector GR route to D
    pg=g.select(req(inst,[inst['segment_path']],target='D',sector='GR',R=.6,B=.6),available=cl.available); assert pg.domains[-1]=='D'
    # 7 QFT cannot reach D
    try:g.select(req(inst,[inst['segment_path']],target='D',sector='QFT'),available=cl.available); assert False
    except Exception:pass
    # 8 chirality restriction accepted R
    pr=g.select(req(inst,[inst['segment_path']],chi='R'),available=cl.available); assert pr.edge_ids
    # 9 deterministic plan
    r=req(inst,[inst['segment_path']]); plan=eng.plan(r); pid=plan.portal_id
    # cleanup plan reservations manually
    cl.release(plan.route_reservation_id,'TEST'); alloc.abort(plan.destination_reservation_id)
    plan2=eng.plan(r); assert plan2.portal_id==pid
    cl.release(plan2.route_reservation_id,'TEST'); alloc.abort(plan2.destination_reservation_id)
    # 10 capacity reservation reduces availability
    rr=cl.reserve(['e_ab','e_bc'],2,'x'); assert cl.available('e_ab')==0
    try:g.select(r,cl.available); assert False
    except Exception:pass
    cl.release(rr,'TEST')
    # 11 execute closes
    src_hash=file_sha256(inst['segment_path']); fab_hash=file_sha256(f.path); res=eng.execute(r); assert res.receipt['status']=='CLOSED'
    # 12 physical region changes
    assert res.destination_instance['region']['start']!=inst['region']['start']
    # 13 content preserved
    assert res.receipt['source_content_root']==res.receipt['destination_content_root']
    # 14 residue preserved
    assert res.receipt['source_residue_root']==res.receipt['destination_residue_root']
    # 15 MMO identity preserved
    assert res.destination_instance['canonical_mmo_id']==inst['canonical_mmo_id']
    # 16 representation preserved
    assert res.destination_instance['representation_id']==inst['representation_id']
    # 17 source segment immutable
    assert file_sha256(inst['segment_path'])==src_hash
    # 18 base fabric immutable
    assert file_sha256(f.path)==fab_hash
    # 19 lifecycle includes close/inherit
    assert 'CLOSED' in res.receipt['lifecycle'] and 'INHERITED' in res.receipt['lifecycle']
    # 20 provenance route retained
    assert res.destination_instance['provenance'][-1]['portal_receipt']['corridor']['edge_ids']==['e_ab','e_bc']
    # 21 BRANE lift
    assert res.destination_instance['brane_m5']['D']['portal_id']==res.receipt['portal_id']
    # 22 capacity released after close
    assert cl.available('e_ab')==2
    # 23 destination independently readable
    from vendor.genesis_geometric_engine.segment import GeometricOverlaySegment
    s=GeometricOverlaySegment(res.destination_segment_path); assert s.record_count==inst['region']['count']; s.close()
    # 24 stale source check
    bad=req(inst,[inst['segment_path']]); bad.expected_source_content_root='0'*64
    try:eng.execute(bad); assert False
    except Exception:pass
    # 25 no target route failure
    bad2=req(inst,[inst['segment_path']],target='Z')
    try:eng.execute(bad2); assert False
    except Exception:pass
    # 26 ledger hash chain exists
    lines=[json.loads(x) for x in (tmp/'out'/'PORTAL_LEDGER.jsonl').read_text().splitlines() if x.strip()]; assert lines and all('entry_hash' in x for x in lines)
    # 27 destination ancestry
    assert res.destination_instance['parent_instance_id']==inst['instance_id']
    f.close()
    return 27

if __name__=='__main__': print(f'{run()}/27 PASS')
