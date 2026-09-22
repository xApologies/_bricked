# Genesis Chirality Machine — Section 09
## Static Type/Effect Checker + Semantic Linker

**Version:** 0.1.0 — bootstrap static semantics and link layer  
**Date:** 2026-08-21

Section 09 sits immediately above the Section 08 GIR/GVM execution model. It answers a different question from the VM:

> **Before a Genesis relationship graph is allowed to execute, is it semantically well-formed, capability-compatible, ownership-safe, sector-correct, and closed?**

The section adds five machine-facing facilities:

1. a refined **parametric type system** for identity-bearing runtime resources;
2. **typestate and linear-resource checking** for Portals, Roads, and QSTATEs;
3. an explicit **effect budget** for fabric access, transformation, transport, closure, transduction, measurement, provenance, and control;
4. a **semantic module/linker format** that resolves typed imports/exports and alpha-renames graphs without flattening provenance;
5. a **backend capability contract** that rejects linked programs a target cannot realize.

```text
future Genesis source modules
          |
          v
typed GIR modules
          |
          +--> symbol resolution
          +--> static type / typestate checker
          +--> effect budget checker
          +--> proof-obligation ledger
          +--> backend capability check
          |
          v
semantic linker
          |
          v
one verified GIR graph
          |
          v
Section 08 compiler -> GVM -> backend ABI -> Sections 01..07
```

### Important boundary

Section 09 is still **below human-facing Genesis syntax**. It does not freeze keywords or grammar. Its interfaces are graph/module semantics that a future parser, graph editor, generated program, or other frontend can target.

### Status discipline

The static semantics and linker are a new computational synthesis constrained by Sections 01–08 and the project mathematics. They are not represented as recovered historical mathematics.
