# Design invariants

**S03-I01 Parent immutability** — committed parents are never overwritten.

**S03-I02 Base-fabric immutability** — transformations write only immutable child delta segments.

**S03-I03 Explicit effects** — every operator declares the fields/classes it may change.

**S03-I04 Capability admission** — effects outside the active capability profile fail before commit.

**S03-I05 Explicit semantic identity** — cell-level change never silently becomes a new molecular identity.

**S03-I06 Address containment** — every patch record lies inside the inherited FabricRegion.

**S03-I07 Deterministic plan** — equivalent canonical requests over the same parent root produce the same plan identifier.

**S03-I08 Content-addressed closure** — pre-state, patch, and post-state roots are recorded.

**S03-I09 Invariant preservation** — declared invariants are verified over changed cells and object metadata.

**S03-I10 Ancestry monotonicity** — child history extends parent history; it does not rewrite it.

**S03-I11 R-domain chirality read-only** — the `PIPELINE_R` capability profile rejects chirality/occupancy writes.

**S03-I12 Representation is not identity** — QFT, GR, 3+1+1, hardware-cell and other representations remain typed projections unless an explicit equivalence is declared elsewhere.
