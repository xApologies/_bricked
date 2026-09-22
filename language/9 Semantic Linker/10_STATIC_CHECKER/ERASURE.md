# Refinement erasure into Section 08

Section 09 refinements do not require changing the stable Section 08 bytecode type-tag enum.

```text
PORTAL<QFT,OPEN>        -> PORTAL
GEOMETRIC<CLOSED,GR>    -> GEOMETRIC
QSTATE<OWNED>           -> QSTATE
RECEIPT<PORTAL_CLOSE>   -> RECEIPT
```

The unified GIR carries a `metadata.section09.refined_types` map. Section 08 compiles the coarse `type` fields and executes the already-checked graph.
