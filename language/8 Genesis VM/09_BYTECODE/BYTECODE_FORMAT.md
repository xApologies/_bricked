# `.gvm` bytecode format v0.1

All multibyte integers are big-endian.

## File header

```text
4 bytes   magic = "GVM1"
2 bytes   major version
2 bytes   minor version
4 bytes   instruction count
4 bytes   metadata JSON length
32 bytes  SHA-256 of metadata + encoded instruction records
N bytes   canonical metadata JSON
...
```

## Instruction record

```text
2 bytes   opcode
2 bytes   output register (0xFFFF = no output)
2 bytes   argument count
2 bytes   flags
4 bytes   canonical JSON payload length
N bytes   payload {"args": [...], "attrs": {...}, "source": ...}
```

The first bytecode is deliberately transparent and auditable rather than maximally compact. A future packed encoding may be introduced without changing GIR/GVM semantics.
