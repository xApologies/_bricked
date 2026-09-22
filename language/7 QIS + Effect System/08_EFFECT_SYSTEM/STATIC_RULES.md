# Static rules

1. `SUPERPOSE` requires QFT quantum semantics and creates a coherent PURE state.
2. `ENTANGLE` consumes/moves component ownership into one JOINT state.
3. `UNITARY` preserves norm and does not classicalize.
4. `DEPHASE` returns a density state and may reduce coherence.
5. `MEASURE` consumes a live coherent handle and emits a classical outcome plus measured successor.
6. `QFT_PORTAL_TRANSPORT` requires a QFT Portal and a declared channel.
7. `STRUCTURAL_TRANSDUCE` may change QFT/GR representation but does not imply preservation of quantum coherence.
8. A GR-only Portal cannot accept a live coherent quantum handle unless a future explicit channel/bridge type is registered.
