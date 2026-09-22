# Section 13 — Callable Abstractions, Functions + Generics

Section 13 adds reusable callable abstractions to Genesis without changing the semantic machine established in Sections 01–12.

The key rule is that a Genesis function is **not a new runtime ontology**. It is a typed, effect-bounded, parameterized relationship-graph template. Static calls are specialized (monomorphized), alpha-renamed, and expanded before GIR is handed to the Section 09 static semantics/linker. The ordinary Section 08 GVM therefore continues to execute the same machine operations it already understands.

Pipeline:

```text
Genesis 0.2 callable surface
  -> callable AST
  -> function import/visibility resolution
  -> generic constraint checking
  -> recursion/termination check
  -> deterministic specialization
  -> alpha-renamed expansion to Genesis 0.1 core source
  -> Section 10 frontend
  -> Section 09 static type/effect/link proof
  -> Section 11 optimizer/codegen
  -> Section 08 GVM
  -> Sections 01–07 execution substrate
```

This design makes functions a zero-overhead language abstraction in the reference implementation. It also prevents functions from bypassing Portal closure, QSTATE linear ownership, sector bridges, package effect budgets, or provenance rules; after expansion, those invariants are checked by the existing semantic machine.

## v0.1 callable ABI scope

Implemented:

- local and public functions;
- cross-module callable imports (`usefn`);
- explicit generic type parameters with bounds;
- typed parameters and typed single return;
- effect declarations checked against expanded body effects;
- nested non-recursive calls;
- deterministic monomorphization;
- collision-free alpha-renaming of function locals;
- callable receipts and proof ledgers;
- package-level direct dependency discipline for `usefn`;
- executable v0.2 standard-library callable packages;
- compatibility with Genesis 0.1 modules.

Deliberately not implemented yet:

- recursion or mutually recursive call graphs;
- dynamic dispatch / trait objects;
- runtime generic dictionaries;
- closures capturing lexical state;
- multiple return values;
- returning an input parameter as a fresh alias (the v0.1 ABI requires the returned value to be locally produced);
- a native GVM stack-frame value-passing ABI. The GVM already has control CALL/RETURN opcodes, but Section 13 does not pretend those are a complete typed function ABI.

Those omissions are explicit design boundaries, not hidden fallbacks.
