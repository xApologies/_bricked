# Design invariants

1. Functions may not weaken the lower machine's type, effect, closure, chirality, sector, provenance, or quantum-linear rules.
2. Generic specialization is deterministic for the same function definition and concrete type arguments.
3. Every expanded local receives a collision-resistant call-site namespace.
4. Cross-module callable use requires an explicitly public function and an explicit `usefn` binding.
5. Package direct-dependency rules apply equally to value imports and callable imports.
6. Recursive call graphs are rejected in callable ABI v0.1.
7. Actual expanded effects must be a subset of the function's declared effect set.
8. The return value must satisfy the specialized return type after the Section 09 refined type check.
9. QSTATE resources retain Section 07 linear ownership semantics after expansion.
10. Portal and Road closure remains mandatory at module/program boundaries.
11. QFT/GR sector crossing still requires an explicit Bridge witness.
12. Python implements the reference compiler; Python does not define Genesis semantics.
13. Runtime generics are not silently introduced. No generic dictionaries or hidden dynamic dispatch exist in v0.1.
14. Source Genesis linguistic material remains source lineage, not an assertion that the reconstructed language historically contained compiler functions/generics.
