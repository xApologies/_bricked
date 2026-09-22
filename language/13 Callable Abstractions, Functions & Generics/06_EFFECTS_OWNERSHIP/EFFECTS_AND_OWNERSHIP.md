# Effects and ownership

Functions declare the maximum effects they may realize. The compiler calculates the union of underlying operation effects after nested callable expansion and requires:

```text
actual_effects ⊆ declared_effects
```

Examples include `ADMIT`, `TRANSPORT`, `INHERIT`, `CLOSE`, `PROVENANCE`, `TRANSDUCE`, `QUANTUM_LINEAR`, `MEASURE`, `PROJECT`, `TRANSFORM`, and fabric effects.

This is intentionally a containment rule rather than an exact-equality rule so a stable public callable contract can conservatively advertise effects while implementations evolve internally.

## Quantum linearity

Function parameters do not copy values. After monomorphization, the ordinary Section 09 checker sees the actual QSTATE uses. Therefore:

```text
q entangle q q as result
```

inside a function still fails with the same linear alias violation it would fail with at top level.

## Portal/Road typestates

A function that opens a Portal but fails to close it fails Section 09 after expansion. A function that returns while a Road remains open similarly fails. Function boundaries do not reset typestate.

## Sector bridges

A callable may package an explicit QFT/GR bridge operation, but the bridge witness must still be used by the underlying Portal operation. A generic function cannot claim `QFT -> GR` merely by changing its return annotation.
