# Design Invariants

1. Base chirality fabric is immutable.
2. A source Geometric and every source segment are immutable during Portal execution.
3. A Portal has a declared source address, target address, payload identity, preservation contract, and closure target.
4. A Corridor is selected only from edges whose local contracts admit the payload and request.
5. The route witness is never collapsed out of provenance.
6. Minimum route Resolution and Bandwidth must satisfy request thresholds.
7. Capacity must be reserved before Portal OPEN.
8. Destination re-realization receives a new instance ID and a distinct fabric region.
9. Canonical MMO identity is preserved unless a future explicit transduction/derivation contract says otherwise.
10. Transported content root must match the source content root for lossless RE_REALIZE transport.
11. Address-dependent state roots are allowed to differ because absolute physical addresses differ.
12. Invariant residue is declared field-by-field and independently checked.
13. QFT and GR are sectors, not aliases. Cross-sector traversal requires an explicit bridge/transduction capability.
14. Failure produces a receipt and releases uncommitted reservations.
15. A successful Portal closes only after destination readback and target-address verification.
