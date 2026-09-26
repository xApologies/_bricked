# Chirality Fabric — recovered R62 working tree

This source integration is independent of DP-004. The complete R62 checkpoint was reconstructed from all 21 verified A–U transport volumes using the supplied ASSEMBLY script unchanged. Its exact SHA-256 is `f0c63cabf18ad856f10dc2ffd57669ae02106a561d2c9af06a5ecf83bf79d65e` (1,838,368,113 bytes).

The user selected **working R62 tree plus complete provenance; archives stay local**. Git therefore contains all 66 non-ZIP R62 files, byte-for-byte, plus assembly/handoff controls and integration receipts. The 36 embedded source/checkpoint ZIPs, original A–U transports and assembled ZIP remain in the ignored local source library. A clone supplies the working documents, two QMO databases and APIs, formal stack, historical expanded evidence and typed context; it does not supply those 36 archives.

## Navigation

- [Start here](R62/00_START_HERE/README_FIRST.md), [source scope](R62/00_START_HERE/SCOPE_AND_COMPLETENESS.md)
- [R62 state](R62/01_CANON/CANONICAL_STATE_R62.md), [authority/firewalls](R62/01_CANON/AUTHORITY_AND_FIREWALLS.md)
- [Supersession history](R62/02_THREAD_HISTORY/SUPERSESSION_HISTORY.md)
- [Equation ledger](R62/03_MATHEMATICS/FULL_EQUATION_LEDGER.md), [native update frontier](R62/03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md)
- [Original artifact inventory](R62/06_MANIFEST/FILE_INVENTORY.csv)
- [Git/local source inventory](provenance/SOURCE_INVENTORY.json), [reconstruction validation](provenance/RECONSTRUCTION_VALIDATION.json)
- [Local source recovery and limitations](provenance/RECOVERY.md)
- [Independent integration decision](../provenance/decisions/0006-chirality-fabric-r62-source-ingest.md)

## Query and validate

From the repository root, using Python 3.12:

```text
python -B chirality_fabric/R62/05_MACHINE/qmo_api.py info
python -B chirality_fabric/R62/05_MACHINE/qmo_api.py resume
python -B chirality_fabric/R62/05_MACHINE/qmo_api.py address @open/native_multiscale_update_law
python -B chirality_fabric/tools/validate.py
node tools/validators/validate-bootstrap.mjs
```

The validator checks every committed source/control hash, both SQLite databases and original R62 QA counts, and the supplied API smoke surfaces. With the local extraction available, also use `--local-root _inbox/fabric-recovery/reconstructed` to check all 102 original files and all 36 embedded ZIPs.

## Authority boundary

Genesis Chirality v9, Propagation Girl v8, CRD→QCD v1.9, unified API/QMO and the books remain independent reservoirs. Source recovery does not reconcile or supersede them. R62's `01_CANON` is canon within that source checkpoint, not an automatic replacement of the repository's project authorities.

R62's truncated color average and weights 1–6 are explicitly a **toy readout**, not a canonical physical color law. Its seed-to-byte set-lift remains OPEN. Neither is silently substituted for DP-004's working cube/shared-face organization or unresolved color composition. DP-004 records and the complete `language/` tree are unchanged. Fusion remains CANDIDATE; QCD/SU(3) remain downstream comparisons. ZIP integrity validation is not a substantive inspection of every nested propagation-model claim.

The native multiscale update law, coupling, path selection, Bandwidth, simultaneous updates, canonical noncommutativity, readout composition and energy-density/color map remain unresolved. No mathematical law is implemented in this ingest.

Original manifests, QMO artifact flags and source links describe the complete source checkpoint. They may refer to intentionally local archives or inherited historical paths; consult SOURCE_INVENTORY.json for actual Git presence. Do not run the preserved historical `build_full_checkpoint_r62.py` as a modern project build: it recreates a historical host-specific checkpoint and is kept as provenance only.
