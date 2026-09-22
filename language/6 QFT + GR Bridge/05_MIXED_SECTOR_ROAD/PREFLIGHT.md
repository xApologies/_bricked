# Mixed-Road Preflight

Given source address `A/S0` and ordered target addresses:

```text
for target in waypoints:
    if target.sector != current.sector:
        validate Bridge(current.sector -> target.sector)
        append BRIDGE at current.domain
        current.sector = target.sector

    if target.domain != current.domain or target.boundary/logical address differs:
        select Corridor in current.sector
        append PORTAL(current -> target)
        collect capacity hold
        current = target
```

All Bridge checks and Corridor selections complete before the Road acquires its Rainbow Bus hold.
