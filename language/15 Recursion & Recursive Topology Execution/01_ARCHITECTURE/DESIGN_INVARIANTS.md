# Design invariants

1. Recursion is a GVM/Genesis execution property, not Python call-stack semantics.
2. Each recursive invocation owns a fresh local register file.
3. A self-call must be admitted by a declared recursion contract.
4. `decreases` self-calls carry a statically verified negative affine delta relative to the declared metric.
5. `fuel` self-calls consume one unit of inherited fuel.
6. `visit_once` self-calls cannot repeat a key already present in the inherited visit history.
7. Every function return is preceded by recursive closure.
8. Closure receipts are deterministic and contribute to an inherited history root.
9. Open Portal/Road and live QSTATE resources cannot be implicitly captured across recursion or persistent-yield boundaries.
10. Persistent recursion yields a continuation; it is never mislabeled as a halted computation.
11. Mutual recursion is rejected in v0.1 until SCC-wide termination proofs are implemented.
12. Python is the reference backend only; it does not define recursion semantics.
