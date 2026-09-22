# Section-06 Design Invariants

1. QFT and GR are representation sectors, not aliases.
2. `Bridge<QFT,GR>` and `Bridge<GR,QFT>` are explicit transactions.
3. A Portal remains single-sector; it cannot silently change sector.
4. A Bridge is representation transduction at one realized Geometric/address, not information transportation by itself.
5. The underlying Geometric segment chain remains immutable during a Bridge.
6. The base chirality fabric remains immutable.
7. No global inverse map from QFT to fabric or GR to fabric is assumed.
8. Common ancestry is represented by an explicit `FabricWitness`.
9. The canonical MMO identity, content root, residue root, and selected provenance survive Bridge transduction by default.
10. QFT/GR sector descriptors are software representation contracts, not claims of new physical derivation.
11. A mixed-sector Rainbow Road inserts Bridge actions exactly where sector changes occur.
12. Every Portal action on a mixed Road still passes Section-04 Corridor admission.
13. Mixed-road preflight includes every Portal Corridor and every Bridge compatibility check before execution.
14. Closed Portal and Bridge history is append-only.
15. If a later action fails, the mixed Road resolves `FAILED_PARTIAL` and retains the exact completion frontier.
16. BRANE M^5 re-lift records current sector plus bridge ancestry; BRANE realization Z remains BRANE-owned.
17. Source bridge statements marked open typing remain open typing in this implementation.
