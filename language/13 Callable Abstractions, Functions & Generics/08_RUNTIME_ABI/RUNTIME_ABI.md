# Runtime ABI

Section 13 deliberately does not require a new GVM runtime opcode.

```text
source function call
    ↓ compile time
specialized relationship subgraph
    ↓
ordinary GIR operations
    ↓
ordinary GVM instructions
```

This is the current callable ABI: **static graph specialization**.

The Section 08 GVM already contains control-level CALL and RETURN opcodes, but those instructions presently model control transfer only. They do not yet define typed argument registers, return registers, stack-frame ownership, QSTATE transfer, effect frames, or generic dictionaries. Section 13 therefore does not misuse them as if a complete native function ABI already existed.

A later native-call section can add a typed GVM call-frame contract once profiling shows which callables should remain uninlined. Such a change should preserve Section 13 source semantics and be an implementation strategy change rather than a language meaning change.
