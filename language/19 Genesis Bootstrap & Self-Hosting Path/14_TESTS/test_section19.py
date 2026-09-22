import json, tempfile, unittest, zipfile
from pathlib import Path

from genesis_bootstrap import BootstrapHarness, load_frontier, verify_frontier, build_gboot, verify_gboot
from genesis_bootstrap.compiler_port import CompilerAwareBraneHost
from genesis_bootstrap.runtime import BootstrapRuntime
from genesis_bootstrap.errors import BootstrapError
from genesis_bootstrap.util import sha256_bytes, digest_obj, canonical_json
from genesis_system_io.compiler import compile_source
from genesis_system_io.bytecode import encode, decode
from genesis_system_io.storage import CASStore
from genesis_system_io.model import PortManifest

SEC=Path(__file__).resolve().parents[1]
CTRL=SEC/'15_EXAMPLES/bootstrap_controller.gen'
FRONT=SEC/'15_EXAMPLES/self_host_frontier.json'

class Section19Tests(unittest.TestCase):
    def test_01_controller_exists(self): self.assertTrue(CTRL.is_file())
    def test_02_frontier_exists(self): self.assertTrue(FRONT.is_file())
    def test_03_frontier_kind(self): self.assertEqual(load_frontier(FRONT)['kind'],'GENESIS_SELF_HOST_FRONTIER')
    def test_04_frontier_status(self): self.assertEqual(load_frontier(FRONT)['release_status'],'PARTIAL_SELF_HOST')
    def test_05_controller_native(self): self.assertEqual(load_frontier(FRONT)['components']['bootstrap_controller']['status'],'GENESIS_NATIVE')
    def test_06_parser_host(self): self.assertEqual(load_frontier(FRONT)['components']['parser']['status'],'HOST_ORACLE')
    def test_07_verifier_host(self): self.assertEqual(load_frontier(FRONT)['components']['verifier']['status'],'HOST_ORACLE')
    def test_08_runtime_host(self): self.assertEqual(load_frontier(FRONT)['components']['runtime']['status'],'HOST_ORACLE')
    def test_09_frontier_root_stable(self): self.assertEqual(verify_frontier(load_frontier(FRONT))['frontier_root'],verify_frontier(load_frontier(FRONT))['frontier_root'])
    def test_10_false_full_self_host_rejected(self):
        d=load_frontier(FRONT); d['release_status']='FULL_SELF_HOST'
        with self.assertRaisesRegex(BootstrapError,'BOOTSTRAP_FALSE_SELF_HOST_CLAIM'): verify_frontier(d)
    def test_11_bad_frontier_header(self):
        d=load_frontier(FRONT); d['kind']='X'
        with self.assertRaisesRegex(BootstrapError,'BOOTSTRAP_FRONTIER_INVALID'): verify_frontier(d)
    def test_12_bad_frontier_status(self):
        d=load_frontier(FRONT); d['components']['parser']['status']='MAGIC'
        with self.assertRaisesRegex(BootstrapError,'BOOTSTRAP_FRONTIER_INVALID'): verify_frontier(d)
    def test_13_controller_compiles(self): self.assertTrue(compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen'))
    def test_14_controller_version(self): self.assertEqual(compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').version,'0.6.0')
    def test_15_controller_module(self): self.assertEqual(compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').module,'genesis.bootstrap.controller')
    def test_16_compiler_port_declared(self): self.assertIn('compiler',compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').ports)
    def test_17_compiler_role(self): self.assertEqual(compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').ports['compiler'].role,'compiler')
    def test_18_compile_capability(self): self.assertIn('compile',compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').ports['compiler'].capabilities)
    def test_19_program_deterministic(self):
        a=encode(compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen')); b=encode(compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen')); self.assertEqual(a,b)
    def test_20_program_roundtrip(self):
        b=encode(compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen')); self.assertEqual(encode(decode(b)),b)
    def test_21_compiler_port_mount(self):
        with tempfile.TemporaryDirectory() as td:
            h=CompilerAwareBraneHost(CASStore(Path(td))); m=compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').ports['compiler']; self.assertEqual(h.mount(m)['status'],'MOUNTED')
    def test_22_compiler_port_compiles(self):
        with tempfile.TemporaryDirectory() as td:
            cas=CASStore(Path(td)); h=CompilerAwareBraneHost(cas); m=compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').ports['compiler']; h.mount(m); ref=cas.put(CTRL.read_bytes()); r=h.realize('compiler','compile',ref); self.assertTrue(r['bytecode_ref'].startswith('sha256:'))
    def test_23_compiler_port_output_exists(self):
        with tempfile.TemporaryDirectory() as td:
            cas=CASStore(Path(td)); h=CompilerAwareBraneHost(cas); m=compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').ports['compiler']; h.mount(m); ref=cas.put(CTRL.read_bytes()); r=h.realize('compiler','compile',ref); self.assertGreater(len(cas.get(r['bytecode_ref'])),40)
    def test_24_compiler_port_hash_matches(self):
        with tempfile.TemporaryDirectory() as td:
            cas=CASStore(Path(td)); h=CompilerAwareBraneHost(cas); m=compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').ports['compiler']; h.mount(m); ref=cas.put(CTRL.read_bytes()); r=h.realize('compiler','compile',ref); self.assertEqual(r['bytecode_sha256'],sha256_bytes(cas.get(r['bytecode_ref'])))
    def test_25_compiler_port_program_id(self):
        with tempfile.TemporaryDirectory() as td:
            cas=CASStore(Path(td)); h=CompilerAwareBraneHost(cas); m=compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').ports['compiler']; h.mount(m); ref=cas.put(CTRL.read_bytes()); r=h.realize('compiler','compile',ref); self.assertTrue(r['program_id'].startswith('sysprog:'))
    def test_26_compiler_port_proof(self):
        with tempfile.TemporaryDirectory() as td:
            cas=CASStore(Path(td)); h=CompilerAwareBraneHost(cas); m=compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').ports['compiler']; h.mount(m); ref=cas.put(CTRL.read_bytes()); r=h.realize('compiler','compile',ref); self.assertEqual(len(r['proof_root']),64)
    def test_27_compiler_port_m6_z(self):
        with tempfile.TemporaryDirectory() as td:
            cas=CASStore(Path(td)); h=CompilerAwareBraneHost(cas); m=compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen').ports['compiler']; h.mount(m); ref=cas.put(CTRL.read_bytes()); r=h.realize('compiler','compile',ref); self.assertTrue(r['M6']['Z'].startswith('z:'))
    def test_28_runtime_closes(self):
        p=compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen')
        with tempfile.TemporaryDirectory() as td:
            rt=BootstrapRuntime(p,Path(td)); rt.seed('source','bootstrap/bootstrap_controller.gen',CTRL.read_bytes()); rr=rt.run(); self.assertEqual(rr.status,'CLOSED')
    def test_29_runtime_compiled_register(self):
        p=compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen')
        with tempfile.TemporaryDirectory() as td:
            rt=BootstrapRuntime(p,Path(td)); rt.seed('source','bootstrap/bootstrap_controller.gen',CTRL.read_bytes()); rr=rt.run(); self.assertIn('bytecode_ref',rr.registers['compiled'])
    def test_30_runtime_durable_commit(self):
        p=compile_source(CTRL.read_text(),'bootstrap/bootstrap_controller.gen')
        with tempfile.TemporaryDirectory() as td:
            rt=BootstrapRuntime(p,Path(td)); rt.seed('source','bootstrap/bootstrap_controller.gen',CTRL.read_bytes()); rr=rt.run(); self.assertEqual(len(rr.durable),1)
    def test_31_harness_fixed_point(self): self.assertTrue(BootstrapHarness(CTRL,FRONT).run().fixed_point)
    def test_32_harness_not_self_hosted(self): self.assertFalse(BootstrapHarness(CTRL,FRONT).run().self_hosted)
    def test_33_harness_status(self): self.assertEqual(BootstrapHarness(CTRL,FRONT).run().status,'BOOTSTRAP_FIXED_POINT')
    def test_34_harness_three_stages(self): self.assertEqual(len(BootstrapHarness(CTRL,FRONT).run().stages),3)
    def test_35_stage_hash_fixed_point(self):
        r=BootstrapHarness(CTRL,FRONT).run(); self.assertEqual(len({s.bytecode_sha256 for s in r.stages}),1)
    def test_36_stage_proof_fixed_point(self):
        r=BootstrapHarness(CTRL,FRONT).run(); self.assertEqual(len({s.proof_root for s in r.stages}),1)
    def test_37_stage_program_id_fixed_point(self):
        r=BootstrapHarness(CTRL,FRONT).run(); self.assertEqual(len({s.program_id for s in r.stages}),1)
    def test_38_stage_prior_chain(self):
        r=BootstrapHarness(CTRL,FRONT).run(); self.assertIsNone(r.stages[0].prior_stage_sha256); self.assertEqual(r.stages[1].prior_stage_sha256,r.stages[0].bytecode_sha256); self.assertEqual(r.stages[2].prior_stage_sha256,r.stages[1].bytecode_sha256)
    def test_39_source_hash_consistent(self):
        r=BootstrapHarness(CTRL,FRONT).run(); self.assertEqual({s.source_sha256 for s in r.stages},{sha256_bytes(CTRL.read_bytes())})
    def test_40_receipt_root_stable(self): self.assertEqual(BootstrapHarness(CTRL,FRONT).run().receipt_root,BootstrapHarness(CTRL,FRONT).run().receipt_root)
    def test_41_missing_source_rejected(self):
        with self.assertRaisesRegex(BootstrapError,'BOOTSTRAP_SOURCE_MISSING'): BootstrapHarness(SEC/'nope.gen',FRONT).run()
    def test_42_gboot_builds(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.gboot'; r=build_gboot(p,{'a':b'1','b':b'2'}); self.assertTrue(p.is_file()); self.assertGreater(r['bytes'],0)
    def test_43_gboot_verifies(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.gboot'; build_gboot(p,{'a':b'1'}); self.assertEqual(verify_gboot(p)['status'],'PASS')
    def test_44_gboot_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            a=Path(td)/'a.gboot'; b=Path(td)/'b.gboot'; build_gboot(a,{'x':b'alpha','y':b'beta'}); build_gboot(b,{'y':b'beta','x':b'alpha'}); self.assertEqual(a.read_bytes(),b.read_bytes())
    def test_45_gboot_manifest_present(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.gboot'; build_gboot(p,{'a':b'1'}); 
            with zipfile.ZipFile(p) as z: self.assertIn('BOOTSTRAP_MANIFEST.json',z.namelist())
    def test_46_gboot_detects_payload_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.gboot'; build_gboot(p,{'a':b'1'}); q=Path(td)/'bad.gboot'
            with zipfile.ZipFile(p) as zin, zipfile.ZipFile(q,'w') as zout:
                for i in zin.infolist(): zout.writestr(i, b'X' if i.filename=='a' else zin.read(i.filename))
            with self.assertRaisesRegex(BootstrapError,'BOOTSTRAP_IMAGE_TAMPER'): verify_gboot(q)
    def test_47_receipt_canonicalizable(self):
        r=BootstrapHarness(CTRL,FRONT).run(); self.assertGreater(len(canonical_json(r.as_dict())),100)
    def test_48_frontier_deferred_blackglass(self): self.assertEqual(load_frontier(FRONT)['components']['blackglass_v3_migration']['status'],'DEFERRED')

if __name__=='__main__': unittest.main(verbosity=2)
