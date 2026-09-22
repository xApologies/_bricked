# Design Invariants

1. Canonical MMO identity, representation identity, instance identity, and fabric-binding identity are distinct.
2. The base `.gcf` image is immutable.
3. A committed `.gos` segment is immutable.
4. Any state change produces a child delta/segment with ancestry.
5. A Geometric cannot be LIVE until its source hashes, plan, region, segment hash, and readback checks pass.
6. Region allocation is non-overlapping for writable instances.
7. Read-only shared instances may share a committed segment only when the shared-representation contract is explicit.
8. Scientific 3+1+1 axes are not renamed as BRANE I/D/Chi/R/P.
9. The 2x2 scientific chirality plane is not silently identified with a 2x2x2 chirality cell.
10. Unknown scientific fields remain unknown; the adapter does not invent mass, persistence, admissibility, locality, or resolution data.
11. Explicit adapter defaults are marked in receipts.
12. A fabric execution projection is not the entire molecular object.
13. BRANE owns Z realization.
14. Object history is append-only.
15. Instantiation failures leave no committed region or LIVE instance.
