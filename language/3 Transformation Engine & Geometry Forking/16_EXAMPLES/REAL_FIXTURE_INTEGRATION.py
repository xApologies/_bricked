
import sys,json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'11_REFERENCE_IMPLEMENTATION'))
from vendor.genesis_chirality_machine.image import FabricImage
from genesis_transform_engine import TransformationEngine,TransformRequest,InvariantContract
from genesis_transform_engine.view import TransformView
from genesis_transform_engine.util import file_sha256
S02=Path('/mnt/data/GENESIS_CHIRALITY_MACHINE_SECTION_02_GEOMETRIC_INSTANTIATION_v0.1.0_20260821/13_EXAMPLES/INTEGRATION_FIXTURES')
OUT=BASE/'16_EXAMPLES/REAL_FIXTURE_TRANSFORMS'; OUT.mkdir(exist_ok=True)
fabric=FabricImage(S02/'reference_fabric_1m.gcf')
results={}
try:
 for name,op,cap,inv in [
   ('HSV1',{'op':'STABILIZE_RHO','delta':64,'selector':{'type':'role','role':'control'}},'GENERIC_LIVE',InvariantContract(preserve_identity_tags=True,preserve_occupancy=True,preserve_handedness=True,preserve_chi=True)),
   ('HYDROGEN',{'op':'SET_TAU','delta':32,'selector':{'type':'role','role':'control'}},'GENERIC_LIVE',InvariantContract(preserve_identity_tags=True,preserve_occupancy=True,preserve_handedness=True,preserve_chi=True)),
   ('OXYGEN',{'op':'STABILIZE_RHO','delta':16,'selector':{'type':'range','start':0,'end':256}},'GENERIC_LIVE',InvariantContract(preserve_identity_tags=True,preserve_occupancy=True,preserve_handedness=True,preserve_chi=True)),
   ('BLANK',{'op':'INHERIT'},'GENERIC_LIVE',InvariantContract(preserve_identity_tags=True,preserve_occupancy=True,preserve_handedness=True,preserve_chi=True)),
 ]:
   parent=json.loads((S02/name/'INSTANCE.json').read_text())
   # make source path absolute to copied fixture currently in S02
   parent['segment_path']=str(S02/name/{'HSV1':'hsv1.gos','HYDROGEN':'hydrogen.gos','OXYGEN':'oxygen.gos','BLANK':'blank.gos'}[name])
   req=TransformRequest(parent,[parent['segment_path']],cap,[op],inv)
   od=OUT/name; od.mkdir(exist_ok=True)
   eng=TransformationEngine(fabric,od,od/'TRANSFORMATION_LEDGER.jsonl')
   ph=file_sha256(parent['segment_path']); fh=file_sha256(S02/'reference_fabric_1m.gcf')
   r=eng.execute(req)
   (od/'PARENT_INSTANCE.json').write_text(json.dumps(parent,indent=2,sort_keys=True))
   (od/'CHILD_INSTANCE.json').write_text(json.dumps(r.child_instance,indent=2,sort_keys=True))
   (od/'TRANSFORM_PLAN.json').write_text(json.dumps(r.plan,indent=2,sort_keys=True))
   (od/'CLOSURE_RECEIPT.json').write_text(json.dumps(r.receipt,indent=2,sort_keys=True))
   results[name]={'parent_instance_id':parent['instance_id'],'child_instance_id':r.child_instance['instance_id'],'canonical_mmo_id':r.child_instance['canonical_mmo_id'],'changed_cells':r.changed_cells,'pre_state_root':r.pre_state_root,'post_state_root':r.post_state_root,'delta_bytes':Path(r.delta_path).stat().st_size,'delta_sha256':file_sha256(r.delta_path),'parent_unchanged':ph==file_sha256(parent['segment_path']),'fabric_unchanged':fh==file_sha256(S02/'reference_fabric_1m.gcf'),'effects':r.plan['effects'],'capability':cap}
 finally_result=results
finally:
 fabric.close()
(OUT/'INTEGRATION_RESULTS.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\\n')
print(json.dumps(results,indent=2,sort_keys=True))
