# Effect system

Effects describe what a transformation *may* change, independent of whether a particular execution changes every such field.

Core effects:

- `READ`
- `ADMISSIBILITY_WRITE` (`sigma`)
- `CHIRALITY_WRITE` (`chi`, handedness/chiral class)
- `OCCUPANCY_WRITE` (occupancy/complement patterns)
- `PERSISTENCE_WRITE` (`rho`)
- `LOCALITY_WRITE` (`lambda`)
- `TRANSLATION_WRITE` (`tau`)
- `FLAGS_WRITE`
- `ADJACENCY_WRITE`
- `LINEAGE_WRITE`
- `IDENTITY_TAG_WRITE`

Effect sets are checked against a capability profile before execution.

The effect system is also the future lowering point for Genesis language effects and Portal sector rules.
