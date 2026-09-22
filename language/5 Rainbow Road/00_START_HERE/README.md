# Genesis Chirality Machine — Section 05
## Rainbow Road Composition Engine

Version `0.1.0` — implementation layer.

Section 05 composes closed Section-04 Portal transactions into persistent **Rainbow Road** objects.

### Canonical implementation distinction

```text
Rainbow Bus  = available transport/capacity fabric.
Corridor     = one mathematically admissible route.
Portal       = one typed transfer transaction over a Corridor.
Rainbow Road = persistent ordered composition of closed Portals.
```

A Rainbow Road is therefore not an alias for a network path and not one oversized Portal. It is a first-class, inspectable, hash-addressed history object whose identity includes its ordered Portal/Corridor witnesses.

### Section-05 execution path

```text
closed Geometric / MMO
      -> Road declaration
      -> waypoint + sector + invariant validation
      -> per-leg Corridor preflight
      -> Rainbow Bus capacity hold
      -> Portal_1 OPEN/XFER/CLOSE
      -> inherited intermediate Geometric
      -> Portal_2 OPEN/XFER/CLOSE
      -> ...
      -> end-to-end invariant audit
      -> transport-holonomy witness
      -> ROAD CLOSED receipt
      -> final Geometric history/provenance inheritance
      -> BRANE M^5 road re-lift
```

### Failure law

Rainbow Road is **append-only**. A closed Portal is history and is never erased to simulate rollback. If a later leg fails, the Road resolves as `FAILED_PARTIAL`, preserving every completed Portal receipt and releasing only still-held scheduling capacity. This is deliberate: history is part of identity.

### Scope boundary

Section 05 executes same-sector roads (`GENERIC`, `QFT`, `GR`). Explicit QFT<->GR transduction/bridge execution remains the next dedicated layer. The bridge mathematics travels with this release but is not silently treated as a reversible identity map.
