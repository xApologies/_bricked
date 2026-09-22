# Design Invariants

- No ambient authority: every external action requires a declared capability.
- Host paths are implementation details; durable identities use hashes/object references.
- Source/canonical state is read-only during ordinary execution.
- Derived state may be written only inside declared derived endpoints.
- Audit state is append-only.
- Persistent BLACKGLASS/Heart state is not directly mutated by ordinary module code.
- Persistence crosses an explicit proposal/admission boundary.
- BRANE modules are validated as five-coordinate organizational modules; `Z` is host-owned.
- A module may not inject its own request-relative `Z` realization.
- Cross-boundary payloads are typed/reference-addressed; no shared-memory pointer mutation is semantic canon.
- Every successful or failed system request yields a receipt/witness.
- System I/O does not redefine Geometric, Portal, Rainbow Road, recursion, or concurrency semantics.
- Physical host parallelism and device-specific APIs remain backend realization choices.
