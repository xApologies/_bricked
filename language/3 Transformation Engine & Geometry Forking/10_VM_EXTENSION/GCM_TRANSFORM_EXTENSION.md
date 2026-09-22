# GCM ISA — Section 03 transformation extension

Section 01 already reserves `XFORM = 0x20` for transformation. Section 03 defines the higher-level transaction protocol lowered under that opcode rather than changing the base opcode map.

Logical micro-operations:

```text
XBEGIN   parent_instance, expected_root, capability
XAPPLY   operator_descriptor
XCHECK   invariant_contract
XCOMMIT  child_descriptor
XABORT   reason
```

These are IR/runtime transaction phases, not new physical opcodes in v0.1. A future binary ISA encoding may allocate sub-opcodes once Genesis IR stabilizes.
