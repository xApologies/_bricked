# Instruction semantics notes

## Hardware/fabric group

`FABRIC_MOUNT`, `FABRIC_ALLOC`, `FABRIC_READ`, and `FABRIC_WRITE_OVERLAY` are the only direct hardware-facing instructions in v0.1. They delegate to Section 01. The write opcode means **overlay/derived-state write**, never an unrestricted rewrite of the immutable base fabric image.

## Geometric group

Instantiation and transformation instructions delegate to Sections 02–03 semantics: child states have explicit ancestry and closed parents remain immutable.

## Portal/Road group

Portal operations preserve the separation between Portal transaction and Corridor admission/routing established by Sections 04–05. Road instructions compose closed Portal receipts rather than merging all legs into one untyped mutation.

## Sector bridge

`BRIDGE_SECTOR` delegates to Section 06. It is an explicit transduction witness; it does not assert QFT=GR.

## Quantum group

QSTATE instructions delegate to Section 07 semantic contracts. They are optional sector-scoped resources and obey linear/no-cloning rules.

## Projection/provenance

BRANE lift and receipts are explicit machine operations because realization/provenance are part of the execution contract, not incidental logs.
