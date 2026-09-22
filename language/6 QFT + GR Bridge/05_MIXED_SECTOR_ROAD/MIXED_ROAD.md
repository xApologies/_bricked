# Mixed-Sector Rainbow Road

Section 05 intentionally required one sector for an entire Road. Section 06 lifts that restriction only by making every sector boundary explicit.

Example:

```text
ALPHA/QFT
  --Portal<QFT>--> GREEN/QFT
  --Bridge<QFT,GR>--> GREEN/GR
  --Portal<GR>--> OMEGA/GR
```

The mixed Road is an ordered action list:

```text
PORTAL
BRIDGE
PORTAL
...
```

A sector change with no domain change is a Bridge-only action. A waypoint that changes both domain and sector expands into `BRIDGE` then `PORTAL` in the target sector.

The end-to-end Road receipt contains Portal receipts, Bridge receipts, a combined action trajectory, Corridor edge trajectory, sector trajectory, and common-ancestry witnesses.
