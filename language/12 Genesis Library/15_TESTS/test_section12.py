import json,sys,tempfile,shutil,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'12_REFERENCE_IMPLEMENTATION'))
from genesis_packages import Version,Requirement,load_manifest,hash_package,LocalRegistry,Resolver,ContentStore,PackageRuntime
from genesis_packages.errors import PackageError,ManifestError,ResolutionError
from genesis_packages.lockfile import lock_from_resolution,Lockfile
from genesis_frontend import parse_source
from genesis_frontend.lower import lower_module
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import verify,decode

REG=HERE/'17_STANDARD_LIBRARY/REGISTRY'; PROJ=HERE/'16_EXAMPLES/PROJECTS'

class SemverManifestTests(unittest.TestCase):
  def test_01_version_order(self): self.assertLess(Version.parse('0.1.0'),Version.parse('0.2.0'))
  def test_02_exact(self): self.assertTrue(Requirement('1.2.3').matches(Version.parse('1.2.3')))
  def test_03_caret(self): self.assertTrue(Requirement('^1.2.3').matches(Version.parse('1.9.0')))
  def test_04_caret_blocks_major(self): self.assertFalse(Requirement('^1.2.3').matches(Version.parse('2.0.0')))
  def test_05_tilde(self): self.assertTrue(Requirement('~1.2.3').matches(Version.parse('1.2.9')))
  def test_06_wildcard(self): self.assertTrue(Requirement('1.2.*').matches(Version.parse('1.2.99')))
  def test_07_bad_version(self):
    with self.assertRaises(PackageError): Version.parse('1.2')
  def test_08_manifest(self): self.assertEqual(load_manifest(REG/'genesis.std.fabric/0.1.0/genesis.pkg.json').name,'genesis.std.fabric')
  def test_09_hash_deterministic(self):
    p=REG/'genesis.std.atomic/0.1.0'; self.assertEqual(hash_package(p),hash_package(p))
  def test_10_all_manifests(self):
    self.assertGreaterEqual(len([load_manifest(x) for x in REG.glob('*/*/genesis.pkg.json')]),10)

class ResolverStoreTests(unittest.TestCase):
  def setUp(self): self.reg=LocalRegistry(REG)
  def test_11_names(self): self.assertIn('genesis.std.atomic',self.reg.names())
  def test_12_highest_candidate(self): self.assertEqual(self.reg.versions('genesis.std.core')[0].version,'0.1.0')
  def test_13_resolve_first(self):
    m=load_manifest(PROJ/'FIRST_PORTAL/genesis.pkg.json'); r=Resolver(self.reg).resolve(m); self.assertIn('genesis.std.atomic',r['selected'])
  def test_14_dependency_first(self):
    m=load_manifest(PROJ/'FIRST_PORTAL/genesis.pkg.json'); r=Resolver(self.reg).resolve(m); self.assertLess(r['order'].index('genesis.std.fabric'),r['order'].index('genesis.std.atomic'))
  def test_15_lock_deterministic(self):
    m=load_manifest(PROJ/'FIRST_PORTAL/genesis.pkg.json'); rr=Resolver(self.reg); a=lock_from_resolution(m,rr.resolve(m)); b=lock_from_resolution(m,rr.resolve(m)); self.assertEqual(a.data,b.data)
  def test_16_lock_root_len(self):
    m=load_manifest(PROJ/'FIRST_PORTAL/genesis.pkg.json'); l=lock_from_resolution(m,Resolver(self.reg).resolve(m)); self.assertEqual(len(l.resolution_root),64)
  def test_17_store_install(self):
    with tempfile.TemporaryDirectory() as td:
      e=self.reg.get('genesis.std.atomic','0.1.0'); s=ContentStore(td); p=s.install(e); self.assertTrue(s.verify(e.content_sha256))
  def test_18_store_tamper(self):
    with tempfile.TemporaryDirectory() as td:
      e=self.reg.get('genesis.std.atomic','0.1.0'); s=ContentStore(td); p=s.install(e); (p/'TAMPER').write_text('x'); self.assertFalse(s.verify(e.content_sha256))
  def test_19_missing(self):
    with self.assertRaises(PackageError): self.reg.get('missing.package','0.1.0')
  def test_20_cycle_detector(self):
    # Directly exercise selected graph with synthetic manifest dependencies.
    from types import SimpleNamespace
    a=SimpleNamespace(manifest=SimpleNamespace(dependencies={'b':'*'})); b=SimpleNamespace(manifest=SimpleNamespace(dependencies={'a':'*'}))
    with self.assertRaises(ResolutionError): Resolver(self.reg)._topological({'a':a,'b':b})

class AuditTests(unittest.TestCase):
  def setUp(self):
    self.tmp=tempfile.TemporaryDirectory(); self.rt=PackageRuntime(LocalRegistry(REG),ContentStore(Path(self.tmp.name)/'store'))
  def tearDown(self): self.tmp.cleanup()
  def test_21_audit_first(self):
    m,r,l=self.rt.resolve(PROJ/'FIRST_PORTAL'); a=self.rt.audit(m,r); self.assertEqual(a['module_owner']['genesis.std.atomic.hydrogen'],'genesis.std.atomic')
  def test_22_effects_root(self):
    m,r,l=self.rt.resolve(PROJ/'FIRST_PORTAL'); a=self.rt.audit(m,r); self.assertIn('TRANSPORT',a['effects']['app.first_portal'])
  def test_23_contract_no_effect_use(self):
    m,r,l=self.rt.resolve(PROJ/'FIRST_PORTAL'); a=self.rt.audit(m,r); self.assertEqual(a['effects']['genesis.std.portal'],[])
  def test_24_atomic_effects(self):
    m,r,l=self.rt.resolve(PROJ/'FIRST_PORTAL'); a=self.rt.audit(m,r); self.assertEqual(set(a['effects']['genesis.std.atomic']),{'ALLOCATE','INHERIT'})
  def test_25_stdlib_sources_lower(self):
    for mf in REG.glob('genesis.std*/*/genesis.pkg.json'):
      m=load_manifest(mf)
      for md in m.modules:
        ast=parse_source((m.root/md['path']).read_text(),str(m.root/md['path'])); mod,_=lower_module(ast); self.assertEqual(ast.module,md['name'])

class BuildTests(unittest.TestCase):
  def setUp(self):
    self.tmp=tempfile.TemporaryDirectory(); self.rt=PackageRuntime(LocalRegistry(REG),ContentStore(Path(self.tmp.name)/'store'))
  def tearDown(self): self.tmp.cleanup()
  def runp(self,d):
    r=self.rt.build(PROJ/d); self.assertTrue(r.execution.halted); self.assertEqual(r.toolchain['equivalence']['status'],'PASS'); self.assertTrue(verify(decode(r.toolchain['artifact'].bytecode))['ok']); return r
  def test_26_first(self): self.runp('FIRST_PORTAL')
  def test_27_road(self): self.runp('RAINBOW_ROAD')
  def test_28_mixed(self): self.runp('MIXED_SECTOR')
  def test_29_quantum(self): self.runp('QUANTUM_EFFECT')
  def test_30_package_chain(self): self.runp('PACKAGE_CHAIN')
  def test_31_receipt_id(self): self.assertTrue(self.runp('FIRST_PORTAL').receipt['package_build_id'].startswith('gpkg-'))
  def test_32_resolution_bound(self):
    r=self.runp('FIRST_PORTAL'); self.assertEqual(r.receipt['resolution_root'],r.lockfile.resolution_root)
  def test_33_bytecode_deterministic(self):
    a=self.runp('FIRST_PORTAL'); b=self.runp('FIRST_PORTAL'); self.assertEqual(a.toolchain['artifact'].bytecode,b.toolchain['artifact'].bytecode)
  def test_34_frozen(self):
    a=self.runp('FIRST_PORTAL'); p=Path(self.tmp.name)/'lock.json'; a.lockfile.write(p); b=self.rt.build(PROJ/'FIRST_PORTAL',p); self.assertEqual(a.lockfile.data,b.lockfile.data)
  def test_35_write_build(self):
    r=self.runp('QUANTUM_EFFECT'); o=self.rt.write_build(r,Path(self.tmp.name)/'out'); self.assertTrue((o/'program.gvm').is_file() and (o/'genesis.lock.json').is_file())
  def test_36_receipt_gvm_hash(self): self.assertEqual(len(self.runp('MIXED_SECTOR').receipt['gvm_sha256']),64)
  def test_37_package_chain_has_qftleg(self): self.assertIn('example.qftleg',self.runp('PACKAGE_CHAIN').lockfile.data['order'])
  def test_38_root_exports_only(self):
    r=self.runp('PACKAGE_CHAIN'); self.assertEqual(len(r.toolchain['artifact'].gir['exports']),2)
  def test_39_all_stored(self):
    r=self.runp('FIRST_PORTAL'); self.assertTrue(all(self.rt.store.verify(x['content_sha256']) for x in r.lockfile.data['packages']))
  def test_40_audit_capability_metadata(self): self.assertIn('portal',sum(self.rt.audit(*self.rt.resolve(PROJ/'FIRST_PORTAL')[:2])['capabilities'].values(),[]))

class NegativeTests(unittest.TestCase):
  def test_41_effect_budget(self):
    with tempfile.TemporaryDirectory() as td:
      td=Path(td); shutil.copytree(PROJ/'QUANTUM_EFFECT',td/'p'); m=json.loads((td/'p/genesis.pkg.json').read_text()); m['effects']=[]; (td/'p/genesis.pkg.json').write_text(json.dumps(m));
      rt=PackageRuntime(LocalRegistry(REG),ContentStore(td/'s'))
      with self.assertRaises(PackageError) as c: rt.build(td/'p')
      self.assertEqual(c.exception.code,'EFFECT_BUDGET_EXCEEDED')
  def test_42_direct_dependency(self):
    with tempfile.TemporaryDirectory() as td:
      td=Path(td); shutil.copytree(PROJ/'FIRST_PORTAL',td/'p'); m=json.loads((td/'p/genesis.pkg.json').read_text()); m['dependencies'].pop('genesis.std.atomic'); m['dependencies']['genesis.std']='^0.1.0'; (td/'p/genesis.pkg.json').write_text(json.dumps(m));
      rt=PackageRuntime(LocalRegistry(REG),ContentStore(td/'s'))
      with self.assertRaises(PackageError) as c: rt.build(td/'p')
      self.assertEqual(c.exception.code,'DIRECT_DEPENDENCY_REQUIRED')
  def test_43_frozen_root_drift(self):
    with tempfile.TemporaryDirectory() as td:
      td=Path(td); rt=PackageRuntime(LocalRegistry(REG),ContentStore(td/'s')); r=rt.build(PROJ/'FIRST_PORTAL'); lp=td/'l'; r.lockfile.write(lp); shutil.copytree(PROJ/'FIRST_PORTAL',td/'p'); (td/'p/src/main.gen').write_text((td/'p/src/main.gen').read_text()+'\n# drift\n');
      with self.assertRaises(PackageError) as c: rt.build(td/'p',lp)
      self.assertEqual(c.exception.code,'LOCK_DRIFT')
  def test_44_source_missing(self):
    with tempfile.TemporaryDirectory() as td:
      td=Path(td); shutil.copytree(PROJ/'FIRST_PORTAL',td/'p'); (td/'p/src/main.gen').unlink()
      with self.assertRaises(ManifestError): load_manifest(td/'p/genesis.pkg.json')
  def test_45_unsupported_genesis(self):
    with tempfile.TemporaryDirectory() as td:
      td=Path(td); shutil.copytree(PROJ/'FIRST_PORTAL',td/'p'); m=json.loads((td/'p/genesis.pkg.json').read_text()); m['genesis']='9.9.9'; (td/'p/genesis.pkg.json').write_text(json.dumps(m));
      with self.assertRaises(ManifestError) as c: load_manifest(td/'p/genesis.pkg.json')
      self.assertEqual(c.exception.code,'GENESIS_VERSION_UNSUPPORTED')
  def test_46_duplicate_module_manifest(self):
    with tempfile.TemporaryDirectory() as td:
      td=Path(td); shutil.copytree(PROJ/'FIRST_PORTAL',td/'p'); m=json.loads((td/'p/genesis.pkg.json').read_text()); m['modules'].append(dict(m['modules'][0])); (td/'p/genesis.pkg.json').write_text(json.dumps(m));
      with self.assertRaises(ManifestError): load_manifest(td/'p/genesis.pkg.json')

class ReleaseTests(unittest.TestCase):
  def test_47_meta_resolves(self):
    # synthetic application depending on meta stdlib
    with tempfile.TemporaryDirectory() as td:
      d=Path(td); (d/'src').mkdir(); (d/'src/main.gen').write_text('genesis 0.1.0\nmodule meta_app {\n  emit receipt as receipt\n  export receipt : RECEIPT<EXECUTION>\n}\n');
      man={'manifest':'GENESIS-PACKAGE','schema_version':'0.1.0','name':'meta_app','version':'0.1.0','genesis':'0.1.0','kind':'application','modules':[{'name':'meta_app','path':'src/main.gen'}],'dependencies':{'genesis.std':'^0.1.0'},'effects':['PROVENANCE'],'backend_capabilities':[],'entry_exports':['meta_app::receipt']}; (d/'genesis.pkg.json').write_text(json.dumps(man));
      r=Resolver(LocalRegistry(REG)).resolve(load_manifest(d/'genesis.pkg.json')); self.assertIn('genesis.std.quantum',r['selected'])
  def test_48_module_names_unique_registry(self):
    owners={}
    for mf in REG.glob('*/*/genesis.pkg.json'):
      m=load_manifest(mf)
      for x in m.module_names(): self.assertNotIn(x,owners); owners[x]=m.name
  def test_49_content_roots_len(self):
    reg=LocalRegistry(REG); self.assertTrue(all(len(e.content_sha256)==64 for e in reg.scan().values()))
  def test_50_reference_project_count(self): self.assertEqual(len(list(PROJ.glob('*/genesis.pkg.json'))),5)

if __name__=='__main__': unittest.main()
