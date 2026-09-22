# GVM 0.1 machine model

## State

`MachineState = (PC, Registers, Resources, FabricMounts, Ownership, Frames, Ledger, BackendState)`

### Registers

The reference VM exposes 256 typed virtual registers per frame. A register contains a tagged value or a resource handle. Registers are implementation-level slots; they are not the same thing as chirality fabric cells.

### Resource table

Identity-bearing values are stored as immutable/versioned backend resources and referenced by deterministic handles. Examples: `GEOMETRIC`, `PORTAL`, `ROAD`, `BRIDGE`, `QSTATE`, `RECEIPT`.

### Fabric address space

GVM has dedicated fabric instructions. Generic register operations cannot rewrite the Section 01 base fabric. `FABRIC_WRITE_OVERLAY` delegates to the hardware ABI/overlay contract.

### Ledger

Every persistent semantic operation may emit a receipt. The VM ledger is append-only and content-hashed.

### Control flow

GVM has explicit `JUMP`, `BRANCH`, `CALL`, `RETURN`, and `HALT`. GIR v0.1 compilation focuses on acyclic semantic graphs; explicit control-flow lowering is available directly at GVM level and is reserved for the source-language frontend/compiler stage.
