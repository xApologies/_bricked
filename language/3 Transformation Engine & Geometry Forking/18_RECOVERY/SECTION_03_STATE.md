# Section 03 recovery state

**Release:** GENESIS_CHIRALITY_MACHINE_SECTION_03_TRANSFORMATION_ENGINE_v0.1.0_20260821

**Status:** IMPLEMENTED / REFERENCE-VALIDATED

**Core rule:** a committed Geometric is not mutated in place. Every admitted transformation creates an immutable `.gtd` delta, a child instance, a closure receipt, and monotonic ancestry.

**Execution boundary:** Section 03 operates on Section 02 Geometrics instantiated on the Section 01 immutable chirality fabric.

**Capability rule:** `PIPELINE_T` may write chirality/occupancy; `PIPELINE_R` is chirality/occupancy read-only.

**Semantic identity:** low-level field edits do not automatically define a new molecule. `PRESERVE_MMO`, `DERIVE_REPRESENTATION`, and explicit `DERIVE_MMO` are separate policies.

**Verification:** 23/23 unit tests pass. Real fixture transformations for HSV-1, Hydrogen, Oxygen, and Blank preserve parent segments and base fabric byte-for-byte.

**Next section:** Section 04 should implement Portal transaction semantics and Corridor admission/transport over transformed Geometrics, using Section 03 closure receipts as the state-transition primitive.
