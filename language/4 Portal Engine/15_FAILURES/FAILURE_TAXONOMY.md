# Failure Taxonomy

* `NO_CORRIDOR` — no path satisfies all hard predicates.
* `RESOLUTION_INSUFFICIENT` — route distinguishability below request.
* `BANDWIDTH_INSUFFICIENT` — route organizational freedom below request.
* `CAPACITY_EXHAUSTED` — implementation scheduling capacity unavailable.
* `CHIRALITY_MISMATCH` — route rejects payload chirality class.
* `RESIDUE_MISMATCH` — transported invariant residue differs.
* `SECTOR_MISMATCH` — Portal/QFT/GR sector not supported.
* `SOURCE_STALE` — caller's expected content root differs from current source.
* `DESTINATION_ALLOCATION_FAILED` — no target fabric region.
* `TRANSPORT_INTEGRITY_FAILED` — destination content differs or source/fabric mutated.
* `TARGET_CLOSURE_FAILED` — route does not resolve at requested target.

All runtime failures must emit a receipt when a Portal plan had already been created.
