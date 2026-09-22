# Hard barriers in v0.1

`FABRIC_*`, `GEO_*`, `RELATE`, `ADMIT`, `TRANSFORM`, `INHERIT`, `PORTAL_*`, `ROAD_*`, `BRIDGE_SECTOR`, all `Q_*`, `BRANE_LIFT`, `PROVENANCE_SEAL`, `ASSERT_CLOSURE`, and `EMIT_RECEIPT` are treated as effectful or semantic-barrier operations.

Pure v0.1 operations are limited to `NOP`, `CONST`, `MOVE`, and `HASH`, with extra restrictions for quantum values and alias coalescing.
