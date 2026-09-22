# Memory Model

Genesis Section-01 uses a three-layer memory model:

1. **Fabric ROM** — immutable global substrate.
2. **Runtime Overlay** — sparse mutable state keyed by `FabricAddress128`.
3. **Receipt Log** — append-only transition/provenance records.

Reads resolve:

```text
read(address):
    if overlay contains address:
        return overlay[address]
    else:
        return fabric[address]
```

Writes resolve:

```text
stage(address, cell)
commit() -> receipt
```

No operation mutates the mounted base fabric.

## Geometric instantiation

An MMO/Geometric is instantiated as a region binding plus overlay state, not by rewriting the substrate:

```text
GeometricInstance = {
    fabric_identity,
    region,
    occupancy/field overlay,
    identity,
    ancestry,
    provenance,
    closure state
}
```

This gives us a stable substrate with dynamic realized objects.
