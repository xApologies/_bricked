import unittest
from pathlib import Path
from genesis_control import *
from genesis_control.model import Instruction,Program,Opcode,TypeTag

SEC=Path(__file__).resolve().parents[1]
EX=SEC/'16_EXAMPLES'

def c(src): return compile_source(src,'test.gen')[1]
def run(src): return VM().run(c(src))
def mod(body,decls=''):
    return 'genesis 0.3.0\nmodule t {\n'+decls+body+'\n}\n'

class Section14Tests(unittest.TestCase):
    def test_01_parse_version(self): self.assertEqual(parse_source(mod('  let x : INT = 1')).version,'0.3.0')
    def test_02_int_literal(self): self.assertEqual(next(iter(run(mod('  let x : INT = 7\n  export x : INT')).exports.values())).value,7)
    def test_03_bool_literal(self): self.assertTrue(next(iter(run(mod('  let x : BOOL = true\n  export x : BOOL')).exports.values())).value)
    def test_04_float_literal(self): self.assertEqual(next(iter(run(mod('  let x : FLOAT = 1.5\n  export x : FLOAT')).exports.values())).value,1.5)
    def test_05_text_literal(self): self.assertEqual(next(iter(run(mod('  let x : TEXT = "hi"\n  export x : TEXT')).exports.values())).value,'hi')
    def test_06_add(self): self.assertEqual(next(iter(run(mod('  let a : INT = 2\n  let b : INT = 3\n  let x : INT = add a b\n  export x : INT')).exports.values())).value,5)
    def test_07_sub(self): self.assertEqual(next(iter(run(mod('  let a : INT = 7\n  let b : INT = 3\n  let x : INT = sub a b\n  export x : INT')).exports.values())).value,4)
    def test_08_lt(self): self.assertTrue(next(iter(run(mod('  let a : INT = 2\n  let b : INT = 3\n  let x : BOOL = lt a b\n  export x : BOOL')).exports.values())).value)
    def test_09_le(self): self.assertTrue(next(iter(run(mod('  let a : INT = 3\n  let b : INT = 3\n  let x : BOOL = le a b\n  export x : BOOL')).exports.values())).value)
    def test_10_eq(self): self.assertTrue(next(iter(run(mod('  let a : INT = 3\n  let b : INT = 3\n  let x : BOOL = eq a b\n  export x : BOOL')).exports.values())).value)
    def test_11_not(self): self.assertFalse(next(iter(run(mod('  let a : BOOL = true\n  let x : BOOL = not a\n  export x : BOOL')).exports.values())).value)
    def test_12_and(self): self.assertFalse(next(iter(run(mod('  let a : BOOL = true\n  let b : BOOL = false\n  let x : BOOL = and a b\n  export x : BOOL')).exports.values())).value)
    def test_13_or(self): self.assertTrue(next(iter(run(mod('  let a : BOOL = true\n  let b : BOOL = false\n  let x : BOOL = or a b\n  export x : BOOL')).exports.values())).value)
    def test_14_record_construct(self):
        s=mod('  let a : INT = 1\n  let b : INT = 2\n  let p : Pair = record Pair { left=a, right=b }\n  export p : Pair','  record Pair { left: INT, right: INT }\n')
        self.assertEqual(next(iter(run(s).exports.values())).value['fields']['right'],2)
    def test_15_record_field(self):
        s=mod('  let a : INT = 1\n  let b : INT = 2\n  let p : Pair = record Pair { left=a, right=b }\n  let x : INT = field p left\n  export x : INT','  record Pair { left: INT, right: INT }\n')
        self.assertEqual(next(iter(run(s).exports.values())).value,1)
    def test_16_record_missing_field_rejected(self):
        with self.assertRaises(Exception): c(mod('  let a : INT = 1\n  let p : Pair = record Pair { left=a }','  record Pair { left: INT, right: INT }\n'))
    def test_17_record_wrong_field_type_rejected(self):
        with self.assertRaises(Exception): c(mod('  let a : TEXT = "x"\n  let b : INT = 2\n  let p : Pair = record Pair { left=a, right=b }','  record Pair { left: INT, right: INT }\n'))
    def test_18_variant_construct(self):
        s=mod('  let a : INT = 4\n  let c : Choice = variant Choice::Left a\n  export c : Choice','  enum Choice { Left(INT), Empty }\n')
        self.assertEqual(next(iter(run(s).exports.values())).value['tag'],'Left')
    def test_19_variant_bad_tag(self):
        with self.assertRaises(Exception): c(mod('  let a : INT = 4\n  let c : Choice = variant Choice::Nope a','  enum Choice { Left(INT), Empty }\n'))
    def test_20_option_some(self):
        self.assertEqual(next(iter(run(mod('  let a : INT = 4\n  let o : OPTION<INT> = some a\n  export o : OPTION<INT>')).exports.values())).value['tag'],'Some')
    def test_21_option_none(self):
        self.assertEqual(next(iter(run(mod('  let o : OPTION<INT> = none\n  export o : OPTION<INT>')).exports.values())).value['tag'],'None')
    def test_22_result_ok(self):
        self.assertEqual(next(iter(run(mod('  let a : INT = 4\n  let o : RESULT<INT,TEXT> = ok a\n  export o : RESULT<INT,TEXT>')).exports.values())).value['tag'],'Ok')
    def test_23_result_err(self):
        self.assertEqual(next(iter(run(mod('  let a : TEXT = "e"\n  let o : RESULT<INT,TEXT> = err a\n  export o : RESULT<INT,TEXT>')).exports.values())).value['tag'],'Err')
    def test_24_if_true_executes(self):
        s=mod('  let c : BOOL = true\n  if c {\n    emit receipt as a\n  } else {\n    emit receipt as b\n  }\n  let x : INT = 1\n  export x : INT')
        self.assertTrue(run(s).halted)
    def test_25_if_false_executes(self):
        s=mod('  let c : BOOL = false\n  if c {\n    emit receipt as a\n  } else {\n    emit receipt as b\n  }\n  let x : INT = 1\n  export x : INT')
        self.assertTrue(run(s).halted)
    def test_26_if_requires_bool(self):
        with self.assertRaises(Exception): c(mod('  let c : INT = 1\n  if c {\n  } else {\n  }'))
    def test_27_branch_local_escape_rejected(self):
        with self.assertRaises(Exception): c(mod('  let c : BOOL = true\n  if c {\n    let x : INT = 1\n  } else {\n  }\n  export x : INT'))
    def test_28_repeat_zero(self): self.assertTrue(run(mod('  repeat 0 {\n    emit receipt as x\n  }')).halted)
    def test_29_repeat_four(self): self.assertEqual(sum(i.op==Opcode.EMIT_RECEIPT for i in c(mod('  repeat 4 {\n    emit receipt as x\n  }')).instructions),4)
    def test_30_repeat_bound(self):
        with self.assertRaises(Exception): c(mod('  repeat 4097 {\n  }'))
    def test_31_match_exhaustive(self):
        s=mod('  let a : INT = 1\n  let c : C = variant C::A a\n  match c {\n    A(v) => {\n      let x : INT = move v\n    }\n    B => {\n      let y : INT = 0\n    }\n  }','  enum C { A(INT), B }\n')
        self.assertTrue(run(s).halted)
    def test_32_match_nonexhaustive(self):
        with self.assertRaises(Exception): c(mod('  let a : INT = 1\n  let c : C = variant C::A a\n  match c {\n    A(v) => {\n      let x : INT = move v\n    }\n  }','  enum C { A(INT), B }\n'))
    def test_33_match_default(self):
        s=mod('  let a : INT = 1\n  let c : C = variant C::A a\n  match c {\n    A(v) => {\n      let x : INT = move v\n    }\n    _ => {\n      let y : INT = 0\n    }\n  }','  enum C { A(INT), B }\n')
        self.assertTrue(run(s).halted)
    def test_34_match_duplicate_rejected(self):
        with self.assertRaises(Exception): c(mod('  let a : INT = 1\n  let c : C = variant C::A a\n  match c {\n    A(v) => {\n      let x : INT = move v\n    }\n    A(z) => {\n      let y : INT = move z\n    }\n  }','  enum C { A(INT), B }\n'))
    def test_35_portal_closed_both_branches(self): self.assertTrue(run((EX/'02_IF_PORTAL.gen').read_text()).halted)
    def test_36_portal_open_one_path_rejected(self):
        body='  let cond : BOOL = true\n  en fab : FABRIC = mount "fabric://reference"\n  en reg : REGION = alloc fab cells 32\n  en g : GEOMETRIC = instantiate fab reg mmo @fixture\n  rel g -> "environment" as rr\n  admit rr as aa\n  portal GR g with aa as p corridor "x"\n  if cond {\n    tor p with g as c\n  } else {\n    emit receipt as z\n  }'
        with self.assertRaises(Exception): c(mod(body))
    def test_37_qstate_consumed_exclusive_branches(self): self.assertTrue(run((EX/'06_QUANTUM_BRANCH.gen').read_text()).halted)
    def test_38_qstate_double_consume_same_path_rejected(self):
        body='  en fab : FABRIC = mount "fabric://reference"\n  en reg : REGION = alloc fab cells 32\n  en g : GEOMETRIC = instantiate fab reg mmo @fixture\n  q prepare g as q0\n  q measure q0 as m1\n  q measure q0 as m2'
        with self.assertRaises(Exception): c(mod(body))
    def test_39_qstate_alias_entangle_rejected(self):
        body='  en fab : FABRIC = mount "fabric://reference"\n  en reg : REGION = alloc fab cells 32\n  en g : GEOMETRIC = instantiate fab reg mmo @fixture\n  q prepare g as q0\n  q entangle q0 q0 as q1'
        with self.assertRaises(Exception): c(mod(body))
    def test_40_cfg_receipt(self): self.assertEqual(c(mod('  let x : INT = 1')).metadata['verification']['verifier'],'CFG_PATH_V0_1')
    def test_41_deterministic_bytecode(self):
        s=(EX/'03_MATCH.gen').read_text(); self.assertEqual(encode(c(s)),encode(c(s)))
    def test_42_roundtrip_bytecode(self):
        p=c((EX/'01_RECORDS.gen').read_text()); q=decode(encode(p)); self.assertEqual(disassemble(p),disassemble(q))
    def test_43_digest_tamper_rejected(self):
        b=bytearray(encode(c(mod('  let x : INT = 1')))); b[-1]^=1
        with self.assertRaises(Exception): decode(bytes(b))
    def test_44_disasm_has_branch(self): self.assertIn('BRANCH',disassemble(c((EX/'02_IF_PORTAL.gen').read_text())))
    def test_45_disasm_has_data_record(self): self.assertIn('DATA_RECORD',disassemble(c((EX/'01_RECORDS.gen').read_text())))
    def test_46_domain_fabric_executes(self): self.assertTrue(run(mod('  en fab : FABRIC = mount "fabric://reference"\n  export fab : FABRIC')).halted)
    def test_47_domain_geometric_executes(self): self.assertTrue(run(mod('  en fab : FABRIC = mount "fabric://reference"\n  en reg : REGION = alloc fab cells 4\n  en g : GEOMETRIC = instantiate fab reg mmo @fixture\n  export g : GEOMETRIC')).halted)
    def test_48_nested_if(self):
        s=mod('  let a : BOOL = true\n  let b : BOOL = false\n  if a {\n    if b {\n      emit receipt as x\n    } else {\n      emit receipt as y\n    }\n  } else {\n    emit receipt as z\n  }')
        self.assertTrue(run(s).halted)
    def test_49_record_example(self): self.assertTrue(run((EX/'01_RECORDS.gen').read_text()).halted)
    def test_50_match_example(self): self.assertTrue(run((EX/'03_MATCH.gen').read_text()).halted)
    def test_51_option_result_example(self): self.assertTrue(run((EX/'04_OPTION_RESULT.gen').read_text()).halted)
    def test_52_repeat_example(self): self.assertTrue(run((EX/'05_REPEAT.gen').read_text()).halted)
    def test_53_all_examples_compile(self):
        for p in EX.glob('*.gen'): c(p.read_text())
    def test_54_all_examples_run(self):
        for p in EX.glob('*.gen'): self.assertTrue(run(p.read_text()).halted)
    def test_55_result_type_mismatch(self):
        with self.assertRaises(Exception): c(mod('  let x : BOOL = 1'))
    def test_56_unknown_identity(self):
        with self.assertRaises(Exception): c(mod('  let x : INT = add nope nope'))
    def test_57_enum_payload_required(self):
        with self.assertRaises(Exception): c(mod('  let c : C = variant C::A','  enum C { A(INT) }\n'))
    def test_58_payloadless_binder_rejected(self):
        with self.assertRaises(Exception): c(mod('  let c : C = variant C::A\n  match c {\n    A(v) => {\n      let x : INT = 1\n    }\n  }','  enum C { A }\n'))
    def test_59_export_type_checked(self):
        with self.assertRaises(Exception): c(mod('  let x : INT = 1\n  export x : TEXT'))
    def test_60_opcode_extension_stable(self): self.assertEqual(int(Opcode.DATA_RECORD),0x0080)
    def test_61_match_default_must_be_last(self):
        with self.assertRaises(Exception): c(mod('  let c : C = variant C::B\n  match c {\n    _ => {\n      let x : INT = 0\n    }\n    B => {\n      let y : INT = 1\n    }\n  }','  enum C { A, B }\n'))
    def test_62_exhaustive_match_has_exact_halting_paths(self):
        s=mod('  let c : C = variant C::B\n  match c {\n    A => {\n      let x : INT = 0\n    }\n    B => {\n      let y : INT = 1\n    }\n  }','  enum C { A, B }\n')
        self.assertEqual(c(s).metadata['verification']['halting_paths'],2)

if __name__=='__main__': unittest.main(verbosity=2)
