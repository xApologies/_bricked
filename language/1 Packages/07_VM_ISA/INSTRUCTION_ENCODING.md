# Instruction Encoding

The Python emulator uses a portable JSON/structured instruction form first. A compact 16-byte binary encoding is reserved for later hardware lowering:

```text
u8 opcode
u8 flags
u8 dst
u8 src_a
u8 src_b
u8 imm_kind
u16 reserved
u64 immediate
```

Complex object handles live in machine tables referenced by register/index. This keeps the low-level record fixed-width without forcing MMO/Portal semantics into raw scalar registers.
