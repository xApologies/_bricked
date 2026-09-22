# Genesis Chirality Machine — Section 14 Release Notes

**Section:** 14  
**Title:** Control Flow + Data Algebra  
**Package version:** v0.1.0  
**Genesis source level:** 0.3.0  
**GVM/CF program level:** 0.2.0

## Release result
- Section 14 unit/conformance suite: **62/62 PASS**.
- Section 13 compatibility regression: **48/48 PASS**.
- Reference source builds/executions: **6/6 PASS**.
- Deterministic bytecode round-trip and digest tamper rejection are covered by the Section 14 tests.

## Implemented
Immutable scalar/data values, records, sum variants, `OPTION<T>`, `RESULT<T,E>`, `if/else`, exhaustive `match`, bounded `repeat`, GVM/CF data opcodes, and a path-sensitive control-flow verifier that carries linear quantum and Portal/Road closure obligations across every reachable path.

## Deliberately deferred
Unbounded loops, recursive execution, recursive topology traversal, phi/value joins, general mutation, and control regions inside generic callable bodies are not silently emulated. Their semantics belong to Section 15 or a later compatibility integration pass.
