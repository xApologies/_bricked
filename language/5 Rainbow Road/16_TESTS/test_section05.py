import json,sys,tempfile,hashlib,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V4=ROOT/'12_REFERENCE_IMPLEMENTATION'/'vendor_section04'
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION')); sys.path.insert(0,str(V4)); sys.path.insert(0,str(V4/'vendor_section03'))
from vendor.genesis_chirality_machine.image import FabricImageBuilder,FabricImage
from vendor.genesis_chirality_machine.fixture import deterministic_cells
from vendor.genesis_geometric_engine.allocator import RegionAllocator
from vendor.genesis_geometric_engine.segment import GeometricOverlayWriter
from genesis_portal_engine import CorridorGraph,CapacityLedger,PortalEngine
from genesis_portal_engine.model import CorridorEdge,PortalAddress,PreservationContract
from genesis_portal_engine.util import file_sha256
from genesis_rainbow_road import *
from genesis_rainbow_road.model import RainbowRoadRequest,RoadTemplate
from genesis_rainbow_road.errors import *
from genesis_rainbow_road.util import digest_obj


def mk_source(tmp,count=64):
    fp=tmp/'f.gcf'; FabricImageBuilder.build(fp,deterministic_cells(4096)); f=FabricImage(fp); alloc=RegionAllocator(f.cell_count,alignment=8); rid,reg=alloc.reserve(count,'src')
    mmo='TEST:MMO'; iid='source-instance'; sp=tmp/'src.gos'; wr=GeometricOverlayWriter(sp,f.fabric_tag,reg.start,reg.count,hashlib.sha256(mmo.encode()).hexdigest(),hashlib.sha256(iid.encode()).hexdigest(),'0'*64)
    for i in range(count):wr.write(reg.start+i,f.read(f.address_for_index(reg.start+i)))
    wr.finalize(); alloc.commit(rid)
    inst={'instance_id':iid,'canonical_mmo_id':mmo,'representation_id':'TEST:REP','fabric_tag':f.fabric_tag,'region':{'start':reg.start,'count':reg.count,'alignment':reg.alignment,'guard_before':0,'guard_after':0},'mapping_profile':'TEST','roles':['state'],'cells_per_voxel':1,'segment_path':str(sp),'segment_sha256':file_sha256(sp),'segment_chain':[str(sp)],'state':'LIVE','history':[],'provenance':[],'brane_m5':{'I':{'instance_id':iid},'D':{},'Chi':{},'R':{'recursive_depth':1},'P':{}}}
    return f,alloc,inst

def graph():
    es=[
      CorridorEdge('e_ab','A','B',('GENERIC','QFT','GR'),('ANY',),('ANY',),.95,.92,3,1,'Red',True),
      CorridorEdge('e_bc','B','C',('GENERIC','QFT','GR'),('ANY',),('ANY',),.90,.88,3,1,'Orange',True),
      CorridorEdge('e_cd','C','D',('GENERIC','QFT','GR'),('ANY',),('ANY',),.86,.82,3,1,'Green',True),
      CorridorEdge('e_de','D','E',('GENERIC','QFT','GR'),('ANY',),('ANY',),.84,.80,3,1,'Violet',True),
      CorridorEdge('e_ac','A','C',('GENERIC',),('ANY',),('ANY',),.99,.99,1,8,'White',True),
    ]; return CorridorGraph(es)

def setup(tmp):
    tmp.mkdir(parents=True,exist_ok=True)
    f,alloc,inst=mk_source(tmp); g=graph(); base=CapacityLedger({e.edge_id:e.capacity_units for e in g.edges.values()},tmp/'base_capacity.jsonl'); buslog=RoadLedger(tmp/'bus.jsonl'); mgr=RoadCapacityManager(base,buslog); pe=PortalEngine(f,alloc,g,mgr,tmp/'portal_out',tmp/'portal_out'/'PORTAL_LEDGER.jsonl'); reg=RoadRegistry(tmp/'registry.json'); re=RainbowRoadEngine(pe,mgr,tmp/'roads',tmp/'roads'/'ROAD_LEDGER.jsonl',reg); return f,alloc,inst,g,base,mgr,pe,re,reg

def req(inst,sector='GENERIC',targets=('B','C'),R=.5,B=.5,cap=1):
    return RainbowRoadRequest(inst,list(inst['segment_chain']),PortalAddress('A',sector=sector),[PortalAddress(x,sector=sector) for x in targets],sector=sector,preservation=PreservationContract(['__FULL_CELL__']),resolution_required=R,bandwidth_required=B,capacity_units_required=cap,chirality_class='ANY',residue_class='ANY',road_name='test-road')

def run():
  n=0
  with tempfile.TemporaryDirectory() as td:
    tmp=Path(td); f,alloc,inst,g,base,mgr,pe,re,reg=setup(tmp)
    p=re.plan(req(inst)); n+=1; assert len(p.leg_plans)==2
    n+=1; assert p.leg_plans[0]['corridor']['edge_ids']==['e_ab'] and p.leg_plans[1]['corridor']['edge_ids']==['e_bc']
    n+=1; assert p.waypoints[-1]['domain_id']=='C'
    n+=1; assert abs(p.min_resolution-.90)<1e-12
    n+=1; assert abs(p.min_bandwidth-.88)<1e-12
    n+=1; assert p.hold_requirements=={'e_ab':1,'e_bc':1}
    p2=re.plan(req(inst)); n+=1; assert p2.road_id==p.road_id
    n+=1; assert p2.transport_holonomy_witness==p.transport_holonomy_witness
    n+=1; assert p.rainbow_trajectory==['Red','Orange']
    # sector mismatch
    bad=req(inst); bad.waypoints=[PortalAddress('B',sector='QFT')]
    try:re.plan(bad); assert False
    except RoadSectorMismatch:pass
    n+=1
    # empty road
    bad=req(inst); bad.waypoints=[]
    try:re.plan(bad); assert False
    except EmptyRoadError:pass
    n+=1
    # bus lease semantics
    hold=mgr.begin_road('manual',{'e_ab':2,'e_bc':1}); n+=1; assert base.available('e_ab')==1
    n+=1; assert mgr.available('e_ab')==2
    sr=mgr.reserve(['e_ab'],1,'p'); n+=1; assert mgr.available('e_ab')==1
    mgr.release(sr); n+=1; assert mgr.available('e_ab')==2
    mgr.end_road('manual'); n+=1; assert base.available('e_ab')==3
    # successful execution
    src_hash=file_sha256(inst['segment_path']); fab_hash=file_sha256(f.path); res=re.execute(req(inst)); n+=1; assert res.receipt['status']=='CLOSED'
    n+=1; assert len(res.portal_results)==2 and len(res.receipt['portal_receipts'])==2
    n+=1; assert all(x.receipt['status']=='CLOSED' for x in res.portal_results)
    n+=1; assert res.receipt['source_content_root']==res.receipt['final_content_root']
    n+=1; assert res.final_instance['canonical_mmo_id']==inst['canonical_mmo_id']
    n+=1; assert res.final_instance['representation_id']==inst['representation_id']
    regs=[inst['region']['start']]+[x.destination_instance['region']['start'] for x in res.portal_results]; n+=1; assert len(regs)==len(set(regs))
    n+=1; assert res.portal_results[1].destination_instance['parent_instance_id']==res.portal_results[0].destination_instance['instance_id']
    n+=1; assert res.receipt['portal_ids']==[x.receipt['portal_id'] for x in res.portal_results]
    n+=1; assert res.receipt['corridor_edge_trajectory']==['e_ab','e_bc']
    n+=1; assert res.receipt['rainbow_trajectory']==['Red','Orange']
    n+=1; assert len(res.receipt['transport_holonomy_witness'])==64
    n+=1; assert res.final_instance['history'][-1]['event']=='RAINBOW_ROAD_CLOSED'
    n+=1; assert 'rainbow_road_receipt' in res.final_instance['provenance'][-1]
    n+=1; assert res.final_instance['brane_m5']['D']['road_id']==res.receipt['road_id']
    n+=1; assert res.final_instance['brane_m5']['Chi']['transport_holonomy_witness']==res.receipt['transport_holonomy_witness']
    n+=1; assert file_sha256(inst['segment_path'])==src_hash
    n+=1; assert file_sha256(f.path)==fab_hash
    n+=1; assert base.available('e_ab')==3 and base.available('e_bc')==3
    n+=1; assert audit_road_receipt(res.receipt)['pass']
    tam=copy.deepcopy(res.receipt); tam['portal_receipts'][0]['portal_id']='tampered'; n+=1; assert not audit_road_receipt(tam)['pass']
    # registry
    t=RoadTemplate(digest_obj({'a':1}),'alias','A',('B','C'),'GENERIC'); reg.register_template(t); n+=1; assert reg.resolve('alias')['source_domain']=='A'
    n+=1; assert reg.resolve('test-road')['road_id']==p.road_id
    # typed plan composition
    q1=req(inst,targets=('B',)); pa=re.plan(q1)
    # make a synthetic B-source plan by adjusting source address; graph select doesn't inspect source instance topology
    q2=req(inst,targets=('C',)); q2.source_address=PortalAddress('B',sector='GENERIC'); pb=re.plan(q2)
    comp=compose_plans(pa,pb); n+=1; assert comp['portal_leg_count']==2 and comp['waypoints'][-1]['domain_id']=='C'
    # unreachable preflight fails before any new Road file
    bad=req(inst,targets=('Z',))
    before=len(list((tmp/'roads').glob('*.road.json')))
    try:re.execute(bad); assert False
    except Exception:pass
    n+=1; assert len(list((tmp/'roads').glob('*.road.json')))==before
    # QFT / GR homogeneous roads
    rq=req(inst,sector='QFT'); rq.road_name='qft-road'; rrq=re.execute(rq); n+=1; assert rrq.receipt['sector']=='QFT'
    rg=req(inst,sector='GR'); rg.road_name='gr-road'; rrg=re.execute(rg); n+=1; assert rrg.receipt['sector']=='GR'
    # partial failure: fail second execute after first closes
    class FailSecond:
        def __init__(self,real): self.real=real; self.graph=real.graph; self.fabric=real.fabric; self.calls=0
        def _source_roots(self,*a,**k): return self.real._source_roots(*a,**k)
        def execute(self,r):
            self.calls+=1
            if self.calls==2: raise RuntimeError('injected second-leg failure')
            return self.real.execute(r)
    # fresh setup avoids name/allocation collisions
    f2,a2,i2,g2,b2,m2,p2e,r2,reg2=setup(tmp/'partial'); r2.portal=FailSecond(p2e)
    try:r2.execute(req(i2)); assert False
    except RoadExecutionError as e:
        n+=1; assert e.receipt['status']=='FAILED_PARTIAL'
        n+=1; assert len(e.receipt['closed_portal_ids'])==1
        n+=1; assert e.receipt['completion_frontier']['domain_id']=='B'
    n+=1; assert b2.available('e_ab')==3 and b2.available('e_bc')==3
    # ledger hash chains
    lines=[json.loads(x) for x in (tmp/'roads'/'ROAD_LEDGER.jsonl').read_text().splitlines() if x.strip()]; n+=1; assert lines and all('entry_hash' in x for x in lines)
    # roadmap file is persisted
    n+=1; assert (tmp/'roads'/(res.receipt['road_id']+'.road.json')).exists()
    f2.close(); f.close()
  return n
if __name__=='__main__':
    n=run(); print(f'{n}/{n} PASS')
