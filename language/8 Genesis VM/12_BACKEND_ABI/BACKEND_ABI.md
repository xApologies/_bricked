# Genesis Machine Backend ABI 0.1

The GVM backend interface is semantic, not CPU-specific.

Required capability groups:

- `fabric.*` — Section 01 mounting/address/overlay operations;
- `geometric.*` — Sections 02–03 instantiation/fork/transform;
- `portal.*` — Section 04 Portal transaction realization;
- `road.*` — Section 05 Rainbow Road composition;
- `bridge.*` — Section 06 sector transduction;
- `quantum.*` — optional Section 07 QFT quantum-information effects;
- `brane.*` — BRANE M5 projection/realization handoff;
- `provenance.*` — receipts, ancestry, closure witnesses.

A backend declares a capability bitmap. Programs requiring unsupported capabilities fail before execution.
