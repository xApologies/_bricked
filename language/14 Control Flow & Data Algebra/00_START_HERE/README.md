# Genesis Chirality Machine — Section 14
## Control Flow + Data Algebra

Section 14 adds explicit control-flow regions and algebraic data values above the existing Chirality Machine stack. It keeps the Section 08 opcode identities and adds a backward-compatible GVM/CF extension at `0x0080+`.

Implemented here: immutable scalar values, records, enums, `OPTION<T>`, `RESULT<T,E>`, `if/else`, exhaustive `match`, statically bounded `repeat N`, deterministic bytecode, and a path-aware CFG verifier for QSTATE linearity plus Portal/Road closure.

Dynamic unbounded repetition is intentionally deferred to Section 15 so recursion and termination/closure can be designed together rather than hidden in the host runtime.
