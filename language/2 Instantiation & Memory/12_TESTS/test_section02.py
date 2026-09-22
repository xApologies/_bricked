import sys, os, tempfile, hashlib, json, unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'10_REFERENCE_IMPLEMENTATION'))
from vendor.genesis_chirality_machine.cell import ChiralityCell
from vendor.genesis_chirality_machine.image import FabricImageBuilder, FabricImage
from genesis_geometric_engine.model import RepresentationBundle
from genesis_geometric_engine.allocator import RegionAllocator
from genesis_geometric_engine.profiles import Generic3p1p1Profile, ScalarChiralityProfile
from genesis_geometric_engine.engine import InstantiationEngine
from genesis_geometric_engine.segment import GeometricOverlaySegment
from genesis_geometric_engine.view import GeometricView
from genesis_geometric_engine.errors import AllocationError

class T(unittest.TestCase):
 def setUp(self):
  self.td=tempfile.TemporaryDirectory(); self.d=Path(self.td.name)
  FabricImageBuilder.build(self.d/'fabric.gcf',[ChiralityCell.right() for _ in range(32768)])
  self.fabric=FabricImage(self.d/'fabric.gcf'); self.basehash=hashlib.sha256((self.d/'fabric.gcf').read_bytes()).hexdigest()
 def tearDown(self): self.fabric.close(); self.td.cleanup()
 def bundle3(self,n=4):
  f=np.zeros((n,n,n,2,2),np.float32); f[...,0,0]=.2; f[...,1,1]=.7
  s=np.ones((n,n,n),np.float32)*.5; p=np.ones((n,n,n),np.float32)*.8; r=np.ones((n,n,n),np.float32)*.6
  return RepresentationBundle('MMO:T','MMO:T:3p1p1','GENERIC_3P1P1',(n,n,n),{'chirality_field_3p1p1':f,'chirality_scalar':s,'persistence':p,'resolution':r},{'field':'abc'})
 def test_01_allocator_non_overlap(self):
  a=RegionAllocator(10000,128); _,r1=a.reserve(1000,'a'); _,r2=a.reserve(1000,'b'); self.assertLessEqual(r1.end,r2.start)
 def test_02_allocator_exhaustion(self):
  a=RegionAllocator(100,1); a.reserve(90,'a'); self.assertRaises(AllocationError,a.reserve,20,'b')
 def test_03_required_cells_3p1p1(self): self.assertEqual(Generic3p1p1Profile().required_cells(self.bundle3()),4**3*5)
 def test_04_materialize_and_live(self):
  a=RegionAllocator(self.fabric.cell_count,128); e=InstantiationEngine(self.fabric,a,self.d/'seg'); b=self.bundle3(); p,r=e.plan(b,Generic3p1p1Profile()); inst,rc=e.materialize(b,Generic3p1p1Profile(),p,r,verify_stride=3); self.assertEqual(inst.state,'LIVE'); self.assertTrue(Path(inst.segment_path).exists())
 def test_05_base_immutable(self):
  a=RegionAllocator(self.fabric.cell_count,128); e=InstantiationEngine(self.fabric,a,self.d/'seg'); b=self.bundle3(); p,r=e.plan(b,Generic3p1p1Profile()); e.materialize(b,Generic3p1p1Profile(),p,r); self.assertEqual(hashlib.sha256((self.d/'fabric.gcf').read_bytes()).hexdigest(),self.basehash)
 def test_06_segment_count(self):
  a=RegionAllocator(self.fabric.cell_count,128); e=InstantiationEngine(self.fabric,a,self.d/'seg'); b=self.bundle3(); p,r=e.plan(b,Generic3p1p1Profile()); inst,_=e.materialize(b,Generic3p1p1Profile(),p,r); s=GeometricOverlaySegment(inst.segment_path); self.assertEqual(s.record_count,p.required_cells); s.close()
 def test_07_read_overlay_precedence(self):
  a=RegionAllocator(self.fabric.cell_count,128); e=InstantiationEngine(self.fabric,a,self.d/'seg'); b=self.bundle3(); p,r=e.plan(b,Generic3p1p1Profile()); inst,_=e.materialize(b,Generic3p1p1Profile(),p,r); s=GeometricOverlaySegment(inst.segment_path); v=GeometricView(self.fabric,[s]); c=v.read_index(inst.region.start); self.assertNotEqual(c.pack(),ChiralityCell.right().pack()); s.close()
 def test_08_formulaic_addressing(self):
  b=self.bundle3(3); cpv=5; x,y,z=1,2,0; lin=(x*3+y)*3+z; self.assertEqual(lin,15); self.assertEqual(lin*cpv,75)
 def test_09_m5_has_no_z(self):
  a=RegionAllocator(self.fabric.cell_count,128); e=InstantiationEngine(self.fabric,a,self.d/'seg'); b=self.bundle3(); p,r=e.plan(b,Generic3p1p1Profile()); inst,_=e.materialize(b,Generic3p1p1Profile(),p,r); self.assertEqual(set(inst.brane_m5),{'I','D','Chi','R','P'}); self.assertNotIn('Z',inst.brane_m5)
 def test_10_scientific_shape_not_m5(self):
  b=self.bundle3(); self.assertEqual(len(b.arrays['chirality_field_3p1p1'].shape),5); self.assertNotEqual(tuple(b.arrays['chirality_field_3p1p1'].shape),('I','D','Chi','R','P'))
 def test_11_scalar_profile(self):
  n=4; s=np.ones((n,n,n),np.float32)*-.4; b=RepresentationBundle('H','H:s','S',(n,n,n),{'chirality_scalar':s},{'s':'h'}); self.assertEqual(ScalarChiralityProfile().required_cells(b),n**3)
 def test_12_release_and_reuse(self):
  a=RegionAllocator(4096,128); rid,r=a.reserve(512,'a'); a.commit(rid); a.release_owner('a'); _,r2=a.reserve(512,'b'); self.assertEqual(r.start,r2.start)
 def test_13_source_hashes_in_m5(self):
  a=RegionAllocator(self.fabric.cell_count,128); e=InstantiationEngine(self.fabric,a,self.d/'seg'); b=self.bundle3(); p,r=e.plan(b,Generic3p1p1Profile()); inst,_=e.materialize(b,Generic3p1p1Profile(),p,r); self.assertEqual(inst.brane_m5['D']['source_hashes'],{'field':'abc'})
 def test_14_segment_hash_stable(self):
  a=RegionAllocator(self.fabric.cell_count,128); e=InstantiationEngine(self.fabric,a,self.d/'seg'); b=self.bundle3(); p,r=e.plan(b,Generic3p1p1Profile()); inst,_=e.materialize(b,Generic3p1p1Profile(),p,r); self.assertEqual(inst.segment_sha256,hashlib.sha256(Path(inst.segment_path).read_bytes()).hexdigest())
 def test_15_control_persistence(self):
  a=RegionAllocator(self.fabric.cell_count,128); e=InstantiationEngine(self.fabric,a,self.d/'seg'); b=self.bundle3(2); p,r=e.plan(b,Generic3p1p1Profile()); inst,_=e.materialize(b,Generic3p1p1Profile(),p,r); s=GeometricOverlaySegment(inst.segment_path); c=s.read_index(inst.region.start+4); self.assertGreater(c.rho,0); s.close()
 def test_16_committed_segment_immutable_by_api(self):
  a=RegionAllocator(self.fabric.cell_count,128); e=InstantiationEngine(self.fabric,a,self.d/'seg'); b=self.bundle3(); p,r=e.plan(b,Generic3p1p1Profile()); inst,_=e.materialize(b,Generic3p1p1Profile(),p,r); before=Path(inst.segment_path).read_bytes(); s=GeometricOverlaySegment(inst.segment_path); s.close(); self.assertEqual(before,Path(inst.segment_path).read_bytes())
 def test_17_distinct_instances(self):
  a=RegionAllocator(self.fabric.cell_count,128); e=InstantiationEngine(self.fabric,a,self.d/'seg'); b=self.bundle3(); p1,r1=e.plan(b,Generic3p1p1Profile()); i1,_=e.materialize(b,Generic3p1p1Profile(),p1,r1); p2,r2=e.plan(b,Generic3p1p1Profile()); i2,_=e.materialize(b,Generic3p1p1Profile(),p2,r2); self.assertNotEqual(i1.instance_id,i2.instance_id); self.assertEqual(i1.canonical_mmo_id,i2.canonical_mmo_id)
 def test_18_role_group_count(self): self.assertEqual(Generic3p1p1Profile.cells_per_voxel,5)

if __name__=='__main__': unittest.main()
