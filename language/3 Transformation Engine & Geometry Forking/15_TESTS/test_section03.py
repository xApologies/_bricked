import unittest,tempfile,sys,json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'11_REFERENCE_IMPLEMENTATION'))
from vendor.genesis_chirality_machine.image import FabricImageBuilder,FabricImage
from vendor.genesis_chirality_machine.cell import ChiralityCell
from vendor.genesis_chirality_machine.constants import RIGHT_PATTERN,LEFT_PATTERN
from vendor.genesis_geometric_engine.segment import GeometricOverlayWriter
from genesis_transform_engine import TransformationEngine,TransformRequest,InvariantContract,TransformationDeltaSegment
from genesis_transform_engine.errors import *
from genesis_transform_engine.view import TransformView
from genesis_transform_engine.util import file_sha256

class S03(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory(); self.d=Path(self.t.name)
  cells=[ChiralityCell.right(state_class=1,sigma=50000,chi=40000,rho=10000,lambda_=20000,tau=30000,identity_tag=i+1) for i in range(128)]
  self.fpath=self.d/'fabric.gcf'; tag=FabricImageBuilder.build(self.fpath,cells); self.fabric=FabricImage(self.fpath)
  self.gos=self.d/'parent.gos'; md=hashlib.sha256(b'MMO').hexdigest(); iid='parent-instance'; idig=hashlib.sha256(iid.encode()).hexdigest(); sd=hashlib.sha256(b'source').hexdigest(); wr=GeometricOverlayWriter(self.gos,tag,16,32,md,idig,sd)
  for i in range(16,48): wr.write(i,ChiralityCell.right(state_class=1,sigma=50000,chi=40000,rho=10000,lambda_=20000,tau=30000,identity_tag=i+1))
  wr.finalize()
  self.parent={'instance_id':iid,'canonical_mmo_id':'MMO:TEST','representation_id':'R0','fabric_tag':tag,'region':{'start':16,'count':32,'alignment':1,'guard_before':0,'guard_after':0},'mapping_profile':'TEST','roles':['control'],'cells_per_voxel':1,'grid_shape':[2,4,4],'segment_path':str(self.gos),'segment_sha256':file_sha256(self.gos),'state':'LIVE','history':[],'provenance':[],'brane_m5':{'R':{'recursive_depth':0}}}
  self.engine=TransformationEngine(self.fabric,self.d/'out')
 def tearDown(self): self.fabric.close(); self.t.cleanup()
 def req(self,ops,cap='GENERIC_LIVE',inv=None,**kw): return TransformRequest(self.parent,[str(self.gos)],cap,ops,inv or InvariantContract(),**kw)
 def root(self):
  v=TransformView(self.fabric,[str(self.gos)]); r=v.state_root(16,32); v.close(); return r
 def test_plan_determinism(self):
  q=self.req([{'op':'STABILIZE_RHO','delta':5}]); self.assertEqual(self.engine.plan(q).plan_id,self.engine.plan(q).plan_id)
 def test_stabilize_fork_parent_immutable(self):
  ph=file_sha256(self.gos); fh=file_sha256(self.fpath); r=self.engine.execute(self.req([{'op':'STABILIZE_RHO','delta':7}]))
  self.assertNotEqual(r.pre_state_root,r.post_state_root); self.assertEqual(file_sha256(self.gos),ph); self.assertEqual(file_sha256(self.fpath),fh); self.assertEqual(r.child_instance['parent_instance_id'],self.parent['instance_id'])
 def test_noop_inherit_root(self):
  r=self.engine.execute(self.req([{'op':'INHERIT'}])); self.assertEqual(r.pre_state_root,r.post_state_root); self.assertEqual(r.changed_cells,0)
 def test_identity_tags_preserved(self):
  r=self.engine.execute(self.req([{'op':'STABILIZE_RHO','delta':1}],inv=InvariantContract(preserve_identity_tags=True)))
  self.assertTrue(all(x['pass'] for x in r.receipt['invariants']))
 def test_chirality_invariant_blocks_mirror(self):
  inv=InvariantContract(preserve_occupancy=True,preserve_handedness=True,preserve_chi=True)
  with self.assertRaises(InvariantViolation): self.engine.execute(self.req([{'op':'MIRROR_CHIRALITY'}],inv=inv))
 def test_r_denies_chi_write(self):
  with self.assertRaises(AdmissionError): self.engine.plan(self.req([{'op':'MIRROR_CHIRALITY'}],cap='PIPELINE_R'))
 def test_t_allows_chi_write(self):
  r=self.engine.execute(self.req([{'op':'MIRROR_CHIRALITY'}],cap='PIPELINE_T')); self.assertEqual(r.changed_cells,32)
 def test_redistribution_sum(self):
  r=self.engine.execute(self.req([{'op':'REDISTRIBUTE_RHO','amount':100,'selector':{'type':'range','start':0,'end':4}}]));
  pv=TransformView(self.fabric,[str(self.gos)]); cv=TransformView(self.fabric,r.child_instance['segment_chain']);
  self.assertEqual(sum(pv.read_index(i).rho for i in range(16,20)),sum(cv.read_index(i).rho for i in range(16,20))); pv.close();cv.close()
 def test_stale_parent(self):
  with self.assertRaises(StaleParentError): self.engine.plan(self.req([{'op':'INHERIT'}],expected_parent_root='f'*64))
 def test_projection_only_rejects_write(self):
  with self.assertRaises(AdmissionError): self.engine.plan(self.req([{'op':'SET_TAU','value':1}],cap='PROJECTION_ONLY'))
 def test_delta_reopens(self):
  r=self.engine.execute(self.req([{'op':'SET_TAU','value':123}])); d=TransformationDeltaSegment(r.delta_path); self.assertEqual(d.post_state_root,r.post_state_root); d.close()
 def test_sparse_delta(self):
  r=self.engine.execute(self.req([{'op':'SET_TAU','value':123,'selector':{'type':'range','start':0,'end':3}}])); self.assertEqual(r.changed_cells,3)
 def test_child_reconstructs_root(self):
  r=self.engine.execute(self.req([{'op':'STABILIZE_RHO','delta':3}])); v=TransformView(self.fabric,r.child_instance['segment_chain']); self.assertEqual(v.state_root(16,32),r.post_state_root);v.close()
 def test_branching(self):
  ph=file_sha256(self.gos); a=self.engine.execute(self.req([{'op':'SET_TAU','value':1}])); b=self.engine.execute(self.req([{'op':'SET_TAU','value':2}])); self.assertNotEqual(a.child_instance['instance_id'],b.child_instance['instance_id']); self.assertEqual(file_sha256(self.gos),ph)
 def test_derive_mmo_requires_id(self):
  with self.assertRaises(IdentityPolicyError): self.engine.plan(self.req([{'op':'INHERIT'}],identity_policy='DERIVE_MMO'))
 def test_derive_representation(self):
  r=self.engine.execute(self.req([{'op':'INHERIT'}],identity_policy='DERIVE_REPRESENTATION',derived_representation_id='R1')); self.assertEqual(r.child_instance['canonical_mmo_id'],'MMO:TEST'); self.assertEqual(r.child_instance['representation_id'],'R1')
 def test_brane_relift(self):
  r=self.engine.execute(self.req([{'op':'STABILIZE_RHO','delta':2}])); self.assertEqual(set(r.child_instance['brane_m5']),{'I','D','Chi','R','P'}); self.assertEqual(r.child_instance['brane_m5']['R']['parent_instance_id'],'parent-instance')
 def test_ledger_advances(self):
  self.engine.execute(self.req([{'op':'INHERIT'}])); h1=self.engine.ledger.prev; self.engine.execute(self.req([{'op':'SET_TAU','value':44}])); self.assertNotEqual(h1,self.engine.ledger.prev)
 def test_base_immutable(self):
  h=file_sha256(self.fpath); self.engine.execute(self.req([{'op':'STABILIZE_RHO','delta':9}])); self.assertEqual(h,file_sha256(self.fpath))
 def test_parent_immutable(self):
  h=file_sha256(self.gos); self.engine.execute(self.req([{'op':'STABILIZE_RHO','delta':9}])); self.assertEqual(h,file_sha256(self.gos))
 def test_role_selector(self):
  r=self.engine.execute(self.req([{'op':'SET_TAU','value':88,'selector':{'type':'role','role':'control'}}])); self.assertEqual(r.changed_cells,32)
 def test_voxel_box(self):
  r=self.engine.execute(self.req([{'op':'SET_TAU','value':77,'selector':{'type':'voxel_box','x':[0,1],'y':[0,1],'z':[0,2]}}])); self.assertEqual(r.changed_cells,2)
 def test_sequential_staged(self):
  r=self.engine.execute(self.req([{'op':'STABILIZE_RHO','delta':10},{'op':'DESTABILIZE_RHO','delta':4}])); v=TransformView(self.fabric,r.child_instance['segment_chain']); self.assertEqual(v.read_index(16).rho,10006);v.close()

if __name__=='__main__': unittest.main()
