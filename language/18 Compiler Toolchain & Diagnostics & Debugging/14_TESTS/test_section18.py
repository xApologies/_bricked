from __future__ import annotations
import json,os,subprocess,sys,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REF=ROOT/"12_REFERENCE_IMPLEMENTATION"
sys.path.insert(0,str(REF))

from genesis_toolchain import BuildDriver,compare_rebuilds,TracingRuntime,DebugSession,TestRunner
from genesis_toolchain.diagnostics import render
from genesis_toolchain.source_map import build_source_map
from genesis_system_io.compiler import compile_source
from genesis_system_io.bytecode import decode
from genesis_system_io.errors import GenesisSystemError

GOOD='''genesis 0.6.0
module source_read {
  capability io.source.read
  capability cas.put
  capability cas.get
  endpoint source kind SOURCE mode READ root source
  read source "input.bin" as raw
  cas_put raw as ref
  cas_get ref as restored
  assert_eq raw restored
  close
}
'''

def run_trace(text=GOOD):
    p=compile_source(text,"test.gen")
    td=tempfile.TemporaryDirectory(); rt=TracingRuntime(p,Path(td.name)); rt.seed("source","input.bin",b"abc"); rr=rt.run(); return td,rt,rr

class Section18Tests(unittest.TestCase):
    def test_check_good(self): self.assertTrue(BuildDriver().check_text(GOOD,"x.gen").ok)
    def test_check_unclosed_diag(self):
        r=BuildDriver().check_text(GOOD.replace("  close\n",""),"x.gen"); self.assertFalse(r.ok); self.assertEqual(r.diagnostics[0].code,"SYSTEM_PROGRAM_UNCLOSED")
    def test_check_undefined_register_diag(self):
        s='''genesis 0.6.0\nmodule x {\n capability cas.put\n cas_put nope as ref\n close\n}\n'''
        r=BuildDriver().check_text(s,"x.gen"); self.assertEqual(r.diagnostics[0].code,"SYSTEM_REGISTER_UNDEFINED")
    def test_check_bad_version(self):
        r=BuildDriver().check_text(GOOD.replace("0.6.0","9.9.9"),"x.gen"); self.assertEqual(r.diagnostics[0].code,"SYSTEM_VERSION")
    def test_diagnostic_id_stable(self):
        s=GOOD.replace("  close\n",""); a=BuildDriver().check_text(s,"x.gen").diagnostics[0]; b=BuildDriver().check_text(s,"x.gen").diagnostics[0]; self.assertEqual(a.diagnostic_id,b.diagnostic_id)
    def test_diagnostic_render_has_code(self):
        d=BuildDriver().check_text(GOOD.replace("  close\n",""),"x.gen").diagnostics[0]; self.assertIn("SYSTEM_PROGRAM_UNCLOSED",render(d))
    def test_parse_error_has_span(self):
        s=GOOD.replace('read source "input.bin" as raw','nonsense xyz')
        d=BuildDriver().check_text(s,"x.gen").diagnostics[0]; self.assertIsNotNone(d.span); self.assertGreater(d.span.line,0)
    def test_build_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            r=BuildDriver().build_text(GOOD,Path(td),"x.gen"); self.assertTrue(r.ok)
            for n in ["bytecode.gio","disassembly.txt","proof.json","source_map.json","build_manifest.json"]: self.assertTrue((Path(td)/n).is_file())
    def test_bytecode_decodes(self):
        with tempfile.TemporaryDirectory() as td:
            r=BuildDriver().build_text(GOOD,Path(td),"x.gen"); p=decode((Path(td)/"bytecode.gio").read_bytes()); self.assertEqual(p.module,"source_read")
    def test_manifest_program_id(self):
        with tempfile.TemporaryDirectory() as td:
            r=BuildDriver().build_text(GOOD,Path(td),"x.gen"); self.assertTrue(r.manifest.program_id.startswith("sysprog:"))
    def test_manifest_proof_root(self):
        with tempfile.TemporaryDirectory() as td:
            r=BuildDriver().build_text(GOOD,Path(td),"x.gen"); self.assertTrue(r.manifest.proof_root)
    def test_manifest_artifacts_four_semantic(self):
        with tempfile.TemporaryDirectory() as td:
            r=BuildDriver().build_text(GOOD,Path(td),"x.gen"); self.assertEqual(len(r.manifest.artifacts),4)
    def test_reproducible(self): self.assertTrue(compare_rebuilds(GOOD,"x.gen")["ok"])
    def test_repro_artifacts_all_equal(self): self.assertTrue(all(compare_rebuilds(GOOD,"x.gen")["artifacts"].values()))
    def test_build_id_changes_source(self):
        a=BuildDriver().check_text(GOOD,"x.gen").manifest.build_id; b=BuildDriver().check_text(GOOD+"#x\n","x.gen").manifest.build_id; self.assertNotEqual(a,b)
    def test_build_id_changes_profile(self):
        a=BuildDriver(profile="debug").check_text(GOOD,"x.gen").manifest.build_id; b=BuildDriver(profile="release").check_text(GOOD,"x.gen").manifest.build_id; self.assertNotEqual(a,b)
    def test_build_id_changes_target(self):
        a=BuildDriver(target="a").check_text(GOOD,"x.gen").manifest.build_id; b=BuildDriver(target="b").check_text(GOOD,"x.gen").manifest.build_id; self.assertNotEqual(a,b)
    def test_build_id_changes_option(self):
        a=BuildDriver(options={"x":1}).check_text(GOOD,"x.gen").manifest.build_id; b=BuildDriver(options={"x":2}).check_text(GOOD,"x.gen").manifest.build_id; self.assertNotEqual(a,b)
    def test_build_id_independent_output_dir(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            x=BuildDriver().build_text(GOOD,Path(a),"x.gen").manifest.build_id; y=BuildDriver().build_text(GOOD,Path(b),"x.gen").manifest.build_id; self.assertEqual(x,y)
    def test_source_map_count(self):
        p=compile_source(GOOD,"x.gen"); sm=build_source_map(p,GOOD,"x.gen"); self.assertEqual(len(sm),len(p.instructions))
    def test_source_map_first_read_line(self):
        p=compile_source(GOOD,"x.gen"); sm=build_source_map(p,GOOD,"x.gen"); self.assertEqual(sm[0].opcode,"READ"); self.assertEqual(sm[0].line,7)
    def test_source_map_close(self):
        p=compile_source(GOOD,"x.gen"); sm=build_source_map(p,GOOD,"x.gen"); self.assertEqual(sm[-1].opcode,"SYS_CLOSE")
    def test_trace_closed(self):
        td,rt,rr=run_trace(); self.assertEqual(rr.status,"CLOSED"); td.cleanup()
    def test_trace_event_count(self):
        td,rt,rr=run_trace(); self.assertEqual(len(rr.events),5); td.cleanup()
    def test_trace_receipt_count(self):
        td,rt,rr=run_trace(); self.assertEqual(len(rr.receipts),5); td.cleanup()
    def test_trace_registers(self):
        td,rt,rr=run_trace(); self.assertEqual(rr.registers["raw"],b"abc"); self.assertEqual(rr.registers["restored"],b"abc"); td.cleanup()
    def test_trace_delta_read(self):
        td,rt,rr=run_trace(); self.assertEqual(rr.events[0].register_delta,("raw",)); td.cleanup()
    def test_trace_delta_cas_put(self):
        td,rt,rr=run_trace(); self.assertEqual(rr.events[1].register_delta,("ref",)); td.cleanup()
    def test_trace_close_no_delta(self):
        td,rt,rr=run_trace(); self.assertEqual(rr.events[-1].register_delta,()); td.cleanup()
    def test_trace_root_nonzero(self):
        td,rt,rr=run_trace(); self.assertNotEqual(rr.receipt_root,"0"*64); td.cleanup()
    def test_trace_roots_change(self):
        td,rt,rr=run_trace(); roots=[e.provenance_root for e in rr.events]; self.assertEqual(len(set(roots)),len(roots)); td.cleanup()
    def test_trace_snapshot_bytes_safe(self):
        td,rt,rr=run_trace(); self.assertEqual(rr.events[0].registers["raw"]["$bytes_hex"],"616263"); td.cleanup()
    def test_debug_step(self):
        td,rt,rr=run_trace(); d=DebugSession(rr); self.assertEqual(d.step().opcode,"READ"); self.assertEqual(d.step().opcode,"CAS_PUT"); td.cleanup()
    def test_debug_seek(self):
        td,rt,rr=run_trace(); d=DebugSession(rr); self.assertEqual(d.seek(3).opcode,"ASSERT_EQ"); td.cleanup()
    def test_debug_registers(self):
        td,rt,rr=run_trace(); d=DebugSession(rr); d.seek(2); self.assertIn("restored",d.registers()); td.cleanup()
    def test_debug_receipt(self):
        td,rt,rr=run_trace(); d=DebugSession(rr); d.seek(1); self.assertEqual(d.receipt()["operation"],"CAS_PUT"); td.cleanup()
    def test_debug_opcode_breakpoint(self):
        td,rt,rr=run_trace(); d=DebugSession(rr); d.add_opcode_breakpoint("ASSERT_EQ"); ev=d.continue_run(); self.assertEqual(ev.opcode,"ASSERT_EQ"); td.cleanup()
    def test_debug_line_breakpoint(self):
        td,rt,rr=run_trace(); d=DebugSession(rr); d.add_line_breakpoint("test.gen",8); ev=d.continue_run(); self.assertEqual(ev.opcode,"CAS_PUT"); td.cleanup()
    def test_debug_end(self):
        td,rt,rr=run_trace(); d=DebugSession(rr); [d.step() for _ in rr.events]; self.assertIsNone(d.step()); td.cleanup()
    def test_debug_bad_seek(self):
        td,rt,rr=run_trace(); d=DebugSession(rr); self.assertRaises(IndexError,d.seek,999); td.cleanup()
    def test_test_runner_good(self):
        p=ROOT/"15_EXAMPLES/tests/source_read.gtest.json"; self.assertTrue(TestRunner().run_case(p)["pass"])
    def test_test_runner_expected_failure(self):
        p=ROOT/"15_EXAMPLES/tests/bad_unclosed.gtest.json"; self.assertTrue(TestRunner().run_case(p)["pass"])
    def test_test_runner_many(self):
        ps=[ROOT/"15_EXAMPLES/tests/source_read.gtest.json",ROOT/"15_EXAMPLES/tests/bad_register.gtest.json"]; r=TestRunner().run_many(ps); self.assertTrue(r["pass"]); self.assertEqual(r["count"],2)
    def test_verifier_not_bypassed(self):
        s=GOOD.replace("  capability cas.put\n",""); r=BuildDriver().check_text(s,"x.gen"); self.assertFalse(r.ok); self.assertEqual(r.diagnostics[0].code,"SYSTEM_CAPABILITY_MISSING")
    def test_after_close_rejected(self):
        s=GOOD.replace("  close\n","  close\n  close\n"); r=BuildDriver().check_text(s,"x.gen"); self.assertEqual(r.diagnostics[0].code,"SYSTEM_AFTER_CLOSE")
    def test_endpoint_unknown_rejected(self):
        s=GOOD.replace('read source "input.bin" as raw','read missing "input.bin" as raw'); r=BuildDriver().check_text(s,"x.gen"); self.assertEqual(r.diagnostics[0].code,"SYSTEM_ENDPOINT_UNKNOWN")
    def test_register_redefinition_rejected(self):
        s=GOOD.replace('cas_get ref as restored','cas_get ref as raw'); r=BuildDriver().check_text(s,"x.gen"); self.assertEqual(r.diagnostics[0].code,"SYSTEM_REGISTER_REDEFINED")
    def test_comment_is_accepted(self): self.assertTrue(BuildDriver().check_text(GOOD.replace("module source_read {","module source_read {\n # hi"),"x.gen").ok)
    def test_blank_lines_accepted(self): self.assertTrue(BuildDriver().check_text(GOOD.replace("module source_read {","module source_read {\n\n"),"x.gen").ok)
    def test_build_file(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"x.gen"; p.write_text(GOOD); r=BuildDriver().build_file(p,Path(td)/"out"); self.assertTrue(r.ok)
    def test_disassembly_contains_ops(self):
        with tempfile.TemporaryDirectory() as td:
            BuildDriver().build_text(GOOD,Path(td),"x.gen"); s=(Path(td)/"disassembly.txt").read_text(); self.assertIn("CAS_PUT",s); self.assertIn("SYS_CLOSE",s)
    def test_proof_json_valid(self):
        with tempfile.TemporaryDirectory() as td:
            BuildDriver().build_text(GOOD,Path(td),"x.gen"); d=json.loads((Path(td)/"proof.json").read_text()); self.assertIn("proof_root",d)
    def test_sourcemap_json_valid(self):
        with tempfile.TemporaryDirectory() as td:
            BuildDriver().build_text(GOOD,Path(td),"x.gen"); d=json.loads((Path(td)/"source_map.json").read_text()); self.assertEqual(d[0]["opcode"],"READ")
    def test_manifest_json_valid(self):
        with tempfile.TemporaryDirectory() as td:
            BuildDriver().build_text(GOOD,Path(td),"x.gen"); d=json.loads((Path(td)/"build_manifest.json").read_text()); self.assertTrue(d["build_id"].startswith("build:"))

# Build every valid Section 17 example through the Section 18 driver.
def _make_example_test(path):
    def test(self):
        text=path.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as td:
            r=BuildDriver().build_text(text,Path(td),path.name); self.assertTrue(r.ok,path.name)
    return test
for i,p in enumerate(sorted((ROOT/"15_EXAMPLES").glob("0[1-7]_*.gen")),1):
    setattr(Section18Tests,f"test_example_build_{i:02d}",_make_example_test(p))

# A deterministic matrix of compiler-driver configurations. Each is a separate
# contract test rather than a repeated assertion: target/profile/options are
# all part of build identity but not permission to change semantic verification.
def _make_config_test(i):
    def test(self):
        d=BuildDriver(target=f"gcm-test-{i%3}",profile="debug" if i%2==0 else "release",options={"matrix":i})
        r=d.check_text(GOOD,"matrix.gen"); self.assertTrue(r.ok); self.assertEqual(r.manifest.options["matrix"],i)
    return test
for i in range(1,17): setattr(Section18Tests,f"test_driver_configuration_{i:02d}",_make_config_test(i))

if __name__=="__main__": unittest.main(verbosity=2)
