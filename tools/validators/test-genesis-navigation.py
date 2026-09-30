"""Negative checks for the discovery contract; no source corpus mutation."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('validate_genesis', Path(__file__).with_name('validate-genesis.py'))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class ContractTests(unittest.TestCase):
    def setUp(self): self.registry = v.read('genesis/registries/DOMAIN_REGISTRY.json')
    def test_valid_registry(self): self.assertTrue(v.validate_registry(self.registry))
    def test_extra_domain(self):
        self.registry['domains']['guardian'] = copy.deepcopy(self.registry['domains']['state'])
        with self.assertRaises(ValueError): v.validate_registry(self.registry)
    def test_wrong_dimension(self):
        self.registry['domains']['nexus']['dimensions'] = [5]
        with self.assertRaises(ValueError): v.validate_registry(self.registry)
    def test_direct_jump(self):
        self.registry['adjacency'].append(['shell', 'state'])
        with self.assertRaises(ValueError): v.validate_registry(self.registry)
    def test_missing_manifest_authority(self):
        manifest = v.read('genesis/domains/state/MANIFEST.json'); del manifest['authority_refs']
        with self.assertRaises(ValueError): v.schema_check(manifest, v.read('genesis/schemas/domain-manifest.schema.json'))
    def test_unsupported_schema_keyword(self):
        with self.assertRaises(ValueError): v.schema_check({}, {'invented': True})
    def test_escaping_reference(self):
        with self.assertRaises(ValueError): v.reference('../outside')
    def test_unresolved_authority(self):
        with self.assertRaises(ValueError): v.reference('genesis/not-present')

if __name__ == '__main__': unittest.main()
