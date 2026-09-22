import unittest
from pathlib import Path
from genesis_concurrency import *
from genesis_concurrency.model import Op,TaskState,ResourceSpec,TaskTemplate,TaskOp,SpawnSpec,ConcurrentProgram

SEC=Path(__file__).resolve().parents[1]
EX=SEC/'15_EXAMPLES'

def comp(name): return compile_source((EX/name).read_text(),str(EX/name))
def run(name): return DeterministicScheduler(comp(name)).run()
def src(body): return 'genesis 0.5.0\nmodule t {\n'+body+'\n}\n'

class Section16Tests(unittest.TestCase):
    def test_01_parse_version(self): self.assertEqual(parse_source((EX/'01_ROUND_ROBIN.gen').read_text()).version,'0.5.0')
    def test_02_parse_module(self): self.assertEqual(comp('01_ROUND_ROBIN.gen').module,'round_robin')
    def test_03_parse_tasks(self): self.assertEqual(set(comp('01_ROUND_ROBIN.gen').templates),{'alpha','beta'})
    def test_04_parse_resource(self): self.assertEqual(comp('02_EXCLUSIVE_RESOURCE.gen').resources['fabric'].capacity,1)
    def test_05_parse_shared_capacity(self): self.assertEqual(comp('03_SHARED_CAPACITY.gen').resources['bus'].capacity,2)
    def test_06_parse_priority(self): self.assertEqual(comp('04_PRIORITY.gen').templates['high'].priority,20)
    def test_07_parse_quantum(self): self.assertEqual(comp('01_ROUND_ROBIN.gen').templates['alpha'].quantum,1)
    def test_08_parse_recursive_kind(self): self.assertEqual(comp('05_RECURSIVE_COOPERATIVE.gen').templates['walker'].kind,'RECURSIVE')
    def test_09_recursive_slice_inserted(self): self.assertEqual(comp('05_RECURSIVE_COOPERATIVE.gen').templates['walker'].ops[0].op,Op.RECURSION_SLICE)
    def test_10_parse_join(self): self.assertEqual(comp('01_ROUND_ROBIN.gen').joins,['a','b'])
    def test_11_round_robin_closed(self): self.assertEqual(run('01_ROUND_ROBIN.gen').status,'CLOSED')
    def test_12_exclusive_closed(self): self.assertEqual(run('02_EXCLUSIVE_RESOURCE.gen').status,'CLOSED')
    def test_13_shared_closed(self): self.assertEqual(run('03_SHARED_CAPACITY.gen').status,'CLOSED')
    def test_14_priority_closed(self): self.assertEqual(run('04_PRIORITY.gen').status,'CLOSED')
    def test_15_recursive_closed(self): self.assertEqual(run('05_RECURSIVE_COOPERATIVE.gen').status,'CLOSED')
    def test_16_deadlock_status(self): self.assertEqual(run('06_DEADLOCK_WITNESS.gen').status,'DEADLOCK')
    def test_17_deadlock_cycle_present(self): self.assertGreaterEqual(len(run('06_DEADLOCK_WITNESS.gen').receipt['cycle']),3)
    def test_18_round_robin_dispatch_alternates(self):
        r=run('01_ROUND_ROBIN.gen');ds=[e['task_id'] for e in r.events if e['kind']=='TASK_DISPATCH'][:4];self.assertNotEqual(ds[0],ds[1]);self.assertEqual(ds[0],ds[2])
    def test_19_priority_high_first(self):
        r=run('04_PRIORITY.gen');d=next(e for e in r.events if e['kind']=='TASK_DISPATCH');self.assertTrue(d['task_id'].endswith('-h'))
    def test_20_priority_high_closes_before_low_dispatches(self):
        r=run('04_PRIORITY.gen');ev=r.events;hc=next(i for i,e in enumerate(ev) if e['kind']=='TASK_CLOSE' and e['task_id'].endswith('-h'));ld=next(i for i,e in enumerate(ev) if e['kind']=='TASK_DISPATCH' and e['task_id'].endswith('-l'));self.assertLess(hc,ld)
    def test_21_exclusive_blocks(self): self.assertTrue(any(e['kind']=='RESOURCE_BLOCK' for e in run('02_EXCLUSIVE_RESOURCE.gen').events))
    def test_22_exclusive_wakes(self): self.assertTrue(any(e['kind']=='TASK_WAKE' for e in run('02_EXCLUSIVE_RESOURCE.gen').events))
    def test_23_shared_two_holders_overlap(self):
        r=run('03_SHARED_CAPACITY.gen');acq=[e for e in r.events if e['kind']=='RESOURCE_ACQUIRE'];rel=[i for i,e in enumerate(r.events) if e['kind']=='RESOURCE_RELEASE'];idx2=next(i for i,e in enumerate(r.events) if e['kind']=='RESOURCE_ACQUIRE' and e['event_id']==acq[1]['event_id']);self.assertLess(idx2,rel[0])
    def test_24_close_receipts(self): self.assertTrue(all(v['close_receipt'] for v in run('01_ROUND_ROBIN.gen').tasks.values()))
    def test_25_close_zero_leases(self): self.assertTrue(all(not v['leases'] for v in run('02_EXCLUSIVE_RESOURCE.gen').tasks.values()))
    def test_26_receipt_deterministic(self): self.assertEqual(run('01_ROUND_ROBIN.gen').receipt,run('01_ROUND_ROBIN.gen').receipt)
    def test_27_events_deterministic(self): self.assertEqual(run('03_SHARED_CAPACITY.gen').events,run('03_SHARED_CAPACITY.gen').events)
    def test_28_event_root_nonzero(self): self.assertNotEqual(run('01_ROUND_ROBIN.gen').receipt['event_root'],'0'*64)
    def test_29_resource_root_nonzero(self): self.assertNotEqual(run('02_EXCLUSIVE_RESOURCE.gen').receipt['resource_root'],'0'*64)
    def test_30_proof_root_nonzero(self): self.assertNotEqual(comp('01_ROUND_ROBIN.gen').metadata['verification']['proof_root'],'0'*64)
    def test_31_program_id_stable(self): self.assertEqual(comp('01_ROUND_ROBIN.gen').metadata['program_id'],comp('01_ROUND_ROBIN.gen').metadata['program_id'])
    def test_32_bytecode_deterministic(self): self.assertEqual(encode(comp('02_EXCLUSIVE_RESOURCE.gen')),encode(comp('02_EXCLUSIVE_RESOURCE.gen')))
    def test_33_bytecode_roundtrip(self):
        p=comp('03_SHARED_CAPACITY.gen');q=decode(encode(p));self.assertEqual(disassemble(p),disassemble(q))
    def test_34_bytecode_tamper(self):
        b=bytearray(encode(comp('01_ROUND_ROBIN.gen')));b[-1]^=1
        with self.assertRaisesRegex(Exception,'CONCURRENCY_BYTECODE_TAMPER'): decode(bytes(b))
    def test_35_disasm_resource(self): self.assertIn('RESOURCE fabric',disassemble(comp('02_EXCLUSIVE_RESOURCE.gen')))
    def test_36_disasm_acquire(self): self.assertIn('ACQUIRE',disassemble(comp('02_EXCLUSIVE_RESOURCE.gen')))
    def test_37_opcode_window(self): self.assertEqual((int(Op.WORK),int(Op.ASSERT)),(0x00A0,0x00A6))
    def test_38_unknown_join_rejected(self):
        with self.assertRaisesRegex(Exception,'JOIN_UNKNOWN_HANDLE'): compile_source(src('  task a priority 1 quantum 1 {\n    close\n  }\n  spawn a as x\n  join y'))
    def test_39_duplicate_handle_rejected(self):
        with self.assertRaisesRegex(Exception,'TASK_HANDLE_DUPLICATE'): compile_source(src('  task a priority 1 quantum 1 {\n    close\n  }\n  spawn a as x\n  spawn a as x\n  join x'))
    def test_40_unknown_template_rejected(self):
        with self.assertRaisesRegex(Exception,'TASK_TEMPLATE_UNKNOWN'): compile_source(src('  task a priority 1 quantum 1 {\n    close\n  }\n  spawn b as x\n  join x'))
    def test_41_bad_capacity_rejected(self):
        with self.assertRaisesRegex(Exception,'RESOURCE_CAPACITY'): compile_source(src('  resource r capacity 0\n  task a priority 1 quantum 1 {\n    close\n  }\n  spawn a as x\n  join x'))
    def test_42_bad_quantum_rejected(self):
        with self.assertRaisesRegex(Exception,'TASK_QUANTUM'): compile_source(src('  task a priority 1 quantum 0 {\n    close\n  }\n  spawn a as x\n  join x'))
    def test_43_bad_priority_rejected(self):
        with self.assertRaisesRegex(Exception,'TASK_PRIORITY'): compile_source(src('  task a priority 5000 quantum 1 {\n    close\n  }\n  spawn a as x\n  join x'))
    def test_44_unknown_resource_rejected(self):
        with self.assertRaisesRegex(Exception,'RESOURCE_UNKNOWN'): compile_source(src('  task a priority 1 quantum 1 {\n    acquire nope exclusive\n    close\n  }\n  spawn a as x\n  join x'))
    def test_45_double_acquire_rejected(self):
        with self.assertRaisesRegex(Exception,'RESOURCE_DOUBLE_ACQUIRE'): compile_source(src('  resource r capacity 1\n  task a priority 1 quantum 1 {\n    acquire r exclusive\n    acquire r exclusive\n    release r\n    close\n  }\n  spawn a as x\n  join x'))
    def test_46_release_without_acquire_rejected(self):
        with self.assertRaisesRegex(Exception,'RESOURCE_RELEASE_STATIC'): compile_source(src('  resource r capacity 1\n  task a priority 1 quantum 1 {\n    release r\n    close\n  }\n  spawn a as x\n  join x'))
    def test_47_resource_leak_rejected(self):
        with self.assertRaisesRegex(Exception,'TASK_RESOURCE_LEAK_STATIC'): compile_source(src('  resource r capacity 1\n  task a priority 1 quantum 1 {\n    acquire r exclusive\n    close\n  }\n  spawn a as x\n  join x'))
    def test_48_missing_close_rejected(self):
        with self.assertRaisesRegex(Exception,'TASK_UNCLOSED'): compile_source(src('  task a priority 1 quantum 1 {\n    work 1\n  }\n  spawn a as x\n  join x'))
    def test_49_zero_work_rejected(self):
        with self.assertRaisesRegex(Exception,'WORK_UNITS'): compile_source(src('  task a priority 1 quantum 1 {\n    work 0\n    close\n  }\n  spawn a as x\n  join x'))
    def test_50_bad_version_rejected(self):
        with self.assertRaisesRegex(Exception,'CONCURRENCY_VERSION'): parse_source('genesis 0.4.0\nmodule x {\n}')
    def test_51_cancellation_releases_resource(self):
        p=comp('02_EXCLUSIVE_RESOURCE.gen');s=DeterministicScheduler(p);a=s.handle_to_task['a'];t=s.tasks[a];lease=s.rm.acquire(a,'fabric','EXCLUSIVE',1);t.leases['fabric']=lease;self.assertTrue(s.cancel(a));self.assertEqual(s.rm.available('fabric'),1)
    def test_52_cancellation_state(self):
        s=DeterministicScheduler(comp('01_ROUND_ROBIN.gen'));a=s.handle_to_task['a'];s.cancel(a);self.assertEqual(s.tasks[a].state,TaskState.CANCELLED)
    def test_53_cancel_idempotent_false(self):
        s=DeterministicScheduler(comp('01_ROUND_ROBIN.gen'));a=s.handle_to_task['a'];s.cancel(a);self.assertFalse(s.cancel(a))
    def test_54_wait_graph_cycle(self):
        s=DeterministicScheduler(comp('06_DEADLOCK_WITNESS.gen'));r=s.run();self.assertEqual(r.status,'DEADLOCK');self.assertTrue(r.receipt['cycle'][0]==r.receipt['cycle'][-1])
    def test_55_tick_budget(self):
        with self.assertRaisesRegex(Exception,'SCHEDULER_TICK_BUDGET'): DeterministicScheduler(comp('01_ROUND_ROBIN.gen'),max_ticks=1).run()
    def test_56_recursive_has_suspend_events(self): self.assertTrue(any(e['kind']=='RECURSION_SLICE' and e['status']=='SUSPENDED' for e in run('05_RECURSIVE_COOPERATIVE.gen').events))
    def test_57_recursive_eventually_closes(self): self.assertTrue(any(e['kind']=='RECURSION_SLICE' and e['status']=='CLOSED' for e in run('05_RECURSIVE_COOPERATIVE.gen').events))
    def test_58_recursive_interleaves_observer(self):
        r=run('05_RECURSIVE_COOPERATIVE.gen');ds=[e['task_id'] for e in r.events if e['kind']=='TASK_DISPATCH'];self.assertGreater(len(set(ds[:4])),1)
    def test_59_continuation_roundtrip(self):
        t=make_token('x',0,1,5);a=run_slice(t,2);b=run_slice(a['continuation'],3);self.assertEqual((a['status'],b['status'],b['state']),('SUSPENDED','CLOSED',5))
    def test_60_continuation_tamper(self):
        t=make_token('x',0,1,5);t['state']=99
        with self.assertRaisesRegex(Exception,'RECURSION_CONTINUATION_INVALID'): validate_token(t)
    def test_61_exclusive_consumes_full_capacity(self):
        rm=ResourceManager({'r':ResourceSpec('r',3)});l=rm.acquire('a','r','EXCLUSIVE',1);self.assertEqual((l['units'],rm.available('r')),(3,0))
    def test_62_shared_capacity_enforced(self):
        rm=ResourceManager({'r':ResourceSpec('r',2)});self.assertIsNotNone(rm.acquire('a','r','SHARED',1));self.assertIsNotNone(rm.acquire('b','r','SHARED',1));self.assertIsNone(rm.acquire('c','r','SHARED',1))
    def test_63_shared_blocks_exclusive(self):
        rm=ResourceManager({'r':ResourceSpec('r',2)});rm.acquire('a','r','SHARED',1);self.assertIsNone(rm.acquire('b','r','EXCLUSIVE',2))
    def test_64_resource_snapshot_deterministic(self):
        rm=ResourceManager({'r':ResourceSpec('r',2)});rm.acquire('a','r','SHARED',1);self.assertEqual(rm.snapshot(),rm.snapshot())

if __name__=='__main__':unittest.main(verbosity=2)
