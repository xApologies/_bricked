# Invariant contract

A TransformRequest declares which information must survive.

Metadata invariants:
- canonical MMO identity;
- parent ancestry link;
- fabric tag;
- FabricRegion;
- source representation lineage.

Cell-field invariants (optional):
- identity tag;
- occupancy pattern;
- handedness;
- chirality magnitude;
- admissibility;
- persistence;
- locality;
- translation readiness;
- adjacency index.

`STRICT_IDENTITY` preserves canonical MMO identity, fabric region, identity tags, and parent ancestry while permitting declared non-identity state effects.

`PRESERVE_CHIRALITY` additionally preserves occupancy, complement, handedness, and `chi`.

`READ_ONLY` requires an empty ChangeSet and identical pre/post state roots.

Closure fails if any declared invariant is violated.
