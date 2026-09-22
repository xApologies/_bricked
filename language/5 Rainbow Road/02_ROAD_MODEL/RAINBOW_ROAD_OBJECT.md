# Rainbow Road Object

A Road request is:

```text
RainbowRoadRequest(
    source_geometric,
    source_address,
    waypoints=[address_1, ..., address_n],
    sector,
    preservation_contract,
    chirality_class,
    residue_class,
    R_min,
    B_min,
    capacity_units,
    route_policy
)
```

The resulting Road has three distinct representations:

* **RoadTemplate** — reusable declared waypoint/constraint shape without a bound source instance;
* **RoadPlan** — source-bound, deterministic Corridor preflight and capacity-hold requirements;
* **RoadRun** — realized ordered Portal receipts plus end-to-end closure receipt.

A Road's identity is not merely `(start,end)`. Two Roads with the same endpoints but different Portal/Corridor histories are different Road realizations unless an explicit equivalence relation identifies them.
