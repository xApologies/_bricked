# Road Preflight

For each declared waypoint pair:

```text
source_i -> target_i
```

construct a synthetic Section-04 Portal request using the Road's invariant requirements, then ask the Corridor graph for the deterministic best admissible path.

Preflight returns:

```text
leg index
source address
target address
Corridor path ID
edge IDs
domains
color trajectory
minimum Resolution
minimum Bandwidth
cost
```

The Road plan then computes:

```text
Road min Resolution = min(all leg minima)
Road min Bandwidth  = min(all leg minima)
Road cost           = sum(all leg costs)
Rainbow trajectory  = ordered concatenation of edge colors
Capacity hold       = max sequential units required per edge
```

Preflight is non-mutating and must finish before Road capacity is held.
