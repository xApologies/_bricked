# Section 08 recovery state

**Canonical folder:** `GENESIS_CHIRALITY_MACHINE_SECTION_08_VM_IR_v0.1.0_20260821`

## Established in this section

- GIR 0.1 typed graph IR is the canonical source-neutral compiler target.
- GVM 0.1 is the deterministic executable lowering target.
- Future Genesis text compiles to GIR; GIR lowers to GVM; GVM dispatches through backend ABI to Sections 01–07.
- Python is bootstrap/reference implementation only.
- VM storage is split into registers, resource table, fabric address space, overlay state, ledger, and frames.
- Base chirality fabric is not a generic mutable heap.
- Identity-bearing resources and closure receipts are machine-visible.
- QSTATE remains linear and measurement is explicit.
- QFT/GR sector transition requires an explicit bridge witness.
- `.gvm` deterministic bytecode format v0.1 established.
- First Portal, two-leg Rainbow Road, mixed-sector, and quantum-effect GIR fixtures compile and run through the reference VM.

## Next engineering layer

Section 09 should define the **Genesis static type/effect checker + semantic linker** at the language/compiler boundary: parametric typestates, object/API symbol resolution, module imports, capability checking, proof-obligation generation, and linking GIR graphs into executable programs.
