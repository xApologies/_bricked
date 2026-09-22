# Design invariants
- Chirality fabric remains the lower machine substrate.
- Every statically reachable halting path must close Portal/Road resources.
- QSTATE linear ownership is verified per control path.
- Records and variants are immutable.
- Match over a closed sum is exhaustive unless `_` is present.
- `repeat N` is finite and bounded to `0..4096`.
- Branch/case/repeat locals do not escape their lexical region.
- Identical source produces identical bytecode.
- Python is a reference emulator, not the semantic definition or physical hardware claim.
