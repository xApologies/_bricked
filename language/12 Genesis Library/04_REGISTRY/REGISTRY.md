# Local registry

The reference registry is a filesystem tree:

```text
REGISTRY/
  genesis.std.fabric/
    0.1.0/
      genesis.pkg.json
      src/...
```

The runtime scans and hashes entries. No network lookup exists in Section 12. This is deliberate: deterministic package semantics are established before distribution policy.
