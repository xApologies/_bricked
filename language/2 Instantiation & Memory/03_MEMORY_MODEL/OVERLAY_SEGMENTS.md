# Geometric Overlay Segment (`.gos`) v1

Large MMOs are streamed into an immutable segment instead of materializing hundreds of thousands of Python cell objects.

## Record

Each sorted record is:

```text
cell_index : u64
cell_bytes : 32 bytes (ChiralityCell32)
```

Record size: 40 bytes.

## Superblock

4096 bytes containing:

- magic `GOSMMO01`
- version
- record size
- record count
- parent fabric tag
- region start/count
- MMO identity digest
- instance identity digest
- payload SHA-256
- source-manifest SHA-256

The file becomes immutable at COMMIT. Binary search permits readback without loading the whole segment.
