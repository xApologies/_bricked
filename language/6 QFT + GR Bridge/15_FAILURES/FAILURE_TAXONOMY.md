# Section-06 Failure Taxonomy

* `UNSUPPORTED_SECTOR_PAIR` — no explicit Bridge contract exists.
* `SECTOR_IDENTITY_COLLAPSE` — implementation attempted to equate QFT and GR representations.
* `INVERSE_REQUIRED` — operation requires an undeclared inverse map.
* `COMMON_ANCESTRY_MISMATCH` — sector views do not bind to one fabric witness.
* `BRIDGE_CONTENT_DRIFT` — content root changed during readout transduction.
* `BRIDGE_RESIDUE_DRIFT` — invariant residue changed.
* `BRIDGE_PROVENANCE_BREAK` — required identity/provenance lineage is missing.
* `BRIDGE_SOURCE_MUTATED` — source segment chain changed.
* `BRIDGE_FABRIC_MUTATED` — base fabric changed.
* `MIXED_ROAD_PREFLIGHT_FAILED` — at least one Bridge/Corridor action cannot be admitted before execution.
* `MIXED_ROAD_FAILED_PARTIAL` — prior Portal/Bridge actions closed but a later action failed.
* `PORTAL_SECTOR_MISMATCH` — a Portal attempted to cross sector without Bridge.
