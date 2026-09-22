import json, unittest, tempfile, copy
from pathlib import Path
from genesis_conformance import *
from genesis_conformance.harness import V1ConformanceHarness
from genesis_bootstrap import BootstrapHarness

SEC=Path(__file__).resolve().parents[1]
REL=SEC/'01_RELEASE_FREEZE/GENESIS_V1_0_RELEASE_DESCRIPTOR.json'
LOCK=SEC/'01_RELEASE_FREEZE/SECTION_01_19_CORE_LOCK.json'
ABI=SEC/'02_ABI_FREEZE/GENESIS_V1_0_ABI_FREEZE.json'
FMT=SEC/'03_FORMAT_FREEZE/GENESIS_V1_0_FORMAT_FREEZE.json'
CTRL=SEC/'15_EXAMPLES/bootstrap_controller.gen'
FRONT=SEC/'15_EXAMPLES/self_host_frontier.json'

class Section20Tests(unittest.TestCase):
    def test_01_release_verifies(self): self.assertEqual(verify_release(load_json(REL))['status'],'PASS')
    def test_02_release_version(self): self.assertEqual(load_json(REL)['version'],'1.0.0')
    def test_03_release_frozen(self): self.assertEqual(load_json(REL)['release_status'],'FROZEN')
    def test_04_not_full_self_host(self): self.assertFalse(load_json(REL)['full_self_host'])
    def test_05_blackglass_not_false_migrated(self): self.assertEqual(load_json(REL)['blackglass_v3_status'],'READY_FOR_INTEGRATION_NOT_YET_MIGRATED')
    def test_06_source_boundary(self): self.assertEqual(load_json(REL)['source_genesis_boundary'],'PRESERVED_DISTINCT_FROM_COMPUTATIONAL_GENESIS')
    def test_07_s0_unresolved(self): self.assertIn('S0_STRUCTURAL_ZERO_VS_EXISTENCE_CONFLICT',load_json(REL)['known_unresolved_semantic_gates'])
    def test_08_core_lock_verifies(self): self.assertEqual(verify_core_lock(load_json(LOCK))['sections'],19)
    def test_09_sections_exact(self): self.assertEqual([x['section'] for x in load_json(LOCK)['sections']],list(range(1,20)))
    def test_10_abi_verifies(self): self.assertEqual(verify_abi(load_json(ABI))['status'],'PASS')
    def test_11_abi_count(self): self.assertEqual(len(load_json(ABI)['contracts']),19)
    def test_12_format_verifies(self): self.assertEqual(verify_format(load_json(FMT))['status'],'PASS')
    def test_13_bootstrap_fixed_point(self): self.assertTrue(BootstrapHarness(CTRL,FRONT).run().fixed_point)
    def test_14_bootstrap_not_full_self_host(self): self.assertFalse(BootstrapHarness(CTRL,FRONT).run().self_hosted)
    def test_15_conformance_harness_pass(self): self.assertEqual(V1ConformanceHarness(SEC).run()['status'],'PASS')
    def test_16_conformance_bootstrap_status(self): self.assertEqual(V1ConformanceHarness(SEC).run()['bootstrap_status'],'BOOTSTRAP_FIXED_POINT')
    def test_17_release_root_tamper(self):
        d=load_json(REL); d['blackglass_v3_status']='MIGRATED'
        with self.assertRaises(ConformanceError): verify_release(d)
    def test_18_false_self_host_rejected(self):
        d=load_json(REL); d['full_self_host']=True; x=dict(d); x.pop('release_root'); d['release_root']=digest_obj(x)
        with self.assertRaisesRegex(ConformanceError,'V1_FALSE_FULL_SELF_HOST_CLAIM'): verify_release(d)
    def test_19_s0_silent_reconcile_rejected(self):
        d=load_json(REL); d['known_unresolved_semantic_gates']=[]; x=dict(d); x.pop('release_root'); d['release_root']=digest_obj(x)
        with self.assertRaisesRegex(ConformanceError,'V1_SEMANTIC_GATE_SILENTLY_RECONCILED'): verify_release(d)
    def test_20_source_boundary_erasure_rejected(self):
        d=load_json(REL); d['source_genesis_boundary']='MERGED'; x=dict(d); x.pop('release_root'); d['release_root']=digest_obj(x)
        with self.assertRaisesRegex(ConformanceError,'V1_SOURCE_COMPUTATIONAL_BOUNDARY_ERASED'): verify_release(d)
    def test_21_core_lock_tamper(self):
        d=load_json(LOCK); d['sections'][0]['core_sha256']='0'*64
        with self.assertRaisesRegex(ConformanceError,'V1_CORE_LOCK_MISMATCH'): verify_core_lock(d)
    def test_22_missing_section_rejected(self):
        d=load_json(LOCK); d['sections']=d['sections'][:-1]; x=dict(d); x.pop('core_lock_root'); d['core_lock_root']=digest_obj(x)
        with self.assertRaisesRegex(ConformanceError,'V1_SECTION_MISSING'): verify_core_lock(d)
    def test_23_bad_crc_rejected(self):
        d=load_json(LOCK); d['sections'][0]['core_crc']='FAIL'; x=dict(d); x.pop('core_lock_root'); d['core_lock_root']=digest_obj(x)
        with self.assertRaisesRegex(ConformanceError,'V1_CORE_PACKAGE_TAMPER'): verify_core_lock(d)
    def test_24_abi_tamper(self):
        d=load_json(ABI); d['contracts'][0]['freeze']='OPEN'
        with self.assertRaisesRegex(ConformanceError,'V1_ABI_FREEZE_INVALID'): verify_abi(d)
    def test_25_format_tamper(self):
        d=load_json(FMT); d['status']='OPEN'
        with self.assertRaisesRegex(ConformanceError,'V1_FORMAT_FREEZE_INVALID'): verify_format(d)

    def test_26_section_01_digest(self):
        e=load_json(LOCK)['sections'][0]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_27_section_02_digest(self):
        e=load_json(LOCK)['sections'][1]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_28_section_03_digest(self):
        e=load_json(LOCK)['sections'][2]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_29_section_04_digest(self):
        e=load_json(LOCK)['sections'][3]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_30_section_05_digest(self):
        e=load_json(LOCK)['sections'][4]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_31_section_06_digest(self):
        e=load_json(LOCK)['sections'][5]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_32_section_07_digest(self):
        e=load_json(LOCK)['sections'][6]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_33_section_08_digest(self):
        e=load_json(LOCK)['sections'][7]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_34_section_09_digest(self):
        e=load_json(LOCK)['sections'][8]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_35_section_10_digest(self):
        e=load_json(LOCK)['sections'][9]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_36_section_11_digest(self):
        e=load_json(LOCK)['sections'][10]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_37_section_12_digest(self):
        e=load_json(LOCK)['sections'][11]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_38_section_13_digest(self):
        e=load_json(LOCK)['sections'][12]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_39_section_14_digest(self):
        e=load_json(LOCK)['sections'][13]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_40_section_15_digest(self):
        e=load_json(LOCK)['sections'][14]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_41_section_16_digest(self):
        e=load_json(LOCK)['sections'][15]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_42_section_17_digest(self):
        e=load_json(LOCK)['sections'][16]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_43_section_18_digest(self):
        e=load_json(LOCK)['sections'][17]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_44_section_19_digest(self):
        e=load_json(LOCK)['sections'][18]; self.assertEqual(len(e['core_sha256']),64); int(e['core_sha256'],16)
    def test_45_section_01_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][0]['core_crc'],'PASS')
    def test_46_section_02_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][1]['core_crc'],'PASS')
    def test_47_section_03_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][2]['core_crc'],'PASS')
    def test_48_section_04_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][3]['core_crc'],'PASS')
    def test_49_section_05_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][4]['core_crc'],'PASS')
    def test_50_section_06_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][5]['core_crc'],'PASS')
    def test_51_section_07_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][6]['core_crc'],'PASS')
    def test_52_section_08_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][7]['core_crc'],'PASS')
    def test_53_section_09_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][8]['core_crc'],'PASS')
    def test_54_section_10_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][9]['core_crc'],'PASS')
    def test_55_section_11_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][10]['core_crc'],'PASS')
    def test_56_section_12_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][11]['core_crc'],'PASS')
    def test_57_section_13_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][12]['core_crc'],'PASS')
    def test_58_section_14_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][13]['core_crc'],'PASS')
    def test_59_section_15_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][14]['core_crc'],'PASS')
    def test_60_section_16_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][15]['core_crc'],'PASS')
    def test_61_section_17_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][16]['core_crc'],'PASS')
    def test_62_section_18_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][17]['core_crc'],'PASS')
    def test_63_section_19_crc_lock(self):
        self.assertEqual(load_json(LOCK)['sections'][18]['core_crc'],'PASS')

if __name__=='__main__': unittest.main(verbosity=2)
