# Genesis Chirality Machine — Section 18

**Title:** Compiler Toolchain + Diagnostics + Debugging

Section 18 turns the executable Genesis stack into an operable development toolchain. It does not redefine Genesis semantics. It wraps the Section 17 compiler/runtime boundary with deterministic build orchestration, stable diagnostics, source maps, execution tracing, replay-oriented debugging, conformance test driving, and reproducible-build receipts.

## Boundary rule

Tooling observes, diagnoses, packages, traces, and reproduces. It may not weaken the verifier, bypass capability checks, mutate immutable source/CAS objects, or invent runtime authority.

## Reference command surface

`python -m genesis_toolchain check|build|run|disasm|trace|test|doctor ...`
