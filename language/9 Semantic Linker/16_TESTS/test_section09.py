import unittest, json, copy, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION'))
from genesis_semantics.typesys import parse_type,compatible,erase_type
from genesis_semantics.checker import check_gir,check_module
from genesis_semantics.effects import effects_for_op
from genesis_semantics.capabilities import reference_backend_capabilities,check_capabilities
from genesis_semantics.linker import link_bundle
from genesis_semantics.errors import LinkError,CapabilityError
from genesis_semantics.vendor.genesis_vm import decode,verify,VM

BUNDLES={p.stem.split('.')[0]:json.loads(p.read_text()) for p in (ROOT/'17_EXAMPLES/bundles').glob('*.json')}
MODS={p.stem.split('.')[0]:json.loads(p.read_text()) for p in (ROOT/'17_EXAMPLES/modules').glob('*.json')}

def gir(nodes,exports=None,edges=None): return {'ir':'GIR','version':'0.1.0','name':'test','nodes':nodes,'edges':edges or [],'exports':exports or []}

class TestTypes(unittest.TestCase): pass
TYPE_CASES=[
 ('FABRIC','FABRIC'),('GEOMETRIC<CLOSED,QFT>','GEOMETRIC<CLOSED,QFT>'),('PORTAL<GR,OPEN>','PORTAL<GR,OPEN>'),('ROAD<OPEN>','ROAD<OPEN>'),('QSTATE<OWNED>','QSTATE<OWNED>'),('BRIDGE<QFT,GR>','BRIDGE<QFT,GR>'),('RECEIPT<PORTAL_CLOSE>','RECEIPT<PORTAL_CLOSE>'),
]
for idx,(src,expect) in enumerate(TYPE_CASES):
    def t(self,src=src,expect=expect): self.assertEqual(str(parse_type(src)),expect)
    setattr(TestTypes,f'test_parse_{idx:02d}',t)
COMPAT=[('GEOMETRIC','GEOMETRIC<CLOSED,QFT>',True),('GEOMETRIC<CLOSED,QFT>','GEOMETRIC<CLOSED,QFT>',True),('GEOMETRIC<CLOSED,GR>','GEOMETRIC<CLOSED,QFT>',False),('ANY','QSTATE<OWNED>',True),('PORTAL<QFT>','PORTAL<QFT,OPEN>',True),('PORTAL<GR>','PORTAL<QFT,OPEN>',False)]
for idx,(a,b,ok) in enumerate(COMPAT):
    def t(self,a=a,b=b,ok=ok): self.assertEqual(compatible(a,b),ok)
    setattr(TestTypes,f'test_compat_{idx:02d}',t)

class TestEffects(unittest.TestCase): pass
EFF=[('FABRIC_MOUNT','READ_FABRIC'),('FABRIC_ALLOC','ALLOCATE'),('ADMIT','ADMIT'),('PORTAL_CLOSE','CLOSE'),('BRIDGE_SECTOR','TRANSDUCE'),('Q_MEASURE','MEASURE'),('BRANE_LIFT','PROJECT'),('EMIT_RECEIPT','PROVENANCE')]
for idx,(op,e) in enumerate(EFF):
    def t(self,op=op,e=e): self.assertIn(e,effects_for_op(op))
    setattr(TestEffects,f'test_effect_{idx:02d}',t)

class TestModules(unittest.TestCase):
    def test_fixture_module(self): self.assertTrue(check_module(MODS['fixture']).ok)
    def test_qft_module_seeded(self): self.assertTrue(check_module(MODS['qft_leg']).ok)
    def test_quantum_module(self): self.assertTrue(check_module(MODS['quantum']).ok)
    def test_effect_budget_failure(self):
        m=copy.deepcopy(MODS['fixture']); m['effects']=[]; r=check_module(m); self.assertFalse(r.ok); self.assertTrue(any(d.code=='EFFECT_BUDGET_EXCEEDED' for d in r.diagnostics))
    def test_unknown_value(self):
        r=check_gir(gir([{'id':'x','op':'ADMIT','out':'%a','args':['%missing'],'type':'ADMISSION'}])); self.assertFalse(r.ok)
    def test_unclosed_portal(self):
        n=[{'id':'m','op':'FABRIC_MOUNT','out':'%f','type':'FABRIC'},{'id':'a','op':'FABRIC_ALLOC','out':'%r','args':['%f'],'type':'REGION'},{'id':'g','op':'GEO_INSTANTIATE','out':'%g','args':['%f','%r'],'type':'GEOMETRIC'},{'id':'ad','op':'ADMIT','out':'%a','args':['%g'],'type':'ADMISSION'},{'id':'p','op':'PORTAL_OPEN','out':'%p','args':['%g','%a'],'attrs':{'sector':'QFT'},'type':'PORTAL'}]
        r=check_gir(gir(n)); self.assertFalse(r.ok); self.assertTrue(any(d.code=='PORTAL_UNCLOSED' for d in r.diagnostics))
    def test_qstate_double_use(self):
        n=[{'id':'m','op':'FABRIC_MOUNT','out':'%f','type':'FABRIC'},{'id':'a','op':'FABRIC_ALLOC','out':'%r','args':['%f'],'type':'REGION'},{'id':'g','op':'GEO_INSTANTIATE','out':'%g','args':['%f','%r'],'type':'GEOMETRIC'},{'id':'q','op':'Q_PREPARE','out':'%q','args':['%g'],'type':'QSTATE'},{'id':'q1','op':'Q_CHANNEL','out':'%q1','args':['%q'],'type':'QSTATE'},{'id':'q2','op':'Q_CHANNEL','out':'%q2','args':['%q'],'type':'QSTATE'},{'id':'m1','op':'Q_MEASURE','out':'%x','args':['%q1'],'type':'QRESULT'},{'id':'m2','op':'Q_MEASURE','out':'%y','args':['%q2'],'type':'QRESULT'}]
        r=check_gir(gir(n)); self.assertFalse(r.ok); self.assertTrue(any(d.code=='LINEAR_USE_AFTER_MOVE' for d in r.diagnostics))
    def test_qstate_generic_move(self):
        n=[{'id':'m','op':'FABRIC_MOUNT','out':'%f','type':'FABRIC'},{'id':'a','op':'FABRIC_ALLOC','out':'%r','args':['%f'],'type':'REGION'},{'id':'g','op':'GEO_INSTANTIATE','out':'%g','args':['%f','%r'],'type':'GEOMETRIC'},{'id':'q','op':'Q_PREPARE','out':'%q','args':['%g'],'type':'QSTATE'},{'id':'mv','op':'MOVE','out':'%q2','args':['%q'],'type':'QSTATE'}]
        r=check_gir(gir(n,exports=['%q2']),export_values=['%q2']); self.assertFalse(r.ok); self.assertTrue(any(d.code=='QSTATE_GENERIC_MOVE' for d in r.diagnostics))

class TestLinker(unittest.TestCase): pass
for idx,key in enumerate(['FIRST_PORTAL','MIXED_SECTOR','QUANTUM_EFFECT','RAINBOW_ROAD']):
    def t(self,key=key):
        r=link_bundle(BUNDLES[key],reference_backend_capabilities()); self.assertTrue(r.check.ok); self.assertEqual(len(r.proofs),8); self.assertTrue(all(x['status']=='PASS' for x in r.proofs)); self.assertTrue(verify(decode(r.bytecode))['ok']); self.assertTrue(VM().run(decode(r.bytecode)).halted)
    setattr(TestLinker,f'test_link_execute_{idx:02d}',t)

class TestLinkFailures(unittest.TestCase):
    def test_missing_module(self):
        b=copy.deepcopy(BUNDLES['FIRST_PORTAL']); b['modules']=[m for m in b['modules'] if m['module']!='fixture']
        with self.assertRaises(LinkError): link_bundle(b)
    def test_import_type_mismatch(self):
        b=copy.deepcopy(BUNDLES['FIRST_PORTAL']); q=next(m for m in b['modules'] if m['module']=='qft_leg'); q['imports'][0]['type']='GEOMETRIC<CLOSED,GR>'
        with self.assertRaises(LinkError): link_bundle(b)
    def test_duplicate_module(self):
        b=copy.deepcopy(BUNDLES['FIRST_PORTAL']); b['modules'].append(copy.deepcopy(b['modules'][0]))
        with self.assertRaises(LinkError): link_bundle(b)
    def test_module_cycle(self):
        b=copy.deepcopy(BUNDLES['FIRST_PORTAL']); f=next(m for m in b['modules'] if m['module']=='fixture'); f['imports']=[{'local':'%x','from':'readout','symbol':'m5','type':'M5'}]
        with self.assertRaises(LinkError): link_bundle(b)
    def test_missing_backend_op(self):
        cap=reference_backend_capabilities(); cap['ops']=[x for x in cap['ops'] if x!='PORTAL_OPEN']
        with self.assertRaises(CapabilityError): link_bundle(BUNDLES['FIRST_PORTAL'],cap)
    def test_missing_sector(self):
        cap=reference_backend_capabilities(); cap['sectors']=['GENERIC','QFT']
        with self.assertRaises(CapabilityError): link_bundle(BUNDLES['MIXED_SECTOR'],cap)
    def test_missing_feature(self):
        cap=reference_backend_capabilities(); cap['features']=[x for x in cap['features'] if x!='quantum_linear']
        with self.assertRaises(CapabilityError): link_bundle(BUNDLES['QUANTUM_EFFECT'],cap)

class TestDeterminism(unittest.TestCase):
    def test_input_order_independent(self):
        b=copy.deepcopy(BUNDLES['FIRST_PORTAL']); r1=link_bundle(b); b['modules']=list(reversed(b['modules'])); r2=link_bundle(b); self.assertEqual(r1.receipt['gvm_sha256'],r2.receipt['gvm_sha256']); self.assertEqual(r1.receipt['gir_hash'],r2.receipt['gir_hash'])
    def test_same_link_id(self):
        r1=link_bundle(BUNDLES['MIXED_SECTOR']); r2=link_bundle(copy.deepcopy(BUNDLES['MIXED_SECTOR'])); self.assertEqual(r1.receipt['link_id'],r2.receipt['link_id'])
    def test_alpha_names(self):
        r=link_bundle(BUNDLES['FIRST_PORTAL']); self.assertTrue(all('::' in n['id'] for n in r.gir['nodes'])); self.assertTrue(all(x.startswith('%') and '::' in x for x in r.gir['exports']))
    def test_refined_metadata(self):
        r=link_bundle(BUNDLES['MIXED_SECTOR']); md=r.gir['metadata']['section09']['refined_types']; self.assertTrue(any(v=='GEOMETRIC<CLOSED,GR>' for v in md.values()))
