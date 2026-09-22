# Optimization levels

- **O0** — no GIR rewrite; code generation only.
- **OAUDIT** — canonicalization and duplicate-edge removal only.
- **O1** — all v0.1 locally proven pure rewrites.

There is deliberately no O2/O3 in Section 11 v0.1. Cross-effect and topology-aware optimization requires additional formal proofs rather than a more aggressive flag.
