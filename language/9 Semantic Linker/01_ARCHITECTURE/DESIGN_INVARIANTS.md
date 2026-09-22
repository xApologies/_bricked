# Design invariants

1. GIR remains the semantic execution graph; Section 09 does not replace it with source-language syntax.
2. A module import must resolve to exactly one declared export.
3. Import/export type compatibility is checked before graph merge.
4. Node IDs and SSA values are alpha-renamed by module, preventing accidental capture.
5. Link order is determined from the module dependency DAG, not input-file order.
6. Module dependency cycles are rejected in v0.1 rather than silently introducing initialization semantics.
7. Refined types may add sector/typestate information without changing the Section 08 coarse VM type tag.
8. A QSTATE is linear: a consuming quantum effect moves/consumes the previous state handle.
9. Portals and Roads cannot escape the linked program in OPEN typestate.
10. Cross-sector use requires an explicit Bridge authorization; QFT and GR are not aliases.
11. Effect budgets are allow-lists. A module cannot acquire undeclared authority by linking against another module.
12. A target backend must advertise every required opcode/effect/sector feature.
13. Proof obligations are auditable static witnesses, not claims of mathematical theorem proving beyond the encoded checks.
14. Link receipts and output GIR are content-addressed and deterministic for identical normalized inputs.
15. Python is the bootstrap implementation, not the semantic authority.
