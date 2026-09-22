# Static proof obligations

Section 09 emits auditable witnesses for checks it actually performs:

- `PO-SYMBOL-RESOLUTION` — all imports/exports resolved uniquely;
- `PO-TYPE-SAFETY` — operation arguments and result declarations are compatible;
- `PO-EFFECT-BOUNDS` — actual module effects are within declared budgets;
- `PO-LINEAR-OWNERSHIP` — quantum linear resources are not consumed twice or generically cloned;
- `PO-CLOSURE` — no Portal/Road remains OPEN at linked-program boundary;
- `PO-SECTOR-TRANSDUCTION` — sector change has a matching Bridge witness;
- `PO-CAPABILITY` — target advertises required ops/effects/sectors/features;
- `PO-PROVENANCE` — linked graph contains module/source map and link receipt.

These are **static machine proofs relative to the implemented rules**. They are not broad claims that arbitrary program correctness or physical behavior has been formally proved.
