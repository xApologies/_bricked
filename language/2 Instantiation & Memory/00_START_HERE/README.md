# Genesis Chirality Machine — Section 02
## Geometric Instantiation Engine + MMO Memory Model

**Version:** 0.1.0  
**Date:** 2026-08-21  
**Status:** executable implementation baseline  
**Parent:** Section 01 — Hardware ABI / Immutable Chirality Fabric

Section 02 defines how a Mapped Molecular Object (MMO), called a **Geometric** when realized for execution, becomes live state on a mounted Chirality Fabric.

The section does **not** redefine molecular physics, chirality ontology, or BRANE. It defines the implementation bridge:

```text
canonical MMO
    -> selected scientific representation
    -> instantiation plan
    -> fabric region reservation
    -> geometric overlay segment
    -> live GeometricInstance
    -> M^5 organizational descriptor
    -> BRANE supplies realization Z
```

## Primary decisions

1. **MMO identity is not instance identity.** One canonical MMO may have many live Geometric instances.
2. **Scientific 3+1+1 is not BRANE M^5.** The adapter is explicit.
3. **The immutable Chirality Fabric is not rewritten.** Geometrics inhabit immutable overlay segments and later deltas.
4. **Large objects are streamed.** A 32^3 MMO does not require hundreds of thousands of Python objects in RAM.
5. **Scientific representation is preserved by hash/reference.** The fabric projection is an execution representation, not the entire molecular object.
6. **Instantiation is transactional.** PLAN -> RESERVE -> MATERIALIZE -> VERIFY -> COMMIT -> LIVE.
7. **A committed segment is immutable.** Mutation creates a delta/child segment and ancestry receipt.
8. **BRANE Z is not generated here.** Section 02 emits M^5; BRANE owns request-relative realization.

## Recovery order

1. `01_ARCHITECTURE/ARCHITECTURE.md`
2. `02_OBJECT_MODEL/MMO_GEOMETRIC_ABI.md`
3. `03_MEMORY_MODEL/GEOMETRIC_MEMORY_MODEL.md`
4. `04_INSTANCE_LIFECYCLE/INSTANCE_STATE_MACHINE.md`
5. `05_FIELD_ADAPTERS/SCIENTIFIC_3P1P1_ADAPTER.md`
6. `07_INSTANTIATION_ENGINE/INSTANTIATION_ALGORITHM.md`
7. `08_BRANE_LIFT/BRANE_M5_ADAPTER.md`
8. Run the tests in `12_TESTS`.

The executable reference package is under `10_REFERENCE_IMPLEMENTATION/genesis_geometric_engine`.
