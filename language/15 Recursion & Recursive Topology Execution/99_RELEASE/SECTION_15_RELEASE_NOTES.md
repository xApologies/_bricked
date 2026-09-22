# Section 15 release notes

Section 15 establishes executable recursion and recursive topology semantics for Genesis.

Delivered:

- frame-local recursive register files
- direct recursive calls and returns
- deterministic recursive bytecode
- well-founded `decreases` contracts with affine compile-time decrease proof
- finite `fuel` recursion
- cycle-aware `visit_once` recursion
- runtime depth/fuel/history guards
- deterministic frame closure receipts and inherited history roots
- recursive topology traversal with cycle witnesses
- persistent recursion as validated suspend/resume continuations
- deny-by-default linear resource capture across recursion/yield boundaries
- six executable Genesis 0.4 reference programs

Validation:

- Section 15: 60/60 PASS
- Section 14 regression: 62/62 PASS
- Reference Genesis recursion programs: 6/6 compile and execute

Deliberately deferred instead of simulated:

- mutual recursion / SCC termination proofs
- tail-call optimization
- scheduler-level persistent recursion (Section 16)
- unrestricted linear-resource transfer across recursion frames
