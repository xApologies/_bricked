# ChiralityCell32 ABI

The canonical scientific object is a structured chirality arrangement. `ChiralityCell32` is a hardware representation.

## 32-byte layout

| Offset | Field | Type | Meaning |
|---:|---|---|---|
| 0 | occupancy_pattern | u8 | serialized 8-site occupancy projection |
| 1 | complement_pattern | u8 | optional mirror/complement witness |
| 2 | handedness | i8 | -1 left, 0 unresolved/other, +1 right |
| 3 | state_class | u8 | backend-neutral state/basin class |
| 4 | sigma | u16 Q0.16 | admissibility |
| 6 | chi | u16 Q0.16 | chirality magnitude/transport readiness representation |
| 8 | rho | u16 Q0.16 | persistence |
| 10 | lambda_ | u16 Q0.16 | locality |
| 12 | tau | u16 Q0.16 | translation readiness |
| 14 | flags | u16 | implementation flags |
| 16 | adjacency_index | u32 | optional adjacency-table row |
| 20 | lineage_index | u32 | optional lineage/provenance row |
| 24 | identity_tag | u64 | local identity handle/hash fragment |

## Canonical serialized witnesses

Recovered representations include:

- RIGHT: `01101001` (`0x69`)
- LEFT:  `10010110` (`0x96`)

These byte values are **representations**, not the ontology. The cell API exposes conversion to/from explicit 2×2×2 occupancy tuples.

## Open adjacency gate

The exact scientific adjacency law for the eight-site mote remains source-open. The emulator supports explicit adjacency tables and test topologies but does not promote a guessed adjacency graph to canon.
