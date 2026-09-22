# Genesis Chirality Machine — Section 08
## Genesis Virtual Machine + Graph Intermediate Representation

**Version:** 0.1.0 — bootstrap software execution model  
**Date:** 2026-08-21

Section 08 defines the machine-facing execution language that future Genesis source syntax compiles into.

It intentionally has **two internal levels**:

1. **GIR — Genesis Graph Intermediate Representation**: semantic, typed, dependency-first, relationship-first, mostly SSA-like. It represents the program as a typed relationship/dependency graph.
2. **GVM — Genesis Virtual Machine**: deterministic register/resource machine that executes a scheduled/lowered form of GIR and dispatches semantic operations to Sections 01–07 through a backend ABI.

```text
future Genesis source syntax
          |
          v
         GIR                 semantic graph IR
          |
   verify / type / effect
          |
   deterministic scheduling
          v
         GVM                 machine execution IR / bytecode
          |
     backend ABI
          |
          +--> Section 01 hardware/fabric
          +--> Section 02 Geometric instantiation
          +--> Section 03 transformation/forking
          +--> Section 04 Portal/Corridor
          +--> Section 05 Rainbow Road
          +--> Section 06 QFT/GR transduction
          +--> Section 07 quantum-information effects
          |
          v
      BRANE / Trinity / BLACKGLASS
```

### Foundational decision

Python does **not** define Genesis semantics. Python is the current bootstrap implementation of the GVM and its reference backend. The normative contract is the typed GIR/GVM model, instruction semantics, verifier rules, effects, receipts, and backend ABI contained here.

### Machine principle

The VM does not treat the base chirality fabric as an ordinary mutable heap. Section 01 remains authoritative: base fabric identity is stable; writes occur through overlays/derived state. Persistent semantic changes are represented through new Geometric states, receipts, ancestry, provenance, and closure.

### Scope

This is a software execution model and compiler bootstrap target. It does not claim custom physical hardware has been manufactured. It is designed so the Python VM can later be replaced by a native, FPGA, GPU, or custom chirality-machine backend without changing Genesis language semantics.
