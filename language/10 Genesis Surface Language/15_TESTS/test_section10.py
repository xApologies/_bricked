import unittest,sys,json,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION'))
from genesis_frontend import *
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import decode,verify,VM

EX=ROOT/'16_EXAMPLES'

def src(name): return (EX/name).read_text(encoding='utf-8')

class Section10(unittest.TestCase):
    def test_01_parse_header(self): self.assertEqual(parse_source(src('FIRST_PORTAL.gen'),'x').version,'0.1.0')
    def test_02_parse_module(self): self.assertEqual(parse_source(src('FIRST_PORTAL.gen'),'x').module,'first_portal')
    def test_03_first_statement_en(self): self.assertEqual(parse_source(src('FIRST_PORTAL.gen'),'x').statements[0].kind,'mount')
    def test_04_rel_mnemonic(self): self.assertIn('rel',[x.kind for x in parse_source(src('FIRST_PORTAL.gen'),'x').statements])
    def test_05_ve_mnemonic(self): self.assertIn('transport',[x.kind for x in parse_source(src('FIRST_PORTAL.gen'),'x').statements])
    def test_06_tor_mnemonic(self): self.assertIn('portal_close',[x.kind for x in parse_source(src('FIRST_PORTAL.gen'),'x').statements])
    def test_07_attrs_json(self): self.assertTrue(parse_source(src('FIRST_PORTAL.gen'),'x').statements[4].attrs['admitted'])
    def test_08_lower_ir(self): self.assertEqual(lower_module(parse_source(src('FIRST_PORTAL.gen'),'x'))[0]['ir'],'GIR-MODULE')
    def test_09_lower_mount(self): self.assertEqual(lower_module(parse_source(src('FIRST_PORTAL.gen'),'x'))[0]['gir']['nodes'][0]['op'],'FABRIC_MOUNT')
    def test_10_lower_portal(self): self.assertIn('PORTAL_OPEN',[n['op'] for n in lower_module(parse_source(src('FIRST_PORTAL.gen'),'x'))[0]['gir']['nodes']])
    def test_11_effect_order_edges(self):
        m,_=lower_module(parse_source(src('FIRST_PORTAL.gen'),'x')); self.assertEqual(len(m['gir']['edges']),len(m['gir']['nodes'])-1)
    def test_12_source_map(self): self.assertEqual(len(lower_module(parse_source(src('FIRST_PORTAL.gen'),'x'))[0]['frontend']['source_map']),13)
    def test_13_effect_budget_derived(self):
        m,_=lower_module(parse_source(src('FIRST_PORTAL.gen'),'x')); self.assertIn('TRANSPORT',m['effects']); self.assertIn('CLOSE',m['effects'])
    def test_14_first_build(self): self.assertTrue(compile_sources([('x',src('FIRST_PORTAL.gen'))]).link.check.ok)
    def test_15_first_vm_verify(self): self.assertTrue(verify(decode(compile_sources([('x',src('FIRST_PORTAL.gen'))]).link.bytecode))['ok'])
    def test_16_first_run(self): self.assertTrue(run_build(compile_sources([('x',src('FIRST_PORTAL.gen'))])).halted)
    def test_17_road_build(self): self.assertTrue(compile_sources([('x',src('RAINBOW_ROAD.gen'))]).link.check.ok)
    def test_18_road_run(self): self.assertTrue(run_build(compile_sources([('x',src('RAINBOW_ROAD.gen'))])).halted)
    def test_19_mixed_build(self): self.assertTrue(compile_sources([('x',src('MIXED_SECTOR.gen'))]).link.check.ok)
    def test_20_mixed_run(self): self.assertTrue(run_build(compile_sources([('x',src('MIXED_SECTOR.gen'))])).halted)
    def test_21_quantum_build(self): self.assertTrue(compile_sources([('x',src('QUANTUM_EFFECT.gen'))]).link.check.ok)
    def test_22_quantum_run(self): self.assertTrue(run_build(compile_sources([('x',src('QUANTUM_EFFECT.gen'))])).halted)
    def test_23_modular_parse_use(self): self.assertEqual(parse_source((EX/'MODULAR_QFT/qft_leg.gen').read_text(),'x').imports[0].module,'fixture')
    def test_24_modular_build(self):
        ss=[(str(p),p.read_text()) for p in [EX/'MODULAR_QFT/fixture.gen',EX/'MODULAR_QFT/qft_leg.gen',EX/'MODULAR_QFT/readout.gen']]
        self.assertTrue(compile_sources(ss).link.check.ok)
    def test_25_modular_run(self):
        ss=[(str(p),p.read_text()) for p in [EX/'MODULAR_QFT/fixture.gen',EX/'MODULAR_QFT/qft_leg.gen',EX/'MODULAR_QFT/readout.gen']]
        self.assertTrue(run_build(compile_sources(ss)).halted)
    def test_26_deterministic_bytecode(self):
        a=compile_sources([('x',src('FIRST_PORTAL.gen'))]).link.bytecode; b=compile_sources([('x',src('FIRST_PORTAL.gen'))]).link.bytecode; self.assertEqual(a,b)
    def test_27_deterministic_receipt(self):
        a=compile_sources([('x',src('FIRST_PORTAL.gen'))]).receipt; b=compile_sources([('x',src('FIRST_PORTAL.gen'))]).receipt; self.assertEqual(a,b)
    def test_28_formatter(self): self.assertIn('  en fabric',format_source(src('FIRST_PORTAL.gen')))
    def test_29_comments(self): self.assertEqual(parse_source(src('FIRST_PORTAL.gen').replace('genesis 0.1.0','genesis 0.1.0 # ok'),'x').version,'0.1.0')
    def test_30_bad_version(self):
        with self.assertRaises(FrontendError): parse_source('genesis 9\nmodule x {\n}','x')
    def test_31_missing_close(self):
        with self.assertRaises(FrontendError): parse_source('genesis 0.1.0\nmodule x {\n','x')
    def test_32_unknown_stmt(self):
        with self.assertRaises(FrontendError): parse_source('genesis 0.1.0\nmodule x {\nmagic x\n}\n','x')
    def test_33_duplicate_value(self):
        s='genesis 0.1.0\nmodule x {\nen a : FABRIC = mount "f"\nen a : FABRIC = mount "g"\n}\n'
        with self.assertRaises(FrontendError): parse_source(s,'x')
    def test_34_unknown_export(self):
        with self.assertRaises(FrontendError): parse_source('genesis 0.1.0\nmodule x {\nexport nope : GEOMETRIC\n}\n','x')
    def test_35_unclosed_portal_semantic_error(self):
        s="""genesis 0.1.0\nmodule x {\nen f : FABRIC = mount \"f\"\nen r : REGION = alloc f cells 8\nen g : GEOMETRIC = instantiate f r mmo @h\nadmit g as a @{\"admitted\":true}\nportal GR g with a as p corridor \"c\"\n}\n"""
        with self.assertRaises(FrontendError): lower_module(parse_source(s,'x'))
    def test_36_bridge_required_semantic_error(self):
        s=src('MIXED_SECTOR.gen').replace('  bridge gq QFT -> GR as b @{"preserve":["identity","chirality_ancestry","provenance"]}\n','').replace(' bridge b','').replace(',"bridge":"%b"','')
        with self.assertRaises(FrontendError): lower_module(parse_source(s,'x'))
    def test_37_linear_use_after_move(self):
        s=src('QUANTUM_EFFECT.gen').replace('  q measure q2 as qr','  q measure q1 as qr')
        with self.assertRaises(FrontendError): lower_module(parse_source(s,'x'))
    def test_38_export_refinement(self): self.assertEqual(parse_source(src('MIXED_SECTOR.gen'),'x').exports[0].type,'GEOMETRIC<CLOSED,GR>')
    def test_39_module_effect_exactness(self):
        m,_=lower_module(parse_source(src('QUANTUM_EFFECT.gen'),'x')); self.assertIn('QUANTUM_LINEAR',m['effects']); self.assertIn('MEASURE',m['effects'])
    def test_40_mixed_contains_bridge(self): self.assertIn('BRIDGE_SECTOR',[n['op'] for n in lower_module(parse_source(src('MIXED_SECTOR.gen'),'x'))[0]['gir']['nodes']])
    def test_41_road_contains_append(self): self.assertEqual([n['op'] for n in lower_module(parse_source(src('RAINBOW_ROAD.gen'),'x'))[0]['gir']['nodes']].count('ROAD_APPEND'),2)
    def test_42_frontend_id(self): self.assertTrue(compile_sources([('x',src('FIRST_PORTAL.gen'))]).receipt['frontend_id'].startswith('gfront-'))
    def test_43_link_id_preserved(self): self.assertTrue(compile_sources([('x',src('FIRST_PORTAL.gen'))]).receipt['link_id'].startswith('glnk-'))
    def test_44_gvm_hash_preserved(self): self.assertEqual(compile_sources([('x',src('FIRST_PORTAL.gen'))]).receipt['gvm_sha256'],compile_sources([('x',src('FIRST_PORTAL.gen'))]).link.receipt['gvm_sha256'])
    def test_45_import_lowered_percent(self): self.assertEqual(lower_module(parse_source((EX/'MODULAR_QFT/qft_leg.gen').read_text(),'x'))[0]['imports'][0]['local'],'%source')
    def test_46_source_map_line_positive(self): self.assertGreater(lower_module(parse_source(src('FIRST_PORTAL.gen'),'x'))[0]['frontend']['source_map'][0]['line'],0)

if __name__=='__main__': unittest.main()
