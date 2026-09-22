# Portal Object

A Portal is a first-class transaction object:

```text
Portal(
    source_address,
    target_address,
    payload_geometric,
    sector,
    route_policy,
    preservation_contract,
    resolution_required,
    bandwidth_required,
    closure_contract
)
```

The Portal is *not* the Corridor. The Portal requests and reserves one admissible Corridor, transports over it, and records the Corridor as a witness.

## Source/target address

An implementation address contains:

```text
domain_id
boundary_id
logical_location
sector
recursive_order
fabric_tag (when physically realized)
```

This is an implementation projection of the richer Chirality Address in `corridor.md`.

## Portal sectors

`GENERIC`, `QFT`, `GR` are defined in Section 04. An edge can advertise one or more sectors. A route changing sectors is rejected unless every sector transition is covered by an explicit bridge capability. Section 04 ships only same-sector examples.

## Transport mode

`RE_REALIZE` is canonical Section-04 transport: reconstruct the complete source Geometric state into a distinct destination fabric region while preserving declared invariants and source immutability.
