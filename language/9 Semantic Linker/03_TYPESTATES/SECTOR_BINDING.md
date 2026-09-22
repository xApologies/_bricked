# Sector binding and Bridge authority

Sector is a representation/transport refinement, not identity equivalence.

- `UNBOUND` may bind on first sector-specific Portal transport.
- `QFT -> QFT` and `GR -> GR` transport require no sector bridge.
- `QFT -> GR` or `GR -> QFT` requires a preceding explicit `BRIDGE_SECTOR` witness for the same Geometric lineage/value and target sector.
- A Bridge is authorization/evidence for transduction; it is not treated as a third Portal sector.

The checker records Bridge witnesses as `(geometric-value, from-sector, to-sector)`. A later sector-changing Portal must match one.
