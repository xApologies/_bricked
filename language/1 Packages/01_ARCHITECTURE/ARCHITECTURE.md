# Architecture

## 1. Execution stack

```text
Genesis source
    ↓
Genesis IR
    ↓
Portal / Road IR
    ↓
Genesis Chirality Machine (GCM)
    ↓
Genesis Chirality Hardware Interface (GCHI)
    ↓
Immutable Chirality Fabric + Mutable Runtime Overlay
    ↓
Backend realization
    ├── Python/mmap emulator
    ├── CPU/RAM
    ├── GPU
    ├── block storage
    ├── FPGA
    └── future custom multilevel/analog hardware
```

BRANE/Trinity is realized *over* the mounted fabric. BLACKGLASS remains the operations, continuity, recovery, and provenance base around the whole stack.

## 2. Immutable fabric / dynamic occupancy split

The canonical substrate image is never mutated by normal execution.

```text
Fabric Image (read-only)
      +
Runtime Overlay (copy-on-write, append-only receipts)
      =
Operative Fabric View
```

This implements the project requirement that the persistent fabric can remain fixed while Geometrics/MMOs are instantiated, transformed, transported, and closed on top of it.

## 3. Physical-state rule

Every backend provides a codec:

`logical chirality state -> stored physical representation -> readback logical state`

The logical state is authoritative at the GCHI boundary. Voltage, charge, magnetization, resistance, integer code, or any other physical carrier is backend-specific.

Commodity SSDs and hard drives generally expose logical blocks through controllers rather than individual raw cell voltage. The emulator therefore models calibrated physical levels without pretending a consumer drive gives direct NAND-cell voltage control. Future FPGA/custom memory backends may implement tighter physical mappings.

## 4. No hidden CPU ontology

The machine may execute on x86-64 today. That does not make registers, stack frames, LOAD/STORE, or binary arithmetic the Genesis ontology. They are lowering targets.

The GCM machine exposes object-, fabric-, relationship-, chirality-, Portal-, and closure-oriented operations.
