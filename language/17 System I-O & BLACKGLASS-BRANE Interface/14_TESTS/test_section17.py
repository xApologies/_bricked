import tempfile, unittest
from pathlib import Path

from genesis_system_io import *
from genesis_system_io.model import EndpointKind,EndpointMode,EndpointSpec,PortManifest,Instruction,Op,SystemProgram
from genesis_system_io.util import object_ref,digest_obj
from genesis_system_io.brane import BraneHostReference
from genesis_system_io.blackglass import BlackglassHeartReference
from genesis_system_io.device import DeviceReference
from genesis_system_io.storage import CASStore,SandboxFS

SEC=Path(__file__).resolve().parents[1]
EX=SEC/'15_EXAMPLES'

def comp(name): return compile_source((EX/name).read_text(),str(EX/name))

def run_example(name,data=b'genesis-system-fixture'):
    p=comp(name)
    td=tempfile.TemporaryDirectory()
    r=SystemRuntime(p,Path(td.name))
    read_paths=[]
    for i in p.instructions:
        if i.op==Op.READ: read_paths.append((i.attrs['endpoint'],i.attrs['path']))
    for ep,path in read_paths:
        if p.endpoints[ep].kind==EndpointKind.SOURCE: r.seed(ep,path,data)
    out=r.run(); return td,r,out

def src(body): return 'genesis 0.6.0\nmodule t {\n'+body+'\n}\n'

def base_caps(*extra):
    return '\n'.join('  capability '+x for x in extra)

class Section17Tests(unittest.TestCase):
    def test_01_parse_version(self): self.assertEqual(parse_source((EX/'01_SOURCE_READ.gen').read_text()).version,'0.6.0')
    def test_02_parse_module(self): self.assertEqual(comp('06_END_TO_END_MAINFRAME.gen').module,'end_to_end_mainframe')
    def test_03_parse_capabilities(self): self.assertIn('brane.realize',comp('03_BRANE_LIBRARY_QUERY.gen').capabilities)
    def test_04_parse_endpoint_kind(self): self.assertEqual(comp('01_SOURCE_READ.gen').endpoints['source'].kind,EndpointKind.SOURCE)
    def test_05_parse_endpoint_mode(self): self.assertEqual(comp('02_DERIVED_WRITE_CAS.gen').endpoints['derived'].mode,EndpointMode.READ_WRITE)
    def test_06_parse_port_role(self): self.assertEqual(comp('03_BRANE_LIBRARY_QUERY.gen').ports['library'].role,'library')
    def test_07_parse_port_dimension(self): self.assertEqual(comp('03_BRANE_LIBRARY_QUERY.gen').ports['library'].internal_dimension,5)
    def test_08_parse_port_contract(self): self.assertEqual(comp('03_BRANE_LIBRARY_QUERY.gen').ports['library'].contract_version,'2.0')
    def test_09_parse_api_port_caps(self): self.assertIn('resolve',comp('07_API_PORT_QUERY.gen').ports['api'].capabilities)
    def test_10_opcode_window(self): self.assertEqual((int(Op.READ),int(Op.SYS_CLOSE)),(0x00B0,0x00BB))
    def test_11_source_read_closed(self):
        td,rt,r=run_example('01_SOURCE_READ.gen'); self.addCleanup(td.cleanup); self.assertEqual(r.status,'CLOSED')
    def test_12_derived_closed(self):
        td,rt,r=run_example('02_DERIVED_WRITE_CAS.gen'); self.addCleanup(td.cleanup); self.assertEqual(r.status,'CLOSED')
    def test_13_brane_closed(self):
        td,rt,r=run_example('03_BRANE_LIBRARY_QUERY.gen'); self.addCleanup(td.cleanup); self.assertEqual(r.status,'CLOSED')
    def test_14_blackglass_closed(self):
        td,rt,r=run_example('04_BLACKGLASS_COMMIT.gen'); self.addCleanup(td.cleanup); self.assertEqual(r.status,'CLOSED')
    def test_15_device_closed(self):
        td,rt,r=run_example('05_DEVICE_CAPABILITY.gen'); self.addCleanup(td.cleanup); self.assertEqual(r.status,'CLOSED')
    def test_16_end_to_end_closed(self):
        td,rt,r=run_example('06_END_TO_END_MAINFRAME.gen'); self.addCleanup(td.cleanup); self.assertEqual(r.status,'CLOSED')
    def test_17_api_closed(self):
        td,rt,r=run_example('07_API_PORT_QUERY.gen'); self.addCleanup(td.cleanup); self.assertEqual(r.status,'CLOSED')
    def test_18_cas_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            c=CASStore(Path(td)); ref=c.put(b'abc'); self.assertEqual(c.get(ref),b'abc')
    def test_19_cas_ref_shape(self): self.assertRegex(object_ref(b'abc'),r'^sha256:[0-9a-f]{64}$')
    def test_20_cas_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            c=CASStore(Path(td)); self.assertEqual(c.put(b'abc'),c.put(b'abc'))
    def test_21_cas_missing(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(Exception,'CAS_OBJECT_MISSING'): CASStore(Path(td)).get('sha256:'+'0'*64)
    def test_22_cas_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            c=CASStore(Path(td)); ref=c.put(b'abc'); p=c._path(ref); p.write_bytes(b'xyz')
            with self.assertRaisesRegex(Exception,'CAS_INTEGRITY_FAILURE'): c.get(ref)
    def test_23_sandbox_read(self):
        with tempfile.TemporaryDirectory() as td:
            fs=SandboxFS({'source':Path(td)/'source'}); (Path(td)/'source'/'a').write_bytes(b'x'); self.assertEqual(fs.read('source','a'),b'x')
    def test_24_sandbox_escape(self):
        with tempfile.TemporaryDirectory() as td:
            fs=SandboxFS({'source':Path(td)/'source'})
            with self.assertRaisesRegex(Exception,'SYSTEM_PATH_ESCAPE'): fs.read('source','../escape')
    def test_25_derived_atomic_write(self):
        with tempfile.TemporaryDirectory() as td:
            fs=SandboxFS({'derived':Path(td)/'derived'}); ref=fs.write_derived('derived','x/y.bin',b'123'); self.assertEqual((Path(td)/'derived/x/y.bin').read_bytes(),b'123'); self.assertEqual(ref,object_ref(b'123'))
    def test_26_audit_append(self):
        with tempfile.TemporaryDirectory() as td:
            fs=SandboxFS({'audit':Path(td)/'audit'}); fs.append_audit('audit','a.log',b'a'); fs.append_audit('audit','a.log',b'b'); self.assertEqual((Path(td)/'audit/a.log').read_bytes(),b'ab')
    def test_27_brane_manifest_valid(self): self.assertTrue(BraneHostReference.validate_manifest(comp('03_BRANE_LIBRARY_QUERY.gen').ports['library']))
    def test_28_brane_bad_dimension(self):
        m=PortManifest('x','library','x','1',4,'2.0','READ_ONLY','DERIVED_ONLY',('recover',))
        with self.assertRaisesRegex(Exception,'BRANE_PORT_INVALID'): BraneHostReference.validate_manifest(m)
    def test_29_brane_bad_contract(self):
        m=PortManifest('x','library','x','1',5,'1.0','READ_ONLY','DERIVED_ONLY',('recover',))
        with self.assertRaisesRegex(Exception,'BRANE_PORT_INVALID'): BraneHostReference.validate_manifest(m)
    def test_30_brane_bad_canonical_policy(self):
        m=PortManifest('x','library','x','1',5,'2.0','READ_WRITE','DERIVED_ONLY',('recover',))
        with self.assertRaisesRegex(Exception,'BRANE_PORT_INVALID'): BraneHostReference.validate_manifest(m)
    def test_31_brane_bad_rewrite_policy(self):
        m=PortManifest('x','library','x','1',5,'2.0','READ_ONLY','CANONICAL_WRITE',('recover',))
        with self.assertRaisesRegex(Exception,'BRANE_PORT_INVALID'): BraneHostReference.validate_manifest(m)
    def test_32_brane_z_host_owned(self):
        h=BraneHostReference(); m=comp('03_BRANE_LIBRARY_QUERY.gen').ports['library']; h.mount(m)
        with self.assertRaisesRegex(Exception,'BRANE_Z_CALLER_OWNED'): h.realize('library','recover','sha256:'+'1'*64,{'Z':'caller'})
    def test_33_brane_unmounted(self):
        with self.assertRaisesRegex(Exception,'BRANE_PORT_NOT_MOUNTED'): BraneHostReference().realize('x','recover','sha256:'+'1'*64)
    def test_34_brane_capability_unavailable(self):
        h=BraneHostReference(); m=comp('03_BRANE_LIBRARY_QUERY.gen').ports['library']; h.mount(m)
        with self.assertRaisesRegex(Exception,'BRANE_CAPABILITY_UNAVAILABLE'): h.realize('library','erase','sha256:'+'1'*64)
    def test_35_brane_realization_has_z(self):
        h=BraneHostReference(); m=comp('03_BRANE_LIBRARY_QUERY.gen').ports['library']; h.mount(m); r=h.realize('library','recover','sha256:'+'1'*64); self.assertTrue(r['M6']['Z'].startswith('z:'))
    def test_36_brane_realization_deterministic_fresh_host(self):
        m=comp('03_BRANE_LIBRARY_QUERY.gen').ports['library']; h1=BraneHostReference(); h2=BraneHostReference(); h1.mount(m); h2.mount(m); self.assertEqual(h1.realize('library','recover','sha256:'+'1'*64),h2.realize('library','recover','sha256:'+'1'*64))
    def test_37_heart_direct_write_forbidden(self):
        with tempfile.TemporaryDirectory() as td:
            h=BlackglassHeartReference(CASStore(Path(td)))
            with self.assertRaisesRegex(Exception,'BLACKGLASS_DIRECT_WRITE_FORBIDDEN'): h.direct_write(b'x')
    def test_38_heart_proposal_staged(self):
        with tempfile.TemporaryDirectory() as td:
            h=BlackglassHeartReference(CASStore(Path(td))); p=h.propose({'x':1},'p'); self.assertEqual(p['status'],'STAGED')
    def test_39_heart_admission_committed(self):
        with tempfile.TemporaryDirectory() as td:
            h=BlackglassHeartReference(CASStore(Path(td))); p=h.propose({'x':1},'p'); a=h.admit(p['proposal_id'],True); self.assertEqual(a['status'],'COMMITTED')
    def test_40_heart_admission_needs_authority(self):
        with tempfile.TemporaryDirectory() as td:
            h=BlackglassHeartReference(CASStore(Path(td))); p=h.propose({'x':1},'p')
            with self.assertRaisesRegex(Exception,'BLACKGLASS_ADMISSION_AUTHORITY'): h.admit(p['proposal_id'],False)
    def test_41_heart_unknown_proposal(self):
        with tempfile.TemporaryDirectory() as td:
            h=BlackglassHeartReference(CASStore(Path(td)))
            with self.assertRaisesRegex(Exception,'BLACKGLASS_PROPOSAL_UNKNOWN'): h.admit('proposal:nope',True)
    def test_42_device_request(self): self.assertEqual(DeviceReference().request('speaker','speech.output',None)['status'],'ACCEPTED')
    def test_43_device_missing_capability(self):
        with self.assertRaisesRegex(Exception,'DEVICE_CAPABILITY_UNAVAILABLE'): DeviceReference().request('speaker','vision.capture',None)
    def test_44_bytecode_deterministic(self): self.assertEqual(encode(comp('06_END_TO_END_MAINFRAME.gen')),encode(comp('06_END_TO_END_MAINFRAME.gen')))
    def test_45_bytecode_roundtrip(self):
        p=comp('03_BRANE_LIBRARY_QUERY.gen'); q=decode(encode(p)); self.assertEqual(disassemble(p),disassemble(q))
    def test_46_bytecode_tamper(self):
        b=bytearray(encode(comp('01_SOURCE_READ.gen'))); b[-1]^=1
        with self.assertRaisesRegex(Exception,'SYSTEM_BYTECODE_TAMPER'): decode(bytes(b))
    def test_47_bytecode_magic(self):
        with self.assertRaisesRegex(Exception,'SYSTEM_BYTECODE_MAGIC'): decode(b'NOPE'+b'0'*40)
    def test_48_disasm_endpoint(self): self.assertIn('ENDPOINT source SOURCE READ',disassemble(comp('01_SOURCE_READ.gen')))
    def test_49_disasm_port(self): self.assertIn('PORT library role=library',disassemble(comp('03_BRANE_LIBRARY_QUERY.gen')))
    def test_50_disasm_realize(self): self.assertIn('BRANE_REALIZE',disassemble(comp('03_BRANE_LIBRARY_QUERY.gen')))
    def test_51_program_id_stable(self): self.assertEqual(comp('06_END_TO_END_MAINFRAME.gen').metadata['program_id'],comp('06_END_TO_END_MAINFRAME.gen').metadata['program_id'])
    def test_52_proof_root_nonzero(self): self.assertNotEqual(comp('06_END_TO_END_MAINFRAME.gen').metadata['verification']['proof_root'],'0'*64)
    def test_53_receipt_sequence_contiguous(self):
        td,rt,r=run_example('06_END_TO_END_MAINFRAME.gen'); self.addCleanup(td.cleanup); self.assertEqual([x['sequence'] for x in r.receipts],list(range(1,len(r.receipts)+1)))
    def test_54_receipt_root_nonzero(self):
        td,rt,r=run_example('01_SOURCE_READ.gen'); self.addCleanup(td.cleanup); self.assertNotEqual(r.receipt_root,'0'*64)
    def test_55_receipt_deterministic(self):
        td1,rt1,r1=run_example('01_SOURCE_READ.gen'); td2,rt2,r2=run_example('01_SOURCE_READ.gen'); self.addCleanup(td1.cleanup); self.addCleanup(td2.cleanup); self.assertEqual(r1.receipts,r2.receipts)
    def test_56_end_to_end_durable(self):
        td,rt,r=run_example('06_END_TO_END_MAINFRAME.gen'); self.addCleanup(td.cleanup); self.assertEqual(len(r.durable),1)
    def test_57_end_to_end_derived_exists(self):
        td,rt,r=run_example('06_END_TO_END_MAINFRAME.gen'); self.addCleanup(td.cleanup); self.assertEqual((Path(td.name)/'derived/materialized/payload.bin').read_bytes(),b'genesis-system-fixture')
    def test_58_end_to_end_audit_exists(self):
        td,rt,r=run_example('06_END_TO_END_MAINFRAME.gen'); self.addCleanup(td.cleanup); self.assertEqual((Path(td.name)/'audit/system.log').read_bytes(),b'genesis-system-fixture')
    def test_59_end_to_end_brane_z(self):
        td,rt,r=run_example('06_END_TO_END_MAINFRAME.gen'); self.addCleanup(td.cleanup); self.assertTrue(r.registers['realized']['M6']['Z'].startswith('z:'))
    def test_60_end_to_end_device(self):
        td,rt,r=run_example('06_END_TO_END_MAINFRAME.gen'); self.addCleanup(td.cleanup); self.assertEqual(r.registers['request']['status'],'ACCEPTED')
    def test_61_missing_source_capability(self):
        s=src('  endpoint source kind SOURCE mode READ root source\n  read source "x" as a\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_CAPABILITY_MISSING'): compile_source(s)
    def test_62_missing_write_capability(self):
        s=src('  capability io.source.read\n  endpoint source kind SOURCE mode READ root source\n  endpoint d kind DERIVED mode READ_WRITE root derived\n  read source "x" as a\n  write d "y" from a\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_CAPABILITY_MISSING'): compile_source(s)
    def test_63_missing_cas_capability(self):
        s=src('  capability io.source.read\n  endpoint source kind SOURCE mode READ root source\n  read source "x" as a\n  cas_put a as r\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_CAPABILITY_MISSING'): compile_source(s)
    def test_64_missing_brane_mount_capability(self):
        s=src('  port p role library module x version 1 dimension 5 contract 2.0 canonical READ_ONLY rewrite DERIVED_ONLY caps recover\n  mount p\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_CAPABILITY_MISSING'): compile_source(s)
    def test_65_unknown_endpoint(self):
        s=src('  capability io.source.read\n  read nope "x" as a\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_ENDPOINT_UNKNOWN'): compile_source(s)
    def test_66_write_source_rejected(self):
        s=src('  capability io.source.read\n  capability io.derived.write\n  endpoint source kind SOURCE mode READ root source\n  read source "x" as a\n  write source "y" from a\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_ENDPOINT_MODE'): compile_source(s)
    def test_67_read_audit_rejected(self):
        s=src('  capability io.source.read\n  endpoint audit kind AUDIT mode APPEND root audit\n  read audit "x" as a\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_ENDPOINT_MODE'): compile_source(s)
    def test_68_undefined_register(self):
        s=src('  capability cas.put\n  cas_put no as r\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_REGISTER_UNDEFINED'): compile_source(s)
    def test_69_redefined_register(self):
        s=src('  capability io.source.read\n  endpoint source kind SOURCE mode READ root source\n  read source "x" as a\n  read source "y" as a\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_REGISTER_REDEFINED'): compile_source(s)
    def test_70_unclosed_program(self):
        s=src('  capability io.source.read\n  endpoint source kind SOURCE mode READ root source\n  read source "x" as a')
        with self.assertRaisesRegex(Exception,'SYSTEM_PROGRAM_UNCLOSED'): compile_source(s)
    def test_71_after_close_rejected(self):
        s=src('  close\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_AFTER_CLOSE'): compile_source(s)
    def test_72_bad_version(self):
        with self.assertRaisesRegex(Exception,'SYSTEM_VERSION'): compile_source('genesis 0.5.0\nmodule t {\n close\n}\n')
    def test_73_duplicate_endpoint(self):
        s=src('  endpoint x kind SOURCE mode READ root a\n  endpoint x kind SOURCE mode READ root b\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_ENDPOINT_DUPLICATE'): parse_source(s)
    def test_74_duplicate_port(self):
        b='  port p role library module x version 1 dimension 5 contract 2.0 canonical READ_ONLY rewrite DERIVED_ONLY caps recover\n'
        with self.assertRaisesRegex(Exception,'BRANE_PORT_DUPLICATE'): parse_source(src(b+b+'  close'))
    def test_75_bad_port_static(self):
        s=src('  capability brane.mount\n  port p role library module x version 1 dimension 4 contract 2.0 canonical READ_ONLY rewrite DERIVED_ONLY caps recover\n  mount p\n  close')
        with self.assertRaisesRegex(Exception,'BRANE_PORT_INVALID'): compile_source(s)
    def test_76_unmounted_realize_static(self):
        s=src('  capability io.source.read\n  capability brane.realize\n  endpoint source kind SOURCE mode READ root source\n  port p role library module x version 1 dimension 5 contract 2.0 canonical READ_ONLY rewrite DERIVED_ONLY caps recover\n  read source "x" as a\n  realize p capability recover payload a as out\n  close')
        with self.assertRaisesRegex(Exception,'BRANE_PORT_NOT_MOUNTED'): compile_source(s)
    def test_77_unavailable_port_cap_static(self):
        s=src('  capability io.source.read\n  capability brane.mount\n  capability brane.realize\n  endpoint source kind SOURCE mode READ root source\n  port p role library module x version 1 dimension 5 contract 2.0 canonical READ_ONLY rewrite DERIVED_ONLY caps recover\n  read source "x" as a\n  mount p\n  realize p capability erase payload a as out\n  close')
        with self.assertRaisesRegex(Exception,'BRANE_CAPABILITY_UNAVAILABLE'): compile_source(s)
    def test_78_blackglass_wrong_endpoint(self):
        s=src('  capability io.source.read\n  capability blackglass.commit.propose\n  endpoint source kind SOURCE mode READ root source\n  read source "x" as a\n  propose source a as p\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_ENDPOINT_MODE'): compile_source(s)
    def test_79_device_wrong_endpoint(self):
        s=src('  capability device.request\n  endpoint x kind SOURCE mode READ root source\n  device x target speaker capability speech.output as req\n  close')
        with self.assertRaisesRegex(Exception,'SYSTEM_ENDPOINT_MODE'): compile_source(s)
    def test_80_runtime_path_escape(self):
        s=src('  capability io.source.read\n  endpoint source kind SOURCE mode READ root source\n  read source "../escape" as a\n  close')
        p=compile_source(s)
        with tempfile.TemporaryDirectory() as td:
            r=SystemRuntime(p,Path(td))
            with self.assertRaisesRegex(Exception,'SYSTEM_PATH_ESCAPE'): r.run()

if __name__=='__main__': unittest.main(verbosity=2)
