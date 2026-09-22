# `.gtd` — Geometric Transformation Delta

`.gtd` is an immutable sparse child-state segment.

## Header

The first 4096 bytes contain a fixed header including:

- magic/version/record size;
- record count;
- fabric tag;
- inherited region start/count;
- parent-instance digest;
- child-instance digest;
- transformation-plan digest;
- pre-state root;
- post-state root;
- payload hash.

## Records

Each record is:

```text
uint64 fabric_cell_index
32-byte ChiralityCell
```

Records are strictly increasing and unique.

A zero-record `.gtd` is valid for an `INHERIT`-only fork and must have identical pre/post state roots.
