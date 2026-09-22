import unittest,math,random,sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'12_REFERENCE_IMPLEMENTATION'))
from genesis_quantum_effects import *
from genesis_quantum_effects.superposition import superpose
from genesis_quantum_effects.entanglement import bell_pair,reduced_two_level,is_entangled_reference,tensor_product
from genesis_quantum_effects.channels import *
from genesis_quantum_effects.state import diagnostics,pure_fidelity,StateFactory
from genesis_quantum_effects.linalg import trace,purity
from genesis_quantum_effects.measurement import MeasurementEngine
from genesis_quantum_effects.effects import EffectChecker
from genesis_quantum_effects.audit import audit_transition
from genesis_quantum_effects.portal import QuantumPortalEngine
from genesis_quantum_effects.bridge_policy import QuantumBridgePolicy
from genesis_quantum_effects.brane import QuantumEffectBraneAdapter
from genesis_quantum_effects.ledger import Ledger
from genesis_quantum_effects.errors import *

class T(unittest.TestCase):
    def q0(self): return StateFactory.pure(['0','1'],[1,0],source_instance_id='I',canonical_mmo_id='M')
    def qp(self): return StateFactory.pure(['0','1'],[1,1],source_instance_id='I',canonical_mmo_id='M')
    def test_01_normalize(self): self.assertAlmostEqual(diagnostics(self.qp())['norm'],1)
    def test_02_zero_norm(self):
        with self.assertRaises(NormalizationError): StateFactory.pure(['0'],[0])
    def test_03_density_trace(self): self.assertAlmostEqual(diagnostics(StateFactory.density(['0','1'],[[.5,0],[0,.5]]))['trace'],1)
    def test_04_density_bad_trace(self):
        with self.assertRaises(NormalizationError): StateFactory.density(['0','1'],[[1,0],[0,1]])
    def test_05_density_bad_hermitian(self):
        with self.assertRaises(StateValidationError): StateFactory.density(['0','1'],[[.5,.2],[.1,.5]])
    def test_06_superposition(self): self.assertGreater(diagnostics(self.qp())['coherence_l1'],0)
    def test_07_hadamard(self):
        out=hadamard_channel().apply(self.q0()); self.assertAlmostEqual(abs(complex(*out.amplitudes[0]))**2,.5)
    def test_08_unitary_invalid(self):
        with self.assertRaises(ChannelValidationError): QuantumChannel(ChannelClass.UNITARY,[[[1,1],[0,1]]])
    def test_09_dephase_trace(self): self.assertAlmostEqual(diagnostics(dephasing_channel(.5).apply(self.qp()))['trace'],1)
    def test_10_dephase_coherence(self): self.assertLess(diagnostics(dephasing_channel(.5).apply(self.qp()))['coherence_l1'],diagnostics(self.qp())['coherence_l1']+1e-9)
    def test_11_fidelity_self(self): self.assertAlmostEqual(pure_fidelity(self.qp(),self.qp()),1)
    def test_12_bell(self): self.assertTrue(is_entangled_reference(bell_pair('A','B')))
    def test_13_reduced_mixed(self):
        r=reduced_two_level(bell_pair('A','B')); self.assertAlmostEqual(purity(r),.5)
    def test_14_tensor_product(self): self.assertEqual(len(tensor_product(self.q0(),self.q0(),['A','B']).basis),4)
    def test_15_claim(self):
        R=LinearOwnershipRegistry(); q=self.q0(); rec=R.claim(q,'A'); self.assertEqual(rec.owner,'A')
    def test_16_double_claim(self):
        R=LinearOwnershipRegistry(); q=self.q0(); R.claim(q,'A')
        with self.assertRaises(OwnershipError): R.claim(q,'B')
    def test_17_borrow(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A'); R.borrow_metadata(q.state_id,r.token); self.assertEqual(R.records[q.state_id].status,'OWNED')
    def test_18_move(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A'); r2=R.move(q.state_id,r.token,'B'); self.assertEqual(r2.owner,'B')
    def test_19_no_clone(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A')
        with self.assertRaises(NoCloningError): R.clone(q,r.token)
    def test_20_consumed(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A'); R.consume(q.state_id,r.token)
        with self.assertRaises(ConsumedStateError): R.assert_owned(q.state_id,r.token)
    def test_21_measure(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A'); out,post,rec=MeasurementEngine(R).measure_basis(q,r.token,random.Random(1)); self.assertEqual(out,'0'); self.assertEqual(post.kind,'MEASURED')
    def test_22_measure_consumes(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A'); MeasurementEngine(R).measure_basis(q,r.token,random.Random(1)); self.assertEqual(R.records[q.state_id].status,'CONSUMED')
    def test_23_effect_qft(self): self.assertTrue(EffectChecker().check(Effect.UNITARY,'PURE','QFT')['admitted'])
    def test_24_effect_gr_reject(self):
        with self.assertRaises(QuantumSectorViolation): EffectChecker().check(Effect.UNITARY,'PURE','GR')
    def test_25_effect_typestate_reject(self):
        with self.assertRaises(EffectViolation): EffectChecker().check(Effect.UNITARY,'MEASURED','QFT')
    def test_26_audit_identity(self): self.assertTrue(audit_transition(self.q0(),self.q0(),QuantumPreservation(min_fidelity=1))['pass'])
    def test_27_audit_fidelity_fail(self):
        q1=StateFactory.pure(['0','1'],[0,1]); self.assertFalse(audit_transition(self.q0(),q1,QuantumPreservation(min_fidelity=.9))['pass'])
    def test_28_quantum_portal(self):
        R=LinearOwnershipRegistry(); q=self.q0(); own=R.claim(q,'SRC'); env=QuantumEffectEnvelope(q.state_id,'IDENTITY','id',own.token,{'sector':'QFT','domain_id':'A'},{'sector':'QFT','domain_id':'B'},QuantumPreservation(min_fidelity=1)); t,o,rec=QuantumPortalEngine(R).transport(q,env,identity_channel()); self.assertEqual(rec['status'],'CLOSED')
    def test_29_quantum_portal_gr_reject(self):
        R=LinearOwnershipRegistry(); q=self.q0(); own=R.claim(q,'SRC'); env=QuantumEffectEnvelope(q.state_id,'IDENTITY','id',own.token,{'sector':'QFT','domain_id':'A'},{'sector':'GR','domain_id':'B'})
        with self.assertRaises(QuantumSectorViolation): QuantumPortalEngine(R).transport(q,env,identity_channel())
    def test_30_quantum_portal_coherence_fail(self):
        R=LinearOwnershipRegistry(); q=self.qp(); own=R.claim(q,'SRC'); env=QuantumEffectEnvelope(q.state_id,'DEPHASING','d',own.token,{'sector':'QFT','domain_id':'A'},{'sector':'QFT','domain_id':'B'},QuantumPreservation(preserve_coherence=True,min_coherence=diagnostics(q)['coherence_l1']))
        with self.assertRaises(QuantumClosureError): QuantumPortalEngine(R).transport(q,env,dephasing_channel(.5))
    def test_31_bridge_policy_structural(self): self.assertFalse(QuantumBridgePolicy().require_structural_only(self.q0(),{})['quantum_state_preserved'])
    def test_32_bridge_quantum_reject(self):
        with self.assertRaises(BridgeQuantumBoundaryError): QuantumBridgePolicy().assert_preserve_quantum(self.q0(),{})
    def test_33_capsule(self):
        inst={'canonical_mmo_id':'M','instance_id':'I','representation_id':'R'}; br={'source_content_root':'C','source_residue_root':'RR','bridge_id':'B','fabric_witness_id':'F'}; c=QuantumBridgePolicy().capsule(inst,br); self.assertEqual(c.content_root,'C')
    def test_34_brane(self):
        inst={'canonical_mmo_id':'M','brane_m5':{}}; q=self.q0(); b=QuantumEffectBraneAdapter().adapt(inst,q,[{'measurement_id':'m'}]); self.assertEqual(b['Chi']['quantum_sector'],'QFT')
    def test_35_channel_id_stable(self): self.assertEqual(hadamard_channel().channel_id,hadamard_channel().channel_id)
    def test_36_bell_norm(self): self.assertAlmostEqual(diagnostics(bell_pair('A','B'))['norm'],1)
    def test_37_dephase_purity(self): self.assertLessEqual(diagnostics(dephasing_channel(.5).apply(self.qp()))['purity'],1+1e-9)
    def test_38_measure_probability(self):
        R=LinearOwnershipRegistry(); q=self.q0(); own=R.claim(q,'A'); _,_,rec=MeasurementEngine(R).measure_basis(q,own.token,random.Random(2)); self.assertAlmostEqual(rec['probability'],1)
    def test_39_structural_transduce_any(self): self.assertTrue(EffectChecker().check(Effect.STRUCTURAL_TRANSDUCE,'PURE','GR')['admitted'])
    def test_40_joint_kind(self): self.assertEqual(bell_pair('A','B').kind,'JOINT')

if __name__=='__main__': unittest.main()
