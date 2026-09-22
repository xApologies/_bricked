import unittest,tempfile
from pathlib import Path
from genesis_recursion import *
from genesis_recursion.model import Op

SEC=Path(__file__).resolve().parents[1]
EX=SEC/'15_EXAMPLES'

def comp(name): return compile_source((EX/name).read_text(),str(EX/name))
def run(name): return RecursiveVM().run(comp(name))
def src(body): return 'genesis 0.4.0\nmodule t {\n'+body+'\n}\n'

class Section15Tests(unittest.TestCase):
    def test_01_parse_countdown(self): self.assertEqual(parse_source((EX/'01_COUNTDOWN.gen').read_text()).version,'0.4.0')
    def test_02_parse_decreasing(self): self.assertEqual(parse_source((EX/'01_COUNTDOWN.gen').read_text()).functions[0].mode,'DECREASING')
    def test_03_parse_fuel(self): self.assertEqual(parse_source((EX/'04_FUEL_RECURSION.gen').read_text()).functions[0].mode,'FUEL')
    def test_04_parse_visit_once(self): self.assertEqual(parse_source((EX/'05_VISIT_ONCE.gen').read_text()).functions[0].mode,'VISIT_ONCE')
    def test_05_countdown_result(self): self.assertEqual(run('01_COUNTDOWN.gen').exports['result'],0)
    def test_06_fib_result(self): self.assertEqual(run('02_FIBONACCI.gen').exports['result'],55)
    def test_07_sum_result(self): self.assertEqual(run('03_SUM_ACCUMULATOR.gen').exports['result'],5050)
    def test_08_fuel_result(self): self.assertEqual(run('04_FUEL_RECURSION.gen').exports['result'],0)
    def test_09_visit_result(self): self.assertEqual(run('05_VISIT_ONCE.gen').exports['result'],0)
    def test_10_nested_result(self): self.assertEqual(run('06_NESTED_RECURSIVE_CALL.gen').exports['result'],0)
    def test_11_all_examples_compile(self):
        for p in EX.glob('*.gen'): compile_source(p.read_text(),str(p))
    def test_12_all_examples_halt(self):
        for p in EX.glob('*.gen'): self.assertTrue(RecursiveVM().run(compile_source(p.read_text(),str(p))).halted)
    def test_13_decreasing_metadata(self): self.assertEqual(comp('01_COUNTDOWN.gen').functions['countdown'].metric_param,'n')
    def test_14_recursive_edge_has_negative_delta(self):
        xs=[i for i in comp('01_COUNTDOWN.gen').instructions if i.op==Op.RCALL and i.attrs.get('recursive')]
        self.assertTrue(xs and xs[0].attrs['measure_delta']<0)
    def test_15_fib_has_two_recursive_edges(self):
        self.assertEqual(sum(i.op==Op.RCALL and i.attrs.get('recursive') for i in comp('02_FIBONACCI.gen').instructions),2)
    def test_16_frame_closures_equal_calls(self):
        r=run('01_COUNTDOWN.gen'); self.assertEqual(r.receipt['frames_closed'],9)
    def test_17_history_root_nonzero(self): self.assertNotEqual(run('01_COUNTDOWN.gen').receipt['history_root'],'0'*64)
    def test_18_run_deterministic(self): self.assertEqual(run('01_COUNTDOWN.gen').receipt,run('01_COUNTDOWN.gen').receipt)
    def test_19_bytecode_deterministic(self): self.assertEqual(encode(comp('02_FIBONACCI.gen')),encode(comp('02_FIBONACCI.gen')))
    def test_20_bytecode_roundtrip(self):
        p=comp('03_SUM_ACCUMULATOR.gen'); q=decode(encode(p)); self.assertEqual(disassemble(p),disassemble(q))
    def test_21_bytecode_tamper(self):
        b=bytearray(encode(comp('01_COUNTDOWN.gen'))); b[-1]^=1
        with self.assertRaises(Exception): decode(bytes(b))
    def test_22_disasm_rcall(self): self.assertIn('RCALL',disassemble(comp('01_COUNTDOWN.gen')))
    def test_23_disasm_close(self): self.assertIn('RECURSION_CLOSE',disassemble(comp('01_COUNTDOWN.gen')))
    def test_24_opcode_rcall_stable(self): self.assertEqual(int(Op.RCALL),0x0090)
    def test_25_opcode_resume_stable(self): self.assertEqual(int(Op.RESUME_RECURSION),0x0097)
    def test_26_unguarded_rejected(self):
        s=src('  rec fn f(n: INT) -> INT bogus n {\n    return n\n  }')
        with self.assertRaises(Exception): compile_source(s)
    def test_27_non_decreasing_rejected(self):
        s=src('  rec fn f(n: INT) -> INT decreases n max_depth 8 {\n    recur f(n) as x\n    return x\n  }\n  let a : INT = 1\n  call f(a) as r\n  export r : INT')
        with self.assertRaises(Exception): compile_source(s)
    def test_28_self_call_requires_recur(self):
        s=src('  rec fn f(n: INT) -> INT decreases n max_depth 8 {\n    call f(n) as x\n    return x\n  }')
        with self.assertRaises(Exception): compile_source(s)
    def test_29_recur_other_rejected(self):
        s=src('  rec fn a(n: INT) -> INT fuel 3 {\n    recur b(n) as x\n    return x\n  }\n  rec fn b(n: INT) -> INT fuel 3 {\n    return n\n  }')
        with self.assertRaises(Exception): compile_source(s)
    def test_30_missing_return_rejected(self):
        s=src('  rec fn f(n: INT) -> INT fuel 3 {\n    let x : INT = 1\n  }')
        with self.assertRaises(Exception): compile_source(s)
    def test_31_return_type_rejected(self):
        s=src('  rec fn f(n: INT) -> BOOL fuel 3 {\n    return n\n  }')
        with self.assertRaises(Exception): compile_source(s)
    def test_32_call_arity_rejected(self):
        s=src('  rec fn f(n: INT) -> INT fuel 3 {\n    return n\n  }\n  let a : INT = 1\n  call f() as r')
        with self.assertRaises(Exception): compile_source(s)
    def test_33_export_type_rejected(self):
        s=src('  let a : INT = 1\n  export a : BOOL')
        with self.assertRaises(Exception): compile_source(s)
    def test_34_depth_exceeded_runtime(self):
        s=(EX/'01_COUNTDOWN.gen').read_text().replace('max_depth 64','max_depth 3').replace('let start : INT = 8','let start : INT = 8')
        with self.assertRaisesRegex(Exception,'RECURSION_DEPTH_EXCEEDED'): RecursiveVM().run(compile_source(s))
    def test_35_fuel_exhaust_runtime(self):
        s=src('  rec fn spin(n: INT) -> INT fuel 2 {\n    let one : INT = 1\n    let next : INT = add n one\n    recur spin(next) as x\n    return x\n  }\n  let a : INT = 0\n  call spin(a) as r\n  export r : INT')
        with self.assertRaisesRegex(Exception,'RECURSION_FUEL_EXHAUSTED'): RecursiveVM().run(compile_source(s))
    def test_36_visit_repeat_runtime(self):
        s=src('  rec fn loop(node: INT) -> INT visit_once node max_depth 8 {\n    recur loop(node) as x\n    return x\n  }\n  let a : INT = 1\n  call loop(a) as r\n  export r : INT')
        with self.assertRaisesRegex(Exception,'RECURSION_VISIT_REPEAT'): RecursiveVM().run(compile_source(s))
    def test_37_step_budget(self):
        with self.assertRaisesRegex(Exception,'RECURSION_STEP_BUDGET'): RecursiveVM(max_steps=2).run(comp('01_COUNTDOWN.gen'))
    def test_38_topology_skip_cycle(self):
        r=TopologyRecursiveExecutor().walk('A',{'A':['B'],'B':['C'],'C':['A']},'skip'); self.assertEqual(r.visits,['A','B','C']); self.assertEqual(len(r.cycles),1)
    def test_39_topology_error_cycle(self):
        with self.assertRaisesRegex(Exception,'TOPOLOGY_CYCLE'): TopologyRecursiveExecutor().walk('A',{'A':['B'],'B':['A']},'error')
    def test_40_topology_dag(self):
        r=TopologyRecursiveExecutor().walk('A',{'A':['B','C'],'B':['D'],'C':[],'D':[]}); self.assertEqual(set(r.visits),{'A','B','C','D'})
    def test_41_topology_closure_reverse(self):
        r=TopologyRecursiveExecutor().walk('A',{'A':['B'],'B':[]}); self.assertEqual(r.closures,['B','A'])
    def test_42_topology_deterministic(self):
        a=TopologyRecursiveExecutor().walk(1,{1:[2,3],2:[],3:[]}); b=TopologyRecursiveExecutor().walk(1,{1:[2,3],2:[],3:[]}); self.assertEqual(a.receipt,b.receipt)
    def test_43_persistent_suspends(self):
        r=PersistentRecursiveTask('t',0,1,10).run_slice(3); self.assertEqual((r.status,r.state),('SUSPENDED',3)); self.assertIsNotNone(r.continuation)
    def test_44_persistent_resume(self):
        r=PersistentRecursiveTask('t',0,1,5).run_slice(2); t=PersistentRecursiveTask.resume(r.continuation); r2=t.run_slice(10); self.assertEqual((r2.status,r2.state),('CLOSED',5))
    def test_45_persistent_tamper(self):
        r=PersistentRecursiveTask('t',0,1,None).run_slice(1); tok=dict(r.continuation); tok['state']=999
        with self.assertRaisesRegex(Exception,'RECURSION_CONTINUATION_INVALID'): PersistentRecursiveTask.resume(tok)
    def test_46_persistent_unbounded_remains_suspended(self):
        r=PersistentRecursiveTask('forever',0,1,None).run_slice(10); self.assertEqual(r.status,'SUSPENDED')
    def test_47_persistent_deterministic(self):
        a=PersistentRecursiveTask('t',0,1,5).run_slice(2); b=PersistentRecursiveTask('t',0,1,5).run_slice(2); self.assertEqual(a.continuation,b.continuation)
    def test_48_linear_ledger_safe_empty(self): self.assertTrue(LinearFrameLedger().assert_boundary_safe())
    def test_49_linear_ledger_rejects_portal(self):
        l=LinearFrameLedger(); l.open('PORTAL','p1')
        with self.assertRaisesRegex(Exception,'RECURSION_LINEAR_RESOURCE_CAPTURE'): l.assert_boundary_safe()
    def test_50_linear_ledger_close(self):
        l=LinearFrameLedger(); l.open('QSTATE','q1'); l.close('q1'); self.assertTrue(l.assert_boundary_safe())
    def test_51_verifier_name(self): self.assertEqual(comp('01_COUNTDOWN.gen').metadata['verification']['verifier'],'RECURSIVE_CFG_V0_1')
    def test_52_program_id_stable(self): self.assertEqual(comp('01_COUNTDOWN.gen').metadata['program_id'],comp('01_COUNTDOWN.gen').metadata['program_id'])
    def test_53_frame_receipts_closed(self): self.assertTrue(all(x['closed'] for x in run('02_FIBONACCI.gen').frames))
    def test_54_max_depth_recorded(self): self.assertGreaterEqual(run('01_COUNTDOWN.gen').receipt['max_depth'],8)
    def test_55_fib_frame_count(self): self.assertGreater(run('02_FIBONACCI.gen').receipt['frames_closed'],100)
    def test_56_parser_bad_version(self):
        with self.assertRaises(Exception): parse_source('genesis 0.3.0\nmodule x {\n}')
    def test_57_duplicate_param(self):
        with self.assertRaises(Exception): parse_source(src('  rec fn f(n: INT, n: INT) -> INT fuel 2 {\n    return n\n  }'))
    def test_58_metric_not_param(self):
        with self.assertRaises(Exception): parse_source(src('  rec fn f(n: INT) -> INT decreases x max_depth 2 {\n    return n\n  }'))
    def test_59_depth_range_rejected(self):
        with self.assertRaises(Exception): compile_source(src('  rec fn f(n: INT) -> INT decreases n max_depth 5000 {\n    return n\n  }'))
    def test_60_topology_history_root_nonzero(self): self.assertNotEqual(TopologyRecursiveExecutor().walk('A',{'A':[]}).history_root,'0'*64)

if __name__=='__main__': unittest.main(verbosity=2)
