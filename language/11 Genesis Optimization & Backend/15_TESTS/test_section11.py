import json,sys,unittest,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'12_REFERENCE_IMPLEMENTATION'))
from genesis_optimizer import analyze_gir,optimize_gir,codegen_gir,optimize_files,compare_execution
from genesis_optimizer.optimizer import OptimizationError
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import decode,verify,VM
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm.util import sha256_obj as vm_hash

EX=Path('/mnt/data/GENESIS_CHIRALITY_MACHINE_SECTION_10_GENESIS_FRONTEND_v0.1.0_20260821/16_EXAMPLES')

def synthetic():
    return {'ir':'GIR','version':'0.1.0','name':'synthetic','nodes':[
      {'id':'001_c','op':'CONST','out':'%c','args':[],'attrs':{'value':{'x':7}},'type':'ANY'},
      {'id':'002_h','op':'HASH','out':'%h','args':['%c'],'attrs':{},'type':'HASH'},
      {'id':'003_alias','op':'MOVE','out':'%a','args':['%h'],'attrs':{'alias_only':True},'type':'HASH'},
      {'id':'004_dead','op':'CONST','out':'%dead','args':[],'attrs':{'value':99},'type':'ANY'}
    ],'edges':[],'exports':['%a']}

class CoreTests(unittest.TestCase):
  def test_01_analysis(self): self.assertEqual(analyze_gir(synthetic())['nodes'],4)
  def test_02_o0(self):
    g,r,a=optimize_gir(synthetic(),'O0'); self.assertEqual(len(g['nodes']),4)
  def test_03_oaudit(self):
    g,r,a=optimize_gir(synthetic(),'OAUDIT'); self.assertEqual(len(g['nodes']),4)
  def test_04_o1_reduces(self):
    g,r,a=optimize_gir(synthetic(),'O1'); self.assertLess(len(g['nodes']),4)
  def test_05_hash_preserved(self):
    g,_,_=optimize_gir(synthetic(),'O1'); n=next(n for n in g['nodes'] if n.get('out')=='%h'); self.assertEqual(n['op'],'HASH')
  def test_06_hash_dependency_preserved(self):
    g,_,_=optimize_gir(synthetic(),'O1'); n=next(n for n in g['nodes'] if n.get('out')=='%h'); self.assertEqual(n['args'],['%c'])
  def test_07_alias_removed(self):
    g,_,_=optimize_gir(synthetic(),'O1'); self.assertNotIn('003_alias',[n['id'] for n in g['nodes']])
  def test_08_dead_removed(self):
    g,_,_=optimize_gir(synthetic(),'O1'); self.assertNotIn('004_dead',[n['id'] for n in g['nodes']])
  def test_09_export_rewritten(self):
    g,_,_=optimize_gir(synthetic(),'O1'); self.assertIn('%h',g['exports'])
  def test_10_effect_barrier_empty(self):
    g,_,a=optimize_gir(synthetic(),'O1'); self.assertEqual(a['after']['effectful_order'],[])
  def test_11_barriers(self):
    _,r,_=optimize_gir(synthetic(),'O1'); self.assertTrue(all(r['barriers'].values()))
  def test_12_unknown_level(self):
    with self.assertRaises(OptimizationError): optimize_gir(synthetic(),'O9')
  def test_13_codegen_audit(self):
    a=codegen_gir(synthetic(),'O1','audit'); self.assertTrue(verify(a.program)['ok'])
  def test_14_codegen_reference(self):
    a=codegen_gir(synthetic(),'O1','reference'); self.assertTrue(len(a.bytecode)>0)
  def test_15_codegen_compact(self):
    a=codegen_gir(synthetic(),'O1','compact'); self.assertTrue(all(i.source is None for i in a.program.instructions))
  def test_16_decode(self):
    a=codegen_gir(synthetic(),'O1','audit'); self.assertTrue(verify(decode(a.bytecode))['ok'])
  def test_17_equivalence(self):
    a=codegen_gir(synthetic(),'O1','audit'); self.assertEqual(compare_execution(synthetic(),a)['status'],'PASS')
  def test_18_deterministic(self):
    a=codegen_gir(synthetic(),'O1','audit'); b=codegen_gir(synthetic(),'O1','audit'); self.assertEqual(a.bytecode,b.bytecode)
  def test_19_unknown_codegen(self):
    with self.assertRaises(ValueError): codegen_gir(synthetic(),'O1','native-magic')
  def test_20_receipt_ids(self):
    a=codegen_gir(synthetic()); self.assertTrue(a.optimization_receipt['optimization_id'].startswith('gopt-') and a.codegen_receipt['codegen_id'].startswith('gcg-'))

class SourceReferenceTests(unittest.TestCase):
  def runone(self,name,paths):
    r=optimize_files(paths,name=name,level='O1',profile='audit'); self.assertEqual(r['equivalence']['status'],'PASS'); self.assertTrue(verify(r['artifact'].program)['ok']); self.assertTrue(VM().run(decode(r['artifact'].bytecode)).halted); return r
  def test_21_first_portal(self): self.runone('FIRST_PORTAL',[EX/'FIRST_PORTAL.gen'])
  def test_22_rainbow(self): self.runone('RAINBOW_ROAD',[EX/'RAINBOW_ROAD.gen'])
  def test_23_mixed(self): self.runone('MIXED_SECTOR',[EX/'MIXED_SECTOR.gen'])
  def test_24_quantum(self): self.runone('QUANTUM_EFFECT',[EX/'QUANTUM_EFFECT.gen'])
  def test_25_modular(self): self.runone('MODULAR_QFT',sorted((EX/'MODULAR_QFT').glob('*.gen')))
  def test_26_first_compact(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='FC',profile='compact'); self.assertEqual(r['equivalence']['status'],'PASS')
  def test_27_quantum_compact(self):
    r=optimize_files([EX/'QUANTUM_EFFECT.gen'],name='QC',profile='compact'); self.assertEqual(r['equivalence']['status'],'PASS')
  def test_28_first_oaudit(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='FA',level='OAUDIT'); self.assertEqual(r['equivalence']['status'],'PASS')
  def test_29_first_o0(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='F0',level='O0'); self.assertEqual(r['equivalence']['status'],'PASS')
  def test_30_quantum_order_witness(self):
    r=optimize_files([EX/'QUANTUM_EFFECT.gen'],name='QW'); self.assertEqual(r['artifact'].analyses['before']['quantum_order'],r['artifact'].analyses['after']['quantum_order'])
  def test_31_mixed_bridge_witness(self):
    r=optimize_files([EX/'MIXED_SECTOR.gen'],name='MW'); self.assertEqual(r['artifact'].analyses['before']['bridge_order'],r['artifact'].analyses['after']['bridge_order'])
  def test_32_road_witness(self):
    r=optimize_files([EX/'RAINBOW_ROAD.gen'],name='RW'); self.assertEqual(r['artifact'].analyses['before']['portal_road_order'],r['artifact'].analyses['after']['portal_road_order'])
  def test_33_provenance_witness(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='PW'); self.assertEqual(r['artifact'].analyses['before']['provenance_order'],r['artifact'].analyses['after']['provenance_order'])
  def test_34_effect_witness(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='EW'); self.assertEqual(r['artifact'].analyses['before']['effectful_order'],r['artifact'].analyses['after']['effectful_order'])
  def test_35_gir_metadata_retained(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='MD'); self.assertIn('section09',r['artifact'].gir.get('metadata',{}))
  def test_36_codegen_metadata(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='CM'); self.assertIn('section11',r['artifact'].program.metadata)
  def test_37_compact_labels_zero(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='CL',profile='compact'); self.assertEqual(r['artifact'].codegen_receipt['source_labels'],0)
  def test_38_audit_labels_nonzero(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='AL',profile='audit'); self.assertGreater(r['artifact'].codegen_receipt['source_labels'],0)
  def test_39_bytecode_hash_length(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='BH'); self.assertEqual(len(r['artifact'].codegen_receipt['gvm_sha256']),64)
  def test_40_static_recheck(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='SR'); self.assertTrue(r['artifact'].analyses['static_check'].ok)
  def test_41_capability_recheck(self):
    r=optimize_files([EX/'FIRST_PORTAL.gen'],name='CR'); self.assertTrue(r['artifact'].analyses['capability']['ok'])
  def test_42_all_barriers_true(self):
    r=optimize_files([EX/'QUANTUM_EFFECT.gen'],name='AB'); self.assertTrue(all(r['artifact'].optimization_receipt['barriers'].values()))

if __name__=='__main__': unittest.main()
