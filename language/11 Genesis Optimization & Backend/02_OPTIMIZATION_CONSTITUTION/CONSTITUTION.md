# Optimization constitution v0.1

Section 11 treats optimization as a semantics-preserving graph rewrite under explicit proof obligations. Performance is subordinate to identity, history, closure, admissibility, sector, quantum-resource, and provenance semantics.

The initial optimizer therefore targets only transformations with local, mechanically checkable equivalence:

- canonical graph normalization;
- duplicate-edge elimination;
- typed constant-folding analysis (rewrite deferred until GIR has typed hash literals);
- explicit alias-only `MOVE` coalescing;
- dead **pure** node elimination;
- compact GVM source-metadata stripping after semantic compilation.

No Portal fusion, Road fusion, bridge elimination, measurement motion, effect reordering, provenance pruning, or speculative transform fusion is admitted in v0.1.
