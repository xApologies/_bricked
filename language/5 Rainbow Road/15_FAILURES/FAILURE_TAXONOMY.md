# Section-05 Failure Taxonomy

Inherited Section-04 failures remain valid per Portal leg. Road-specific failures add:

* `EMPTY_ROAD` — no waypoint/Portal leg declared.
* `ROAD_COMPOSITION_FAILED` — Portal boundaries or preservation contracts do not compose.
* `ROAD_SECTOR_MISMATCH` — cross-sector Road attempted without explicit bridge layer.
* `ROAD_CAPACITY_HOLD_FAILED` — Rainbow Bus cannot lease all preflight requirements.
* `ROAD_ROUTE_DRIFT` — actual Portal route differs from preflight under the Road lease.
* `ROAD_END_TO_END_CLOSURE_FAILED` — final invariant audit fails.
* `FAILED_PARTIAL` — one or more Portal legs closed before a later failure.

`FAILED_PARTIAL` is not corruption. It is a precise history state.
