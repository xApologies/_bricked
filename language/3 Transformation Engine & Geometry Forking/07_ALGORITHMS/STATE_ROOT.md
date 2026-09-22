# State root

The Section 03 state root is a deterministic SHA-256 commitment over the operative Geometric region:

```text
for each fabric index in region order:
    hash(index_u64_be)
    hash(cell.pack())
```

The root commits to both address and cell content. It is intentionally representation-level: it proves exact reconstructed mapped state, not physical equivalence of two molecular systems.
