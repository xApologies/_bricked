# Sector Representation Model

A `SectorRepresentation` is a typed readout descriptor over a realized Geometric.

Common fields:

```text
representation_view_id
sector = QFT | GR
source_instance_id
canonical_mmo_id
content_root
residue_root
fabric_witness_id
address
projection_profile
invariants
payload
status
```

## QFT payload

The reference payload can record:

* state class (`PURE_DESCRIPTOR`, `DENSITY_DESCRIPTOR`, `FIELD_HANDOFF_DESCRIPTOR`);
* coherence policy;
* superposition capability declaration;
* entanglement relation references;
* measurement state;
* normalization policy;
* canonical-Q handoff reference.

It is metadata for the software execution model; Section 06 does not synthesize an actual physical wavefunction from arbitrary MMO bytes.

## GR payload

The reference payload can record:

* manifold/geometry representation ID;
* boundary and topology references;
* connection/curvature handoff status;
* metric-readout status;
* orientation/holonomy witness references;
* Time-Shell/continuity-projection lineage.

Again, these fields type the representation boundary. They do not manufacture a metric tensor where the source has not supplied one.
