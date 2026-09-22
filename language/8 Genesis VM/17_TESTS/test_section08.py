import json, sys, unittest, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'13_REFERENCE_IMPLEMENTATION'))
from genesis_vm import *
from genesis_vm.errors import GIRCompileError, VerifyError, BytecodeError, RuntimeFault
from genesis_vm.model import Program, Instruction, Opcode, TypeTag

class Section08Tests(unittest.TestCase):
    def load(self,name): return json.loads((ROOT/'18_EXAMPLES'/name).read_text())
    def compile(self,name): return compile_gir(self.load(name))
    def test_01_schedule_independent_of_json_order(self):
        g=self.load('FIRST_PORTAL.gir.json'); p1=compile_gir(g)
        g['nodes']=list(reversed(g['nodes'])); p2=compile_gir(g)
        self.assertEqual(encode(p1),encode(p2))
    def test_02_cycle_rejected(self):
        g={'ir':'GIR','version':'0.1','name':'cycle','nodes':[{'id':'a','op':'NOP'},{'id':'b','op':'NOP'}],'edges':[{'from':'a','to':'b','kind':'dependency'},{'from':'b','to':'a','kind':'dependency'}]}
        with self.assertRaises(GIRCompileError): compile_gir(g)
    def test_03_unknown_value_rejected(self):
        g={'ir':'GIR','version':'0.1','name':'bad','nodes':[{'id':'a','op':'HASH','out':'%h','type':'HASH','args':['%x']}]}
        with self.assertRaises(GIRCompileError): compile_gir(g)
    def test_04_first_portal_verifies(self): self.assertTrue(verify(self.compile('FIRST_PORTAL.gir.json'))['ok'])
    def test_05_rainbow_verifies(self): self.assertTrue(verify(self.compile('RAINBOW_ROAD.gir.json'))['ok'])
    def test_06_mixed_verifies(self): self.assertTrue(verify(self.compile('MIXED_SECTOR.gir.json'))['ok'])
    def test_07_quantum_verifies(self): self.assertTrue(verify(self.compile('QUANTUM_EFFECT.gir.json'))['ok'])
    def test_08_bytecode_roundtrip_first(self):
        p=self.compile('FIRST_PORTAL.gir.json'); q=decode(encode(p)); self.assertEqual(encode(p),encode(q))
    def test_09_bytecode_roundtrip_quantum(self):
        p=self.compile('QUANTUM_EFFECT.gir.json'); q=decode(encode(p)); self.assertEqual(encode(p),encode(q))
    def test_10_corrupt_bytecode_rejected(self):
        b=bytearray(encode(self.compile('FIRST_PORTAL.gir.json'))); b[-1]^=1
        with self.assertRaises(BytecodeError): decode(bytes(b))
    def test_11_first_portal_runs(self):
        r=VM().run(self.compile('FIRST_PORTAL.gir.json')); self.assertTrue(r.halted); self.assertEqual(len(r.exports),4)
    def test_12_rainbow_runs(self): self.assertTrue(VM().run(self.compile('RAINBOW_ROAD.gir.json')).halted)
    def test_13_mixed_runs(self): self.assertTrue(VM().run(self.compile('MIXED_SECTOR.gir.json')).halted)
    def test_14_quantum_runs(self): self.assertTrue(VM().run(self.compile('QUANTUM_EFFECT.gir.json')).halted)
    def test_15_execution_deterministic(self):
        p=self.compile('FIRST_PORTAL.gir.json'); a=VM().run(p); b=VM().run(p)
        self.assertEqual(a.receipt['content_hash'],b.receipt['content_hash'])
    def test_16_first_portal_export_geometric(self):
        p=self.compile('FIRST_PORTAL.gir.json'); r=VM().run(p); g=r.exports[p.exports[0]].value; self.assertEqual(g['kind'],'GEOMETRIC')
    def test_17_first_portal_receipt_closed(self):
        p=self.compile('FIRST_PORTAL.gir.json'); r=VM().run(p); rec=r.exports[p.exports[1]].value; self.assertEqual(rec['payload']['op'],'PORTAL_CLOSE')
    def test_18_brane_lift_m5(self):
        p=self.compile('FIRST_PORTAL.gir.json'); r=VM().run(p); m5=r.exports[p.exports[2]].value; self.assertEqual(m5['kind'],'M5')
    def test_19_quantum_measure_result_classical(self):
        p=self.compile('QUANTUM_EFFECT.gir.json'); r=VM().run(p); qr=r.exports[p.exports[0]].value; self.assertTrue(qr['payload']['classical'])
    def test_20_quantum_linear_reuse_rejected_static(self):
        g=self.load('QUANTUM_EFFECT.gir.json')
        # add a second consumer of already-consumed q0
        g['nodes'].append({'id':'10_bad','op':'Q_MEASURE','out':'%bad','type':'QRESULT','args':['%q0'],'attrs':{'outcome':1}})
        p=compile_gir(g)
        with self.assertRaises(VerifyError): verify(p)
    def test_21_qstate_generic_move_runtime_forbidden(self):
        p=Program('qmove',instructions=[Instruction(Opcode.CONST,0,(),{'value':{'kind':'QSTATE'}},'a',TypeTag.QSTATE),Instruction(Opcode.MOVE,1,(0,),{},'b',TypeTag.QSTATE)],exports=[])
        # verifier does not claim CONST is a valid quantum allocator; runtime still blocks generic MOVE.
        verify(p)
        with self.assertRaises(RuntimeFault): VM().run(p)
    def test_22_use_before_define(self):
        p=Program('bad',instructions=[Instruction(Opcode.HASH,1,(0,),{},'x',TypeTag.HASH)])
        with self.assertRaises(VerifyError): verify(p)
    def test_23_register_redefinition(self):
        p=Program('bad',instructions=[Instruction(Opcode.CONST,0,(),{'value':1},'a',TypeTag.INT),Instruction(Opcode.CONST,0,(),{'value':2},'b',TypeTag.INT)])
        with self.assertRaises(VerifyError): verify(p)
    def test_24_invalid_jump(self):
        p=Program('bad',instructions=[Instruction(Opcode.JUMP,None,(),{'target':9},'a',TypeTag.VOID)])
        with self.assertRaises(VerifyError): verify(p)
    def test_25_unclosed_portal_static(self):
        # minimal typed constants to reach PORTAL_OPEN
        p=Program('bad',instructions=[
            Instruction(Opcode.CONST,0,(),{'value':{}},'g',TypeTag.GEOMETRIC),
            Instruction(Opcode.CONST,1,(),{'value':{}},'a',TypeTag.ADMISSION),
            Instruction(Opcode.PORTAL_OPEN,2,(0,1),{'sector':'GR'},'p',TypeTag.PORTAL)],exports=[])
        with self.assertRaises(VerifyError): verify(p)
    def test_26_overlay_does_not_change_base_resource(self):
        b=ReferenceBackend(); f=b.mount_fabric('fabric://x'); before=f['content_hash']; b.write_overlay(f,'A',{'v':1}); self.assertEqual(before,f['content_hash'])
    def test_27_bridge_requires_change(self):
        b=ReferenceBackend(); f=b.mount_fabric('x'); reg=b.alloc(f,1); g=b.instantiate(f,reg,{'h':'m'})
        from genesis_vm.errors import SectorError
        with self.assertRaises(SectorError): b.bridge(g,'QFT','QFT',{})
    def test_28_portal_transport_requires_open(self):
        b=ReferenceBackend(); f=b.mount_fabric('x'); reg=b.alloc(f,1); g=b.instantiate(f,reg,{'h':'m'}); a=b.admit(g,{}); p=b.portal_open(g,a,'GR',{}); d=b.portal_transport(p,g,{}); b.portal_close(p,d)
        from genesis_vm.errors import ClosureError
        with self.assertRaises(ClosureError): b.portal_transport(p,g,{})
    def test_29_bytecode_magic(self): self.assertEqual(encode(self.compile('FIRST_PORTAL.gir.json'))[:4],b'GVM1')
    def test_30_disasm_contains_portal(self): self.assertIn('PORTAL_OPEN',disassemble(self.compile('FIRST_PORTAL.gir.json')))
    def test_31_all_outputs_unique(self):
        p=self.compile('RAINBOW_ROAD.gir.json'); outs=[i.out for i in p.instructions if i.out is not None]; self.assertEqual(len(outs),len(set(outs)))
    def test_32_gir_hash_present(self): self.assertEqual(len(self.compile('FIRST_PORTAL.gir.json').metadata['gir_hash']),64)
    def test_33_backend_abi_present(self): self.assertEqual(self.compile('FIRST_PORTAL.gir.json').metadata['required_backend_abi'],'0.1')
    def test_34_portal_receipt_in_ledger(self):
        vm=VM(); vm.run(self.compile('FIRST_PORTAL.gir.json')); self.assertTrue(any(r['payload'].get('op')=='PORTAL_CLOSE' for r in vm.backend.ledger))
    def test_35_road_receipt_in_ledger(self):
        vm=VM(); vm.run(self.compile('RAINBOW_ROAD.gir.json')); self.assertTrue(any(r['payload'].get('op')=='ROAD_CLOSE' for r in vm.backend.ledger))
    def test_36_mixed_has_bridge_resource(self):
        p=self.compile('MIXED_SECTOR.gir.json'); r=VM().run(p); b=r.exports[p.exports[1]].value; self.assertEqual(b['kind'],'BRIDGE')
    def test_37_measure_consumes_state_runtime(self):
        b=ReferenceBackend(); f=b.mount_fabric('x'); reg=b.alloc(f,1); g=b.instantiate(f,reg,{'h':'m'}); q=b.q_prepare(g,{}); b.q_measure(q,{'outcome':0}); self.assertEqual(q['typestate'],'MEASURED')
    def test_38_q_successor_moves_source(self):
        b=ReferenceBackend(); f=b.mount_fabric('x'); reg=b.alloc(f,1); g=b.instantiate(f,reg,{'h':'m'}); q=b.q_prepare(g,{}); q2=b.q_successor('SUPERPOSE',[q],{}); self.assertEqual(q['typestate'],'MOVED'); self.assertEqual(q2['typestate'],'OWNED')
    def test_39_execution_receipt_kind(self): self.assertEqual(VM().run(self.compile('FIRST_PORTAL.gir.json')).receipt['kind'],'RECEIPT')
    def test_40_reference_program_count(self): self.assertEqual(len(list((ROOT/'18_EXAMPLES').glob('*.gir.json'))),4)

if __name__=='__main__': unittest.main()
