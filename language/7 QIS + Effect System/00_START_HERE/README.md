# Genesis Chirality Machine — Section 07
## Quantum Information State + Effect System

**Version:** 0.1.0 — software reference implementation
**Date:** 2026-08-21

Section 07 adds quantum-information semantics to the Genesis Chirality Machine without redefining the chirality fabric as a qubit array and without claiming that the present software emulator is quantum hardware.

The section introduces:

- pure and density-state reference representations;
- superposition as coherent state-space structure, not classical duplication;
- entanglement as a joint nonseparable relationship, not a transport channel;
- unitary/isometric/CPTP-style channel classes;
- projective measurement and classicalization boundaries;
- linear ownership and explicit no-cloning enforcement for nonclassical state handles;
- coherence, trace, normalization, purity, fidelity, and recoverability diagnostics;
- quantum effect contracts for `Portal<QFT>`;
- an explicit rule that QFT/GR transduction does **not** automatically preserve quantum coherence or entanglement;
- BRANE M5 effect/provenance lift fields;
- a small generic finite-dimensional reference simulator used only as an execution oracle for future Genesis language semantics.

### Governing distinction

```text
chirality fabric            = common organizational substrate in the project architecture
quantum-information state   = optional typed state carried/read in the QFT sector
entanglement                 = joint state relationship
Portal                       = information transport transaction
Corridor                     = admissible transport path
Rainbow Road                 = persistent composition of Portals
Bridge<QFT,GR>               = typed representation transduction, not an assumed quantum channel
```

### Scope boundary

Everything in Section 07 is a **software reference semantics**. It is designed to make the future Genesis compiler precise. It does not claim that an MMO, a chirality fabric cell, or a QFT/GR bridge has been physically realized as quantum hardware.
