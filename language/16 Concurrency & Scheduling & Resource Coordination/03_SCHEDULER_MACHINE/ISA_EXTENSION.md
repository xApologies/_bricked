# Section 16 scheduler ISA extension

Reserved reference opcode window:

- `0x00A0 WORK`
- `0x00A1 ACQUIRE`
- `0x00A2 RELEASE`
- `0x00A3 YIELD`
- `0x00A4 TASK_CLOSE`
- `0x00A5 RECURSION_SLICE`
- `0x00A6 ASSERT`

These are reference scheduler opcodes. They do not replace GIR/GVM; code generation may lower higher-level concurrency constructs into this scheduler contract or fuse them into a backend-specific equivalent with identical observable semantics.
