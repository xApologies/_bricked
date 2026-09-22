# Genesis Chirality Machine — Section 10
## Genesis Surface Language + Frontend Compiler

**Version:** 0.1.0  
**Date:** 2026-08-21

Section 10 is the first executable textual projection of the Genesis programming language.

Sections 01–09 established the machine below it: chirality hardware ABI, Geometric instantiation, transformations, Portals, Rainbow Road, QFT/GR transduction, quantum-information effects, GIR/GVM, and static semantics/linking. Section 10 adds the frontend that converts source text into that already-defined semantic machine.

```text
Genesis source (.gen)
      |
      v
lexer / statement parser
      |
      v
Genesis AST
      |
      v
semantic lowering + source map
      |
      v
GIR-MODULE
      |
      v
Section 09 static checker + semantic linker
      |
      v
Section 08 GIR/GVM compiler
      |
      v
Sections 01–07 backends
```

### Critical architectural law

**The text is a projection of the program; the typed relationship graph is the executable semantic object.**

The v0.1 frontend therefore does not redefine the machine semantics. It only provides a deterministic way to name, relate, transform, transport, close, and export objects that Section 09 can verify.

### Source Genesis boundary

The computational language intentionally borrows relationship-first mnemonic roots such as `en`, `rel`, `ve`, `ar`, and `tor` from the reconstructed Source Genesis corpus. This does **not** claim that the historical/reconstructed spoken language already contained compiler semantics. Source Genesis and Computational Genesis remain distinct source layers.
