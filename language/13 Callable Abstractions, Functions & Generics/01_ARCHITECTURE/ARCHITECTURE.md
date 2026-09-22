# Architecture

## Layer placement

Section 13 sits between human/source-level Genesis and the existing Section 10 frontend. It does not alter the Chirality Machine ISA, Fabric ABI, Geometric model, Portal engine, Rainbow Road, sector bridge, or quantum effect substrate.

```text
SOURCE GENESIS / COMPUTATIONAL GENESIS SURFACE
                    |
             Section 13
       callables + generics
                    |
       normalized core Genesis
                    |
             Section 10
                    |
      GIR-MODULE relationship graphs
                    |
             Section 09
      static type/effect/link proof
                    |
             Section 11
       optimizer + backend codegen
                    |
             Section 08 GVM
                    |
 Sections 01–07 Chirality Machine substrate
```

## Why specialization first

A native runtime function ABI could be built now, but it would introduce stack-frame ownership, resource passing, generic dictionaries, effect-frame closure, and QSTATE transfer rules before those mechanisms are needed. Static monomorphization reuses the already-tested semantic checker instead:

1. Resolve a function definition.
2. Bind concrete type arguments.
3. Verify generic bounds.
4. Bind value parameters.
5. Alpha-rename local identities.
6. Recursively expand nested calls.
7. Validate the function's effect declaration.
8. Emit ordinary core Genesis statements.
9. Re-run the full Section 09 proof system over the result.

The optimization target is BLACKGLASS/BRANE execution, so code size is permitted to grow in exchange for explicit static semantics and predictable machine behavior. A later optimizer may deduplicate equivalent specializations if doing so preserves ownership/effect/closure proofs.

## Identity rule

Function invocation does not grant an escape hatch from Object = History. A call's returned resource is the resource produced by the expanded underlying operations. The callable layer records a `gcall-*` call identity and `gmono-*` specialization identity as compiler/provenance metadata; these identifiers are not substituted for the underlying Geometric/Portal/receipt identities.

## Separation of concerns

- **Function:** reusable relationship-graph template.
- **Generic:** compile-time type parameter constrained by the Genesis type system.
- **Call:** compile-time instantiation event plus source-level provenance boundary.
- **GIR:** executable relationship graph after callable erasure.
- **GVM:** machine schedule after static semantics and optimization.

The function disappears as an executable primitive in v0.1, but its call/specialization trace remains in receipts.
