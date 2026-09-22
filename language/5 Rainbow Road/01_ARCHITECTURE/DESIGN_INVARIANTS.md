# Section-05 Design Invariants

1. A Rainbow Road is an ordered composition of one or more Portal transactions.
2. Every Portal leg must independently close under Section-04 rules.
3. Consecutive leg addresses compose exactly: `target_i == source_(i+1)` at the declared domain/sector boundary.
4. Section-05 v0.1 roads are single-sector. Sector changes require an explicit bridge/transduction layer and are rejected here.
5. The Road preflights all leg Corridors before the first Portal opens.
6. The Rainbow Bus holds enough route capacity to guarantee the preflighted sequential leg set while the Road runs.
7. Bus capacity is scheduling capacity, not Bandwidth Algebra.
8. The source Geometric and base chirality fabric remain immutable for the entire Road.
9. Every intermediate Geometric is immutable once its Portal closes.
10. End-to-end canonical MMO identity is preserved unless a future explicit derivation/transduction contract says otherwise.
11. End-to-end representation identity is preserved when the preservation contract requires it.
12. Full-cell content identity is preserved for `RE_REALIZE` roads.
13. The complete ordered Portal/Corridor witness is retained in the Road receipt.
14. A Road's transport-holonomy signature is an implementation witness over the ordered route; it is not automatically a physical holonomy theorem.
15. Closed Portal history is never deleted on Road failure.
16. `FAILED_PARTIAL` is a valid terminal Road state and identifies the last closed waypoint.
17. Reusable Road templates are separate from Road executions.
18. The Road never claims that QFT and GR are identical representations.
