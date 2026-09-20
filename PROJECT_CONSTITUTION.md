# Project Constitution

1. GitHub `main` is canonical accepted project state. Working branches propose changes.
2. Preserve existing repository content unless a task explicitly replaces it.
3. Specifications and runtime implementation remain separate.
4. The 00–14 Development Constitution is invariant. Every playable scenario uses every stage.
5. Mark an irrelevant section **NOT USED** with a rationale; never delete it.
6. Shared concepts have one canonical specification. Levels instantiate shared systems rather than redefine them.
7. Every level instantiates the normalized 11D architecture, referencing [its canonical specification](docs/genesis/11D_ARCHITECTURE.md). Missing definitions remain OPEN.
8. Recursion requires seed, inheritance, update, invariants, guard, termination, history, and brick behavior. Underspecified behavior remains OPEN.
9. Genesis semantics remain upstream of Python, platform adapters, and rendering.
10. Gameplay-significant visuals correspond to authoritative computational state.
11. OPEN mathematics and design remain explicitly OPEN. Do not invent missing Genesis rules.
12. A level is not Gold until all stages 00–14 pass. An empty directory or unresolved required specification is not evidence of passing.
13. Every architectural change requires provenance: source, rationale, affected boundaries, and unresolved questions.
14. ZIP checkpoints are recovery artifacts; they do not supersede accepted GitHub `main`.
15. This bootstrap establishes structure and documentation only. Do not implement the actual game runtime.

## Invariant stage sequence

- `00_RELEASE`
- `01_DESIGN`
- `02_CYBERSECURITY`
- `03_GENESIS_MODEL`
- `04_STATE_MODEL`
- `05_ALGORITHMS`
- `06_PSEUDOCODE`
- `07_VISUALIZATION`
- `08_INTERACTION`
- `09_FLAGS_AND_KEYS`
- `10_TESTING`
- `11_DIAGRAMS`
- `12_MACHINE_READABLE`
- `13_IMPLEMENTATION_HANDOFF`
- `14_PROVENANCE`

The canonical template location is `development/constitution/LEVEL_XX/`. Its full expanded subtree and templates must be preserved from the supplied `dev.zip`, without simplification or consolidation. The complete supplied subtree is imported unchanged; its 87 source file hashes and source archive hash are recorded in `provenance/sources/dev-import.json`.

The [module canon](development/modules/README.md) records 171 playable scenarios. Shared Genesis specifications reside in [docs/genesis/](docs/genesis/README.md).
