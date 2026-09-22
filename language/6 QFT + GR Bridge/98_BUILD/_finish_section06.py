from pathlib import Path
import json, shutil, copy, hashlib, os, sys, subprocess, zipfile, time
BASE=Path('/mnt/data')
NAME='GENESIS_CHIRALITY_MACHINE_SECTION_06_QFT_GR_TRANSDUCTION_v0.1.0_20260821'
ROOT=BASE/NAME
S05=BASE/'GENESIS_CHIRALITY_MACHINE_SECTION_05_RAINBOW_ROAD_v0.1.0_20260821'

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def w(rel,txt):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(txt,encoding='utf-8'); return p
def wj(rel,obj):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,sort_keys=True),encoding='utf-8'); return p

# Persist build scripts for reproducibility
(ROOT/'98_BUILD').mkdir(parents=True,exist_ok=True)
shutil.copy2(BASE/'_build_section06.py',ROOT/'98_BUILD'/'_build_section06.py')
shutil.copy2(Path(__file__),ROOT/'98_BUILD'/'_finish_section06.py')

# refresh unit test results after patch
cp=subprocess.run([sys.executable,str(ROOT/'16_TESTS'/'test_section06.py')],capture_output=True,text=True,cwd=ROOT,timeout=120)
if cp.returncode!=0:
    print(cp.stdout,cp.stderr); raise SystemExit('tests failed')
w('99_RELEASE/TEST_RESULTS.txt',cp.stdout.strip()+'\n')

# Real fixture mixed-sector transductions
REF=ROOT/'20_REAL_FIXTURE_TRANSDUCTIONS'
if REF.exists(): shutil.rmtree(REF)
REF.mkdir()
S05REF=S05/'20_REAL_FIXTURE_ROADS'
shutil.copytree(S05REF/'SOURCE_PARENTS',REF/'SOURCE_PARENTS',dirs_exist_ok=True)
shutil.copytree(S05REF/'SOURCE_TRANSFORMS',REF/'SOURCE_TRANSFORMS',dirs_exist_ok=True)

# imports
V6=ROOT/'12_REFERENCE_IMPLEMENTATION'
V5=V6/'vendor_section05'; V4=V5/'vendor_section04'
sys.path[:0]=[str(V6),str(V5),str(V4),str(V4/'vendor_section03')]
from vendor.genesis_chirality_machine.image import FabricImage
from vendor.genesis_geometric_engine.allocator import RegionAllocator
from genesis_portal_engine import CorridorGraph,CapacityLedger,PortalEngine
from genesis_portal_engine.model import CorridorEdge,PortalAddress,PreservationContract
from genesis_rainbow_road.bus import RoadCapacityManager
from genesis_rainbow_road.ledger import RoadLedger
from genesis_sector_bridge import SectorBridgeEngine,MixedSectorRoadEngine
from genesis_sector_bridge.model import MixedSectorRoadRequest

edge_objs=[
{'edge_id':'red_alpha_orange','source_domain':'ALPHA','target_domain':'ORANGE','sectors':['QFT','GR'],'chirality_classes':['ANY'],'residue_classes':['ANY'],'resolution':0.95,'bandwidth':0.90,'capacity_units':8,'cost':1.0,'color_index':'Red','closure_supported':True},
{'edge_id':'orange_green','source_domain':'ORANGE','target_domain':'GREEN','sectors':['QFT','GR'],'chirality_classes':['ANY'],'residue_classes':['ANY'],'resolution':0.90,'bandwidth':0.85,'capacity_units':8,'cost':1.0,'color_index':'Orange','closure_supported':True},
{'edge_id':'green_blue','source_domain':'GREEN','target_domain':'BLUE','sectors':['QFT','GR'],'chirality_classes':['ANY'],'residue_classes':['ANY'],'resolution':0.88,'bandwidth':0.82,'capacity_units':8,'cost':1.0,'color_index':'Green','closure_supported':True},
{'edge_id':'blue_violet','source_domain':'BLUE','target_domain':'OMEGA','sectors':['QFT','GR'],'chirality_classes':['ANY'],'residue_classes':['ANY'],'resolution':0.86,'bandwidth':0.80,'capacity_units':8,'cost':1.0,'color_index':'Violet','closure_supported':True},
]
edges=[CorridorEdge(**{**e,'sectors':tuple(e['sectors']),'chirality_classes':tuple(e['chirality_classes']),'residue_classes':tuple(e['residue_classes'])}) for e in edge_objs]
graph=CorridorGraph(edges)
wj('17_EXAMPLES/REFERENCE_MIXED_SECTOR_TOPOLOGY.json',{'kind':'SECTION06_REFERENCE_MIXED_SECTOR_RAINBOW_BUS','edges':edge_objs})

fabric=FabricImage(REF/'SOURCE_PARENTS'/'reference_fabric_1m.gcf')
alloc=RegionAllocator(fabric.cell_count,alignment=128)
instances=[]
for label in ['HSV1','HYDROGEN','OXYGEN','BLANK']:
    inst=json.load(open(REF/'SOURCE_TRANSFORMS'/label/'CHILD_INSTANCE.json'))
    r=inst['region']; alloc.entries.append({'reservation_id':'source-'+label,'owner':inst['instance_id'],'start':r['start'],'count':r['count'],'guard':0,'state':'COMMITTED'})
    chain=[str(list((REF/'SOURCE_PARENTS'/label).glob('*.gos'))[0])]
    gtd=list((REF/'SOURCE_TRANSFORMS'/label).glob('*.gtd'))
    if gtd: chain.append(str(gtd[0]))
    inst=copy.deepcopy(inst); inst['segment_chain']=chain; inst['segment_path']=chain[-1]
    instances.append((label,inst))

cases={
# Section 06 focuses on sector transduction. Keep the largest HSV-1 fixture bridge-only
# so the reference suite exercises the real object without spending minutes re-realizing
# the 163,840-cell payload twice. Smaller atomic/blank fixtures exercise mixed Portal+Bridge roads.
'HSV1':('QFT',[('ALPHA','GR')]),
'HYDROGEN':('GR',[('GREEN','GR'),('GREEN','QFT')]),
'OXYGEN':('GR',[('ALPHA','QFT'),('GREEN','QFT')]),
'BLANK':('QFT',[('ALPHA','GR'),('GREEN','GR'),('GREEN','QFT')]),
}
integration=[]
for label,inst in instances:
    start_sector,wp_spec=cases[label]
    out=REF/'RUNS'/label; out.mkdir(parents=True,exist_ok=True)
    basecap=CapacityLedger({e.edge_id:e.capacity_units for e in edges},out/'BASE_CAPACITY_LEDGER.jsonl')
    mgr=RoadCapacityManager(basecap,RoadLedger(out/'RAINBOW_BUS_LEDGER.jsonl'))
    pe=PortalEngine(fabric,alloc,graph,mgr,out/'PORTALS',out/'PORTALS'/'PORTAL_LEDGER.jsonl')
    be=SectorBridgeEngine(fabric,out/'BRIDGES',out/'BRIDGES'/'BRIDGE_LEDGER.jsonl')
    me=MixedSectorRoadEngine(pe,be,mgr,out,out/'MIXED_ROAD_LEDGER.jsonl')
    waypoints=[PortalAddress(domain,sector=sec) for domain,sec in wp_spec]
    req=MixedSectorRoadRequest(inst,list(inst['segment_chain']),PortalAddress('ALPHA',sector=start_sector),waypoints,PreservationContract(['__FULL_CELL__']),resolution_required=.75,bandwidth_required=.70,capacity_units_required=1,chirality_class='ANY',residue_class='ANY',road_name=label+'_REFERENCE_MIXED_ROAD')
    res=me.execute(req)
    wj(str((out/'ROAD_PLAN.json').relative_to(ROOT)),res.plan)
    wj(str((out/'ROAD_RECEIPT.json').relative_to(ROOT)),res.receipt)
    wj(str((out/'FINAL_INSTANCE.json').relative_to(ROOT)),res.final_instance)
    integration.append({
        'label':label,'start_sector':start_sector,'final_sector':res.final_address.sector,'road_id':res.receipt['road_id'],
        'actions':[a['kind'] for a in res.action_results],'portal_count':len(res.receipt['portal_receipts']),'bridge_count':len(res.receipt['bridge_receipts']),
        'sector_trajectory':res.receipt['sector_trajectory'],'edges':res.receipt['corridor_edge_trajectory'],'rainbow_trajectory':res.receipt['rainbow_trajectory'],
        'source_root':res.receipt['source_content_root'],'final_root':res.receipt['final_content_root'],'pass':res.receipt['audit']['pass'] and res.receipt['source_content_root']==res.receipt['final_content_root']
    })
fabric.close()
wj('20_REAL_FIXTURE_TRANSDUCTIONS/INTEGRATION_RESULTS.json',integration)
w('99_RELEASE/INTEGRATION_TEST_RESULTS.txt','\n'.join(f"{x['label']} {x['start_sector']}->{x['final_sector']} {'PASS' if x['pass'] else 'FAIL'} actions={','.join(x['actions'])} bridges={x['bridge_count']} portals={x['portal_count']}" for x in integration)+'\n')

# Rebuild manifest/checksums including fixtures and build scripts
allfiles=[p for p in ROOT.rglob('*') if p.is_file() and p.name not in ('CORE_CHECKSUMS.sha256','CORE_MANIFEST.json')]
entries=[]
for p in sorted(allfiles):
    entries.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)})
wj('99_RELEASE/CORE_MANIFEST.json',{'name':NAME,'version':'0.1.0','section':'06','file_count':len(entries),'test_status':cp.stdout.strip(),'real_fixture_runs':integration,'files':entries})
w('99_RELEASE/CORE_CHECKSUMS.sha256','\n'.join(f"{e['sha256']}  {e['path']}" for e in entries)+'\n')

# Staging dirs for package lineage
for d in ['_section06_lineage_stage','_section06_math_stage','_section06_tome_stage']:
    q=BASE/d
    if q.exists(): shutil.rmtree(q)
    q.mkdir()
line=BASE/'_section06_lineage_stage'
for src,alias in [
(BASE/'GENESIS_LAYER_ZERO_IMPLEMENTATION_v0.1.0_20260821_PART_A.zip','LAYER_ZERO_CORE.zip'),
(BASE/'GENESIS_CHIRALITY_MACHINE_SECTION_01_HARDWARE_ABI_v0.1.0_20260821_PART_A_CORE.zip','SECTION01_CORE.zip'),
(BASE/'GENESIS_CHIRALITY_MACHINE_SECTION_02_GEOMETRIC_INSTANTIATION_v0.1.0_20260821_PART_A_CORE.zip','SECTION02_CORE.zip'),
(BASE/'GENESIS_CHIRALITY_MACHINE_SECTION_03_TRANSFORMATION_ENGINE_v0.1.0_20260821_PART_A_CORE.zip','SECTION03_CORE.zip'),
(BASE/'GENESIS_CHIRALITY_MACHINE_SECTION_04_PORTAL_ENGINE_v0.1.0_20260821_PART_A_CORE.zip','SECTION04_CORE.zip'),
(BASE/'GENESIS_CHIRALITY_MACHINE_SECTION_05_RAINBOW_ROAD_v0.1.0_20260821_PART_A_CORE.zip','SECTION05_CORE.zip'),
(BASE/'CFP_exp.zip','CFP_exp.zip'),
(BASE/'Rainbow_road(1)(1).zip','RAINBOW_ROAD_SOURCE.zip'),
(BASE/'corridor(5).md','CORRIDOR_MATH.md')]:
    if src.exists(): shutil.copy2(src,line/alias)
math=BASE/'_section06_math_stage'
for src,alias in [
(BASE/'1.0 | QFT - GR BRIDGE(1).zip','QFT_GR_BRIDGE.zip'),
(BASE/'TRANSDUCTION_GEOMETRY_v1.0.zip','TRANSDUCTION_GEOMETRY.zip'),
(BASE/'Bandwidth Algebra.zip','BANDWIDTH_ALGEBRA.zip'),
(BASE/'Resolution Readout.zip','RESOLUTION_READOUT.zip'),
(BASE/'Identity Through History.zip','IDENTITY_THROUGH_HISTORY.zip'),
(BASE/'Holonomy and Chirality.zip','HOLONOMY_AND_CHIRALITY.zip'),
(BASE/'1.0(20260821-152752).zip','API43_EXACT_OR_LINEAGE.zip')]:
    if src.exists(): shutil.copy2(src,math/alias)
tome=BASE/'_section06_tome_stage'
for src in [BASE/'MK Ultra(2).pdf',BASE/'MK43U_AERA_Phase_I_II_III_Master_Copy_Full.pdf',BASE/'MK43U_AERA_Helicon_Chirality_Companion.pdf']:
    if src.exists(): shutil.copy2(src,tome/src.name)

# Package helper
PREFIX='GENESIS_CHIRALITY_MACHINE_SECTION_06_QFT_GR_TRANSDUCTION_v0.1.0_20260821'
outs=[]
def zipdir(outpath, sources):
    if outpath.exists(): outpath.unlink()
    with zipfile.ZipFile(outpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for src,arcbase in sources:
            src=Path(src)
            if src.is_dir():
                for p in sorted(src.rglob('*')):
                    if p.is_file(): z.write(p,str(Path(arcbase)/p.relative_to(src)))
            else: z.write(src,str(Path(arcbase)/src.name) if arcbase else src.name)
    # CRC
    with zipfile.ZipFile(outpath) as z:
        bad=z.testzip()
        if bad: raise RuntimeError(f'CRC fail {bad}')
    if outpath.stat().st_size>=100*1024*1024: raise RuntimeError(f'oversize {outpath} {outpath.stat().st_size}')
    outs.append(outpath)

# Part A core excludes bulky real fixture source copies, but includes schemas/code/docs/tests.
core_stage=BASE/'_section06_core_stage'
if core_stage.exists(): shutil.rmtree(core_stage)
shutil.copytree(ROOT,core_stage)
shutil.rmtree(core_stage/'20_REAL_FIXTURE_TRANSDUCTIONS',ignore_errors=True)
zipdir(BASE/(PREFIX+'_PART_A_CORE.zip'),[(core_stage,NAME)])
zipdir(BASE/(PREFIX+'_PART_B_REFERENCE_MIXED_SECTOR_RUNS.zip'),[(REF,NAME+'/20_REAL_FIXTURE_TRANSDUCTIONS')])
zipdir(BASE/(PREFIX+'_PART_C_IMPLEMENTATION_LINEAGE.zip'),[(line,NAME+'/SOURCE_CAPSULES/IMPLEMENTATION_LINEAGE')])
zipdir(BASE/(PREFIX+'_PART_D_MATH_BRIDGE_API43.zip'),[(math,NAME+'/SOURCE_CAPSULES/MATH_BRIDGE_API43')])
zipdir(BASE/(PREFIX+'_PART_E_MK_ULTRA_INFORMATION_QFT_GR.zip'),[(tome,NAME+'/SOURCE_CAPSULES/MK_ULTRA_TOME')])

# release manifest/sha/status
manifest={'name':PREFIX,'section':'06','version':'0.1.0','folder_name':NAME,'test_status':cp.stdout.strip(),'integration':integration,'parts':[]}
for p in outs:
    manifest['parts'].append({'file':p.name,'bytes':p.stat().st_size,'mib':round(p.stat().st_size/1024/1024,3),'sha256':sha(p)})
mp=BASE/(PREFIX+'_MANIFEST.json'); mp.write_text(json.dumps(manifest,indent=2,sort_keys=True))
sp=BASE/(PREFIX+'_SHA256.txt'); sp.write_text('\n'.join(f"{x['sha256']}  {x['file']}" for x in manifest['parts'])+'\n')
st=BASE/(PREFIX+'_PACKAGE_STATUS.txt'); st.write_text('SECTION 06 PACKAGE STATUS\n'+f"Unit tests: {cp.stdout.strip()}\n"+f"Reference runs: {sum(1 for x in integration if x['pass'])}/{len(integration)} PASS\n"+'ZIP CRC: '+str(len(outs))+'/'+str(len(outs))+' clean\n'+'All parts < 100 MiB: YES\n')
print(cp.stdout.strip())
print(json.dumps(integration,indent=2))
for p in outs: print(p.name, round(p.stat().st_size/1024/1024,3),'MiB')
print(mp.name,sp.name,st.name)
