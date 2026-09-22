# Surface-to-GIR lowering

| Source form | GIR operation |
|---|---|
| `en x = mount ...` | `FABRIC_MOUNT` |
| `en x = alloc ...` | `FABRIC_ALLOC` |
| `en x = instantiate ...` | `GEO_INSTANTIATE` |
| `en x = fork ...` | `GEO_FORK` |
| `rel` | `RELATE` |
| `admit` | `ADMIT` |
| `transform` | `TRANSFORM` |
| `ar` | `INHERIT` |
| `portal` | `PORTAL_OPEN` |
| `ve` | `PORTAL_TRANSPORT` |
| `tor` | `PORTAL_CLOSE` |
| `road begin/append/close` | `ROAD_BEGIN/ROAD_APPEND/ROAD_CLOSE` |
| `bridge` | `BRIDGE_SECTOR` |
| `q prepare/superpose/entangle/channel/measure` | corresponding `Q_*` op |
| `lift` | `BRANE_LIFT` |
| `seal` | `PROVENANCE_SEAL` |
| `assert closure` | `ASSERT_CLOSURE` |
| `emit receipt` | `EMIT_RECEIPT` |

Every lowered node is chained in v0.1 source effect order. Data arguments still encode the actual dependency graph.
