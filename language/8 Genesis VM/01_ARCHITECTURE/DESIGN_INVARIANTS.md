# Design invariants

1. GIR is graph-native; textual Genesis syntax is not required to define the machine.
2. GVM is deterministic for a fixed program, input resource set, backend version, and declared measurement seed/input.
3. Base chirality fabric is never mutated through generic VM memory stores.
4. Fabric writes require the `WRITE_OVERLAY` effect and backend support for Section 01 overlay semantics.
5. Identity-bearing resources are referenced by handles, not copied as untyped blobs.
6. Persistent transformations produce new state/ancestry; they do not silently mutate a closed parent Geometric.
7. Portal and Road execution must close or expose an explicit partial/failure frontier.
8. Sector changes require explicit `BRIDGE_SECTOR`; QFT and GR are not silently interchangeable.
9. Nonclassical quantum resources are linear. GVM move/copy rules cannot clone a live QSTATE.
10. Measurement is an explicit effect and typestate transition.
11. Provenance and closure are machine-visible results, not logging side effects.
12. Python is the bootstrap oracle, not the semantic authority.
