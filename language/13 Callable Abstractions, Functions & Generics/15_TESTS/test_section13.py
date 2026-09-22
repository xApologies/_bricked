import json, tempfile, unittest
from pathlib import Path

from genesis_callables import parse_extended_source, compile_sources, run_callable_build, CallableError
from genesis_callables.expander import Expander
from genesis_packages.registry import LocalRegistry
from genesis_callable_packages import CallablePackageRuntime

SEC=Path(__file__).resolve().parents[1]
REG=SEC/'17_STANDARD_LIBRARY/REGISTRY'
PROJECTS=SEC/'16_EXAMPLES/PROJECTS'


def src(body, module='app.t', version='0.2.0'):
    return f'genesis {version}\nmodule {module} {{\n{body}\n}}\n'

def fixture_prefix():
    return '''  en fab : FABRIC = mount "fabric://reference"\n  en reg : REGION = alloc fab cells 32\n  en g : GEOMETRIC = instantiate fab reg mmo @fixture\n'''

class Section13Tests(unittest.TestCase):
    def test_01_parse_legacy_version(self): self.assertEqual(parse_extended_source(src('',version='0.1.0')).version,'0.1.0')
    def test_02_parse_extended_version(self): self.assertEqual(parse_extended_source(src('')).version,'0.2.0')
    def test_03_parse_generic_function(self):
        m=parse_extended_source(src('''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {\n    en y : T = fork x\n    return y\n  }'''))
        self.assertEqual(m.functions[0].generics[0].name,'T')
    def test_04_parse_public_function(self):
        m=parse_extended_source(src('''  pub fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {\n    en y : T = fork x\n    return y\n  }'''))
        self.assertTrue(m.functions[0].public)
    def test_05_parse_usefn(self):
        m=parse_extended_source(src('  usefn lib.m::f as local'))
        self.assertEqual(m.function_imports[0].local,'local')
    def test_06_duplicate_generic_rejected(self):
        with self.assertRaises(Exception): parse_extended_source(src('''  fn f<T:ANY,T:ANY> (x:T) -> T effects [] {\n    return x\n  }'''))
    def test_07_duplicate_param_rejected(self):
        with self.assertRaises(Exception): parse_extended_source(src('''  fn f<T:ANY> (x:T,x:T) -> T effects [] {\n    return x\n  }'''))
    def test_08_missing_return_rejected(self):
        with self.assertRaises(Exception): parse_extended_source(src('''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {\n    en y : T = fork x\n  }'''))
    def test_09_multiple_return_rejected(self):
        with self.assertRaises(Exception): parse_extended_source(src('''  fn f<T:ANY> (x:T) -> T effects [] {\n    return x\n    return x\n  }'''))
    def test_10_nested_fn_rejected(self):
        with self.assertRaises(Exception): parse_extended_source(src('''  fn f<T:ANY> (x:T) -> T effects [] {\n    fn g<U:ANY> (y:U) -> U effects [] {\n    return y\n  }\n    return x\n  }'''))
    def test_11_private_cross_module_rejected(self):
        a=src('''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {\n    en y : T = fork x\n    return y\n  }''','lib.a')
        b=src('  usefn lib.a::f as f','app.b')
        with self.assertRaises(Exception): compile_sources([('a.gen',a),('b.gen',b)])
    def test_12_public_cross_module_accepted(self):
        a=src('''  pub fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {\n    en y : T = fork x\n    return y\n  }''','lib.a')
        b=src(f'''  usefn lib.a::f as f\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC<CLOSED,UNBOUND>''','app.b')
        r=compile_sources([('a.gen',a),('b.gen',b)]); self.assertEqual(len(r.expansion_records),1)
    def test_13_generic_arity_rejected(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {{\n    en y : T = fork x\n    return y\n  }}\n{fixture_prefix()}  call f<> (g) as y\n  export y : GEOMETRIC''')
        with self.assertRaises(Exception): compile_sources([('t.gen',s)])
    def test_14_generic_bound_rejected(self):
        s=src(f'''  fn f<T:QSTATE> (x:T) -> T effects [QUANTUM_LINEAR] {{\n    q superpose x as y\n    return y\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : QSTATE''')
        with self.assertRaises(Exception): compile_sources([('t.gen',s)])
    def test_15_value_arity_rejected(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T,z:T) -> T effects [TRANSFORM,INHERIT] {{\n    en y : T = fork x\n    return y\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC''')
        with self.assertRaises(Exception): compile_sources([('t.gen',s)])
    def test_16_return_must_be_local_v01(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [] {{\n    return x\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC''')
        with self.assertRaises(Exception): compile_sources([('t.gen',s)])
    def test_17_effect_containment_rejected(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [] {{\n    en y : T = fork x\n    return y\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC''')
        with self.assertRaises(Exception): compile_sources([('t.gen',s)])
    def test_18_direct_recursion_rejected(self):
        s=src('''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {\n    call f<T> (x) as y\n    return y\n  }''')
        with self.assertRaises(Exception): compile_sources([('t.gen',s)])
    def test_19_indirect_recursion_rejected(self):
        s=src('''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {\n    call g<T> (x) as y\n    return y\n  }\n  fn g<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {\n    call f<T> (x) as y\n    return y\n  }''')
        with self.assertRaises(Exception): compile_sources([('t.gen',s)])
    def test_20_simple_monomorphization(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {{\n    en y : T = fork x\n    return y\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC<CLOSED,UNBOUND>''')
        r=compile_sources([('t.gen',s)]); self.assertIn('en y : GEOMETRIC<CLOSED,UNBOUND> = fork g',r.expanded_sources[0][1])
    def test_21_deterministic_specialization(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {{\n    en y : T = fork x\n    return y\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC<CLOSED,UNBOUND>''')
        a=compile_sources([('t.gen',s)]); b=compile_sources([('t.gen',s)])
        self.assertEqual(a.callable_receipt['specializations'],b.callable_receipt['specializations'])
    def test_22_deterministic_bytecode(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {{\n    en y : T = fork x\n    return y\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC<CLOSED,UNBOUND>''')
        a=compile_sources([('t.gen',s)]); b=compile_sources([('t.gen',s)])
        self.assertEqual(a.frontend.link.bytecode,b.frontend.link.bytecode)
    def test_23_function_boundary_erased_before_gir(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {{\n    en y : T = fork x\n    return y\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC<CLOSED,UNBOUND>''')
        r=compile_sources([('t.gen',s)]); self.assertNotIn('CALL', [n['op'] for n in r.frontend.link.gir['nodes']])
    def test_24_callable_receipt_has_call_count(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {{\n    en y : T = fork x\n    return y\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC<CLOSED,UNBOUND>''')
        self.assertEqual(compile_sources([('t.gen',s)]).callable_receipt['call_count'],1)
    def test_25_return_type_proof(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {{\n    en y : T = fork x\n    return y\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC<CLOSED,UNBOUND>''')
        r=compile_sources([('t.gen',s)]); self.assertTrue(all(p['status']=='PASS' for p in r.callable_proofs))
    def test_26_runtime_halts(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {{\n    en y : T = fork x\n    return y\n  }}\n{fixture_prefix()}  call f<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC<CLOSED,UNBOUND>''')
        self.assertTrue(run_callable_build(compile_sources([('t.gen',s)])).halted)
    def test_27_linear_qstate_valid(self):
        s=src(f'''  fn f<T:QSTATE> (x:T) -> QRESULT<CLASSICAL> effects [QUANTUM_LINEAR,MEASURE] {{\n    q superpose x as q1\n    q measure q1 as r\n    return r\n  }}\n{fixture_prefix()}  q prepare g as q0\n  call f<QSTATE<OWNED>> (q0) as r\n  export r : QRESULT<CLASSICAL>''')
        self.assertTrue(compile_sources([('t.gen',s)]).frontend.link.check.ok)
    def test_28_linear_qstate_alias_rejected(self):
        s=src(f'''  fn f<T:QSTATE> (x:T) -> QSTATE<OWNED> effects [QUANTUM_LINEAR] {{\n    q entangle x x as q1\n    return q1\n  }}\n{fixture_prefix()}  q prepare g as q0\n  call f<QSTATE<OWNED>> (q0) as r\n  export r : QSTATE<OWNED>''')
        with self.assertRaises(Exception): compile_sources([('t.gen',s)])
    def test_29_nested_call_expands(self):
        s=src(f'''  fn f<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {{\n    en y : T = fork x\n    return y\n  }}\n  fn g<T:GEOMETRIC> (x:T) -> T effects [TRANSFORM,INHERIT] {{\n    call f<T> (x) as y\n    return y\n  }}\n{fixture_prefix()}  call g<GEOMETRIC<CLOSED,UNBOUND>> (g) as y\n  export y : GEOMETRIC<CLOSED,UNBOUND>''')
        r=compile_sources([('t.gen',s)]); self.assertEqual(len(r.expansion_records),2)
    def test_30_alpha_renames_nested_locals(self):
        reg=LocalRegistry(REG); rt=CallablePackageRuntime(reg); r=rt.build(PROJECTS/'NESTED_CALLABLE')
        text=[t for f,t in r.callable.expanded_sources if 'NESTED_CALLABLE' in f][0]
        self.assertIn('__c',text)
    def test_31_mixed_sector_callable_executes(self):
        reg=LocalRegistry(REG); r=CallablePackageRuntime(reg).build(PROJECTS/'MIXED_SECTOR'); self.assertTrue(r.execution.halted)
    def test_32_quantum_callable_executes(self):
        reg=LocalRegistry(REG); r=CallablePackageRuntime(reg).build(PROJECTS/'QUANTUM_GENERIC'); self.assertTrue(r.execution.halted)
    def test_33_portal_callable_executes(self):
        reg=LocalRegistry(REG); r=CallablePackageRuntime(reg).build(PROJECTS/'PORTAL_GENERIC'); self.assertTrue(r.execution.halted)
    def test_34_brane_callable_executes(self):
        reg=LocalRegistry(REG); r=CallablePackageRuntime(reg).build(PROJECTS/'BRANE_PROVENANCE'); self.assertTrue(r.execution.halted)
    def test_35_package_build_has_callable_receipt(self):
        reg=LocalRegistry(REG); r=CallablePackageRuntime(reg).build(PROJECTS/'GENERIC_FORK'); self.assertIn('callable_frontend_id',r.receipt)
    def test_36_package_lock_reproducible(self):
        reg=LocalRegistry(REG); rt=CallablePackageRuntime(reg); a=rt.build(PROJECTS/'GENERIC_FORK'); b=rt.build(PROJECTS/'GENERIC_FORK',frozen_lock=a.lockfile); self.assertEqual(a.lockfile.resolution_root,b.lockfile.resolution_root)
    def test_37_optimizer_equivalence(self):
        reg=LocalRegistry(REG); r=CallablePackageRuntime(reg).build(PROJECTS/'PORTAL_GENERIC'); self.assertEqual(r.toolchain['equivalence']['status'],'PASS')
    def test_38_explicit_generic_type_preserved(self):
        reg=LocalRegistry(REG); r=CallablePackageRuntime(reg).build(PROJECTS/'GENERIC_FORK'); self.assertTrue(any(x.type_args==['GEOMETRIC<CLOSED,UNBOUND>'] for x in r.callable.expansion_records))
    def test_39_no_recursion_in_stdlib(self):
        mods=[]
        for p in sorted(REG.glob('*/0.2.0/src/*.gen')): mods.append(parse_extended_source(p.read_text(),str(p)))
        Expander(mods); self.assertTrue(True)
    def test_40_registry_has_callable_core(self): self.assertIsNotNone(LocalRegistry(REG).get('genesis.std.core','0.2.0'))
    def test_41_registry_has_callable_portal(self): self.assertIsNotNone(LocalRegistry(REG).get('genesis.std.portal','0.2.0'))
    def test_42_registry_has_callable_quantum(self): self.assertIsNotNone(LocalRegistry(REG).get('genesis.std.quantum','0.2.0'))
    def test_43_registry_has_callable_bridge(self): self.assertIsNotNone(LocalRegistry(REG).get('genesis.std.bridge','0.2.0'))
    def test_44_registry_has_callable_brane(self): self.assertIsNotNone(LocalRegistry(REG).get('genesis.std.brane','0.2.0'))
    def test_45_registry_has_callable_provenance(self): self.assertIsNotNone(LocalRegistry(REG).get('genesis.std.provenance','0.2.0'))
    def test_46_registry_has_callable_road(self): self.assertIsNotNone(LocalRegistry(REG).get('genesis.std.road','0.2.0'))
    def test_47_registry_has_atomic_02(self): self.assertIsNotNone(LocalRegistry(REG).get('genesis.std.atomic','0.2.0'))
    def test_48_registry_has_fabric_02(self): self.assertIsNotNone(LocalRegistry(REG).get('genesis.std.fabric','0.2.0'))

if __name__=='__main__': unittest.main(verbosity=2)
