import json,sys,tempfile,hashlib,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V5=ROOT/'12_REFERENCE_IMPLEMENTATION'/'vendor_section05'
V4=V5/'vendor_section04'
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION')); sys.path.insert(0,str(V5)); sys.path.insert(0,str(V4)); sys.path.insert(0,str(V4/'vendor_section03'))
from vendor.genesis_chirality_machine.image import FabricImageBuilder,FabricImage
from vendor.genesis_chirality_machine.fixture import deterministic_cells
from vendor.genesis_geometric_engine.allocator import RegionAllocator
from vendor.genesis_geometric_engine.segment import GeometricOverlayWriter
from genesis_portal_engine import CorridorGraph,CapacityLedger,PortalEngine
from genesis_portal_engine.model import CorridorEdge,PortalAddress,PreservationContract
from genesis_portal_engine.util import file_sha256
from genesis_rainbow_road.bus import RoadCapacityManager
from genesis_rainbow_road.ledger import RoadLedger
from genesis_sector_bridge import *
from genesis_sector_bridge.model import BridgeRequest,MixedSectorRoadRequest
from genesis_sector_bridge.errors import *


def mk_source(tmp,count=64):
    fp=tmp/'f.gcf'; FabricImageBuilder.build(fp,deterministic_cells(4096)); f=FabricImage(fp); alloc=RegionAllocator(f.cell_count,alignment=8); rid,reg=alloc.reserve(count,'src')
    mmo='TEST:MMO'; iid='source-instance'; sp=tmp/'src.gos'; wr=GeometricOverlayWriter(sp,f.fabric_tag,reg.start,reg.count,hashlib.sha256(mmo.encode()).hexdigest(),hashlib.sha256(iid.encode()).hexdigest(),'0'*64)
    for i in range(count):wr.write(reg.start+i,f.read(f.address_for_index(reg.start+i)))
    wr.finalize(); alloc.commit(rid)
    inst={'instance_id':iid,'canonical_mmo_id':mmo,'representation_id':'TEST:REP','fabric_tag':f.fabric_tag,'region':{'start':reg.start,'count':reg.count,'alignment':reg.alignment,'guard_before':0,'guard_after':0},'mapping_profile':'TEST_3P1P1','roles':['state'],'cells_per_voxel':1,'segment_path':str(sp),'segment_sha256':file_sha256(sp),'segment_chain':[str(sp)],'state':'LIVE','history':[],'provenance':[],'brane_m5':{'I':{'instance_id':iid},'D':{},'Chi':{},'R':{'recursive_depth':1},'P':{}}}
    return f,alloc,inst

def graph():
    es=[
      CorridorEdge('e_ab','A','B',('QFT','GR'),('ANY',),('ANY',),.95,.92,3,1,'Red',True),
      CorridorEdge('e_bc','B','C',('QFT','GR'),('ANY',),('ANY',),.90,.88,3,1,'Orange',True),
      CorridorEdge('e_cd','C','D',('QFT','GR'),('ANY',),('ANY',),.86,.82,3,1,'Green',True),
      CorridorEdge('e_de','D','E',('QFT','GR'),('ANY',),('ANY',),.84,.80,3,1,'Violet',True),
    ]; return CorridorGraph(es)

def setup(tmp):
    tmp.mkdir(parents=True,exist_ok=True); f,alloc,inst=mk_source(tmp); g=graph(); base=CapacityLedger({e.edge_id:e.capacity_units for e in g.edges.values()},tmp/'base.jsonl'); mgr=RoadCapacityManager(base,RoadLedger(tmp/'bus.jsonl')); pe=PortalEngine(f,alloc,g,mgr,tmp/'portals'); be=SectorBridgeEngine(f,tmp/'bridges'); me=MixedSectorRoadEngine(pe,be,mgr,tmp/'mixed'); return f,alloc,inst,g,base,mgr,pe,be,me

def preq(inst,source='QFT',target='GR',domain='A'):
    return BridgeRequest(inst,list(inst['segment_chain']),PortalAddress(domain,sector=source),source,target)

def mreq(inst,start='QFT',wps=None):
    if wps is None:wps=[PortalAddress('B',sector=start),PortalAddress('C',sector='GR' if start=='QFT' else 'QFT')]
    return MixedSectorRoadRequest(inst,list(inst['segment_chain']),PortalAddress('A',sector=start),wps,PreservationContract(['__FULL_CELL__']),resolution_required=.5,bandwidth_required=.5,capacity_units_required=1,road_name='mixed-test')

def run():
  n=0
  with tempfile.TemporaryDirectory() as td:
    tmp=Path(td); f,alloc,inst,g,base,mgr,pe,be,me=setup(tmp)
    # representations
    q=be.reps.read(inst,inst['segment_chain'],PortalAddress('A',sector='QFT'),'QFT','Q'); gview=be.reps.read(inst,inst['segment_chain'],PortalAddress('A',sector='GR'),'GR','G')
    n+=1; assert q.sector=='QFT' and gview.sector=='GR'
    n+=1; assert q.fabric_witness_id==gview.fabric_witness_id
    n+=1; assert q.content_root==gview.content_root and q.residue_root==gview.residue_root
    ca=common_ancestry(q,gview); n+=1; assert ca['admitted']
    n+=1; assert len(ca['relation_id'])==64
    # mismatch
    bad=copy.deepcopy(gview); bad.fabric_witness_id='x'*64
    try:common_ancestry(q,bad); assert False
    except CommonAncestryMismatch:pass
    n+=1
    # deterministic view IDs
    q2=be.reps.read(inst,inst['segment_chain'],PortalAddress('A',sector='QFT'),'QFT','Q'); n+=1; assert q2.representation_view_id==q.representation_view_id
    # bridge q->g
    sh=file_sha256(inst['segment_path']); fh=file_sha256(f.path); br=be.execute(preq(inst)); n+=1; assert br.receipt['status']=='CLOSED'
    n+=1; assert br.receipt['source_sector']=='QFT' and br.receipt['target_sector']=='GR'
    n+=1; assert br.receipt['source_content_root']==br.receipt['target_content_root']
    n+=1; assert br.receipt['source_residue_root']==br.receipt['target_residue_root']
    n+=1; assert br.instance['instance_id']==inst['instance_id']
    n+=1; assert br.instance['segment_chain']==inst['segment_chain']
    n+=1; assert br.address.sector=='GR' and br.address.domain_id=='A'
    n+=1; assert br.instance['history'][-1]['event']=='SECTOR_BRIDGE_CLOSED'
    n+=1; assert br.instance['brane_m5']['Chi']['current_sector']=='GR'
    n+=1; assert audit_bridge_receipt(br.receipt)['pass']
    n+=1; assert file_sha256(inst['segment_path'])==sh and file_sha256(f.path)==fh
    # reverse
    bg=be.execute(preq(inst,'GR','QFT')); n+=1; assert bg.receipt['target_sector']=='QFT'
    # unsupported
    try:be.execute(preq(inst,'QFT','QFT')); assert False
    except UnsupportedSectorPair:pass
    n+=1
    # tamper audit
    tam=copy.deepcopy(br.receipt); tam['target_content_root']='bad'; n+=1; assert not audit_bridge_receipt(tam)['pass']
    # bridge ledger chain
    lines=[json.loads(x) for x in (tmp/'bridges'/'BRIDGE_LEDGER.jsonl').read_text().splitlines() if x.strip()]; n+=1; assert lines and all('entry_hash' in x for x in lines)
    # mixed plan QFT portal then bridge then GR portal
    req=mreq(inst,'QFT',[PortalAddress('B',sector='QFT'),PortalAddress('C',sector='GR')]); plan=me.plan(req); kinds=[x['kind'] for x in plan.actions]
    n+=1; assert kinds==['PORTAL','BRIDGE','PORTAL']
    n+=1; assert plan.actions[1]['source_address']['domain_id']=='B' and plan.actions[1]['target_address']['sector']=='GR'
    n+=1; assert plan.hold_requirements=={'e_ab':1,'e_bc':1}
    n+=1; assert plan.sector_trajectory==['QFT','GR']
    # execute
    res=me.execute(req); n+=1; assert res.receipt['status']=='CLOSED'
    n+=1; assert [x['kind'] for x in res.action_results]==['PORTAL','BRIDGE','PORTAL']
    n+=1; assert len(res.receipt['portal_receipts'])==2 and len(res.receipt['bridge_receipts'])==1
    n+=1; assert res.receipt['source_content_root']==res.receipt['final_content_root']
    n+=1; assert res.final_address.domain_id=='C' and res.final_address.sector=='GR'
    n+=1; assert res.final_instance['canonical_mmo_id']==inst['canonical_mmo_id']
    n+=1; assert res.final_instance['brane_m5']['Chi']['current_sector']=='GR'
    n+=1; assert res.receipt['corridor_edge_trajectory']==['e_ab','e_bc']
    n+=1; assert res.receipt['rainbow_trajectory']==['Red','Orange']
    n+=1; assert audit_mixed_road_receipt(res.receipt)['pass']
    n+=1; assert base.available('e_ab')==3 and base.available('e_bc')==3
    n+=1; assert file_sha256(inst['segment_path'])==sh and file_sha256(f.path)==fh
    # bridge-only target same domain
    f2,a2,i2,g2,b2,m2,p2,be2,me2=setup(tmp/'bridgeonly'); rr=me2.execute(mreq(i2,'QFT',[PortalAddress('A',sector='GR')])); n+=1; assert len(rr.receipt['portal_receipts'])==0 and len(rr.receipt['bridge_receipts'])==1
    n+=1; assert rr.final_instance['instance_id']==i2['instance_id']
    # GR -> QFT mixed
    f3,a3,i3,g3,b3,m3,p3,be3,me3=setup(tmp/'reverse'); rr=me3.execute(mreq(i3,'GR',[PortalAddress('B',sector='GR'),PortalAddress('C',sector='QFT')])); n+=1; assert rr.final_address.sector=='QFT'
    n+=1; assert rr.receipt['bridge_receipts'][0]['source_sector']=='GR'
    # multiple bridges
    f4,a4,i4,g4,b4,m4,p4,be4,me4=setup(tmp/'multi'); rr=me4.execute(mreq(i4,'QFT',[PortalAddress('B',sector='GR'),PortalAddress('C',sector='QFT'),PortalAddress('D',sector='GR')])); n+=1; assert len(rr.receipt['bridge_receipts'])==3
    n+=1; assert len(rr.receipt['portal_receipts'])==3
    n+=1; assert rr.final_address.sector=='GR' and rr.final_address.domain_id=='D'
    # preflight unreachable before bus hold
    bad=mreq(inst,'QFT',[PortalAddress('Z',sector='QFT')])
    try:me.plan(bad); assert False
    except Exception:pass
    n+=1; assert mgr.active is None
    # partial failure after first action - bridge engine fail after first portal
    f5,a5,i5,g5,b5,m5,p5,be5,me5=setup(tmp/'partial')
    class FailBridge:
        def __init__(self,real):self.real=real
        def plan(self,*a,**k):return self.real.plan(*a,**k)
        def execute(self,*a,**k):raise RuntimeError('injected bridge failure')
    me5.bridge=FailBridge(be5)
    try:me5.execute(mreq(i5,'QFT',[PortalAddress('B',sector='QFT'),PortalAddress('C',sector='GR')])); assert False
    except MixedRoadExecutionError as e:
        n+=1; assert e.receipt['status']=='FAILED_PARTIAL'
        n+=1; assert e.receipt['closed_action_count']==1
        n+=1; assert e.receipt['completion_frontier']['domain_id']=='B'
    n+=1; assert b5.available('e_ab')==3 and b5.available('e_bc')==3
    # files persisted
    n+=1; assert list((tmp/'mixed').glob('*.mixedroad.json'))
    for ff in (f,f2,f3,f4,f5):ff.close()
  return n
if __name__=='__main__':
    n=run(); print(f'{n}/{n} PASS')
