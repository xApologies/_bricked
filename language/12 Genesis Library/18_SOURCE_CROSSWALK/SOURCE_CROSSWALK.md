# Source crosswalk

Section 12 is a **new compiler/runtime engineering layer** over the previously established machine stack.

Inherited implementation authority:

- Section 08: GIR/GVM execution model.
- Section 09: static types/effects, module linker, proof obligations, backend capability gate.
- Section 10: Genesis `.gen` parser/lowering/frontend.
- Section 11: proof-preserving optimization and backend code generation.

Inherited conceptual constraints:

- packages must not erase Portal/Road closure history,
- package composition cannot erase QFT/GR bridge boundaries,
- quantum linear ownership remains a compiler semantic rather than a package-manager convention,
- provenance/history remains first-class,
- API/package technology is not promoted into ontology.

New Section 12 engineering decisions:

- `genesis.pkg.json` manifest format,
- local registry layout,
- semantic-version subset,
- deterministic dependency solver,
- content-addressed store,
- lockfile format,
- direct-dependency import discipline,
- package effect-budget audit,
- initial stdlib package boundaries.

These are implementation architecture choices, not claims that the historical Source Genesis corpus specified a software package manager.
