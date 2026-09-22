# Readout Contracts

`rho_Q` and `rho_G` are implemented as **descriptor constructors** over a known Geometric state.

```text
rho_Q(instance,address) -> QFT SectorRepresentation
rho_G(instance,address) -> GR  SectorRepresentation
```

The descriptors bind to the same immutable `FabricWitness` when they are readouts of the same content/residue/identity state.

This is deliberately weaker than claiming a completed physical representation functor. It is strong enough for compiler/runtime typing, provenance, sector admission, and bridge composition.
