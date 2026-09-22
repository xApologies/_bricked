# Section 14 Source Crosswalk

## Purpose
This crosswalk separates inherited machine contracts, new Computational Genesis design choices, established compiler concepts, and source-language inspiration. Section 14 does not retroactively rewrite any upstream source.

## Inherited executable contracts
- **Section 08 — Genesis VM / Intermediate Representation:** preserves the existing numeric identities for `JUMP`, `BRANCH`, `CALL`, `RETURN`, and `HALT`. Section 14 extends the instruction space at `0x0080+` for data algebra rather than renumbering the VM.
- **Section 09 — Static Type/Effect Checker + Semantic Linker:** supplies the proof-discipline precedent for verifying effects and resource obligations before execution.
- **Sections 01–07:** fabric, Geometric, Portal, Road, bridge, QFT/GR, and quantum resource semantics remain authoritative below the control/data layer.
- **Sections 10–13:** source frontend, optimization/codegen, packages, callables, and generics remain preserved compatibility layers. Section 14 does not redefine their existing syntax or semantics.

## New Computational Genesis choices in Section 14
The following are Section 14 implementation semantics, not claims about the historical/source Genesis language:
- `record` product types and `enum` sum types.
- `OPTION<T>` and `RESULT<T,E>` standard algebraic data forms.
- immutable `let` bindings for scalar/data values.
- `if/else` control regions.
- exhaustive `match` with a final `_` default when used.
- statically bounded `repeat N` lowered by compile-time expansion.
- GVM/CF data instructions `0x0080` through `0x008C`.
- the `CFG_PATH_V0_1` path-sensitive verifier.
- non-escaping branch/case/repeat-local values in v0.1.

## Established compiler concepts used as engineering machinery
Control-flow graphs, path-sensitive verification, SSA-style register uniqueness, algebraic data types, exhaustive pattern matching, and bounded loop unrolling are standard compiler/programming-language techniques. Their use here is engineering inheritance, not a claim that these mechanisms originate in MK43 or Source Genesis materials.

## Source Genesis corpus
The Source Genesis language documents are preserved as a linguistic/structural source layer. They inform the relationship-first character of Computational Genesis but do not establish the Section 14 keywords or compiler behavior. In particular, `record`, `enum`, `if`, `match`, and `repeat` remain explicitly Computational Genesis constructs.

## Chirality / physical-hardware status
Section 14 executes on the software reference Chirality Machine backend. It does not claim that consumer storage hardware exposes native chirality cells or that the software data opcodes are a physical instruction set. A future physical backend must implement the lower hardware ABI without changing the Section 14 observable language contract.

## Deferred authority
Unbounded iteration, recursive calls, recursive topology traversal, and termination/closure proofs are deliberately deferred to **Section 15 — Recursion + Recursive Topology Execution**. Section 14 does not hide those semantics inside Python.
