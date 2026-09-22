# Design invariants

1. Source text never becomes semantic authority over GIR/Section 09.
2. One source declaration produces at most one SSA value.
3. Source variable names lower deterministically to `%name` GIR values.
4. Every executable source statement receives a stable source-map entry.
5. v0.1 preserves textual effect order with explicit `effect_order` edges; later optimizers may relax only proven-commutative edges.
6. Effect budgets are compiler-derived from lowered operations, not trusted from source declarations.
7. Export types are explicit interface contracts and are checked by Section 09.
8. Imported symbols retain module provenance and refined type declarations.
9. Quantum QSTATE values remain linear after lowering; there is no frontend copy escape hatch.
10. QFT/GR changes require explicit `bridge` syntax and lower to `BRIDGE_SECTOR`.
11. `ve` lowers to Portal transport, not to entanglement or magical nonlocal transfer.
12. `tor` lowers to explicit closure and cannot be silently inserted to make an invalid program pass.
13. Source Genesis linguistic material is a mnemonic/design source, not retroactively rewritten as compiler history.
14. Canonical source formatting is deterministic.
15. Python is the bootstrap frontend implementation, not the definition of Genesis semantics.
