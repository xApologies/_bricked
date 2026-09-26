# GENESIS / CHIRALITY FABRIC — FULL THREAD RECOVERY R61

**Package:** `GENESIS_CHIRALITY_FABRIC_FULL_THREAD_RECOVERY_R61_v1_0_20260829`  
**Date:** 2026-08-29  
**Mode:** cumulative, loss-resistant, provenance-preserving thread recovery  
**Primary QMO:** `@qmo/genesis_chirality_fabric_r61`  
**Current frontier:** native multiscale chirality update mechanism

## What this package is

This ZIP is the portable recovery surface for the current GENESIS / Chirality Fabric investigation. It preserves the current mathematical state, the full thread chronology, source/provenance receipts, supersessions, open debt, the R60–R61 update-mechanism work, selected source snapshots, and a queryable SQLite QMO with a mini API.

The package is intentionally self-contained for continuity. Very large parent archives are **not duplicated**; they are referenced by exact filename, byte size, SHA-256, role, and authority. The current mathematics needed to resume the thread is carried directly in this package.

## Three-minute recovery

1. Read `01_CANON/CANONICAL_CURRENT_STATE.md`.
2. Read `04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md`.
3. Read `03_VERA/AUTHORITY_SUPERSESSION_AND_FIREWALLS.md`.
4. Query `07_MACHINE/genesis_chirality_recovery.sqlite` through `07_MACHINE/qmo_api.py`.
5. Resume at `@open/native_multiscale_update_law` without reopening every parent branch.

## SQLite / QMO examples

```bash
python 07_MACHINE/qmo_api.py info
python 07_MACHINE/qmo_api.py address @object/chirality_block
python 07_MACHINE/qmo_api.py address @eq/torus_update
python 07_MACHINE/qmo_api.py neighbors @object/chirality_tile --direction both
python 07_MACHINE/qmo_api.py search "Bandwidth"
python 07_MACHINE/qmo_api.py list open_debt
```

Optional local HTTP server:

```bash
python 07_MACHINE/qmo_api.py serve --host 127.0.0.1 --port 8797
```

## Current one-line result

> A block-level chirality update is not a repainting of the block. It is a closure-admissible path of tile-level color/energy-density updates whose relational effects propagate through seed, byte/bite, block, and Time-Shell organization, with History changing the future set of admissible updates.
