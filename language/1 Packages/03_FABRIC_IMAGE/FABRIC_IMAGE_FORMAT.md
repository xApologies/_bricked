# Genesis Chirality Fabric Image Format (`.gcf`) v1

The `.gcf` artifact is an immutable, memory-mappable substrate image.

## Layout

```text
+---------------------------+ 0
| Superblock (4096 bytes)   |
+---------------------------+ 4096
| ChiralityCell32 array     |
| cell_count × 32 bytes     |
+---------------------------+
| optional adjacency table  |
+---------------------------+
| optional region table     |
+---------------------------+
| optional provenance table |
+---------------------------+
```

Version 0.1 fixtures use the cell array and sidecar metadata. Future format revisions may bring all optional tables in-band.

## Superblock

- magic: `GCFABR01`
- format_version: `1`
- cell_size: `32`
- page_size: `4096`
- cell_count: `u64`
- fabric_tag: `u64`
- cell_data_offset: `u64`
- source_manifest_hash: 32-byte SHA-256
- cell_data_hash: 32-byte SHA-256
- reserved/padding to 4096 bytes

## Integrity

The emulator verifies magic, ABI sizes, declared cell count, cell-data hash, and fabric tag before mounting.

A checkpoint never edits its parent image. It creates a child `.gcf` with a new hash and a lineage receipt naming the parent.
