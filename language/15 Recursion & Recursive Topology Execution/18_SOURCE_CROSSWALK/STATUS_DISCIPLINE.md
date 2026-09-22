# Status discipline

Canonical for Section 15 v0.1 implementation:
- recursive frame-local register semantics
- `decreases`, `fuel`, and `visit_once` execution contracts
- deterministic closure/history receipts
- persistent recursion as suspend/resume rather than fake termination
- deny-by-default implicit capture of linear Portal/Road/QSTATE resources across recursion boundaries

Deferred:
- mutual/SCC recursion proofs
- higher-kinded/structural recursion over all Section 14 algebraic data types
- tail-call elimination
- recursion across distributed Section 16 schedulers
- unrestricted recursive capture of linear resources
