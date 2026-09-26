# Chirality Fabric R62 integration audit

Date: 2026-09-26.
Parent HEAD: `dd4c4ad0355f84607d05937b19f22debe10db27b`.
Branch: bootstrap/canonical-architecture.
Baseline: clean; fetched remote matched parent.
Operation: independent of completed DP-004.

## Assembly and complete local recovery

Source directory: `C:\Users\rando\_bricked\_inbox\_chiralityFabric`.
ASSEMBLY/Handoff were inspected first. Handoff's 14 checksums passed and its split-volume index equals ASSEMBLY's. All 21 local letter-named transport ZIPs matched declared lengths and SHA-256 values. Each outer CRC and embedded part manifest passed. Verified copies received the exact manifest filenames in ignored staging; source inputs were unchanged.

The supplied reassembler ran unchanged, verifying every inner part and reconstructing the exact 1,838,368,113-byte ZIP with SHA-256 `f0c63cabf18ad856f10dc2ffd57669ae02106a561d2c9af06a5ecf83bf79d65e`. The complete checkpoint CRC passed. All 102 entries were extracted into ignored staging; Windows-forbidden characters were normalized only in local archive filenames with a reversible mapping. No committed R62 source path required that normalization.

Complete-reconstruction checks passed: 101 original checksums; all 56 physical source-artifact lengths/hashes; all 36 embedded ZIP CRCs; both SQLite integrity checks; exact R62 table counts; all six original R62 smoke commands. The checksum file's own hash is captured separately in the integration inventory. The source builder's QA routine was inspected, not used to regenerate or rewrite source history.

## Git scope

The user explicitly selected the working tree plus complete provenance with archives local. Git contains all 66 non-ZIP R62 entries (80,744,568 bytes), unchanged, including original canon/mathematics/history, formal source stack, two SQLite QMO databases/APIs and typed source/context evidence. The common package wrapper is mounted under `chirality_fabric/R62/`.

Twenty ASSEMBLY/Handoff control files are preserved unchanged. Original manifests, hashes and aliases remain evidence of full-checkpoint scope; a new [source inventory](../../chirality_fabric/provenance/SOURCE_INVENTORY.json) records every included/local-only artifact and its original/local path, byte count and SHA-256. The [assembly receipt](../../chirality_fabric/provenance/ASSEMBLY_RECEIPT.txt), [transport receipt](../../chirality_fabric/provenance/TRANSPORT_RECEIPT.json) and [reconstruction results](../../chirality_fabric/provenance/RECONSTRUCTION_VALIDATION.json) preserve the actual recovery trail.

All 36 embedded ZIPs remain local, including four larger than 100 MiB. No transport ZIP, reconstructed ZIP, LFS change or archive pointer is committed. The working source itself is present. Largest retained source is MK Ultra.pdf at 67,402,112 bytes, below the ordinary Git per-file limit.

## Reconciliation and preservation

See the [independent decision](../decisions/0006-chirality-fabric-r62-source-ingest.md). R62 toy averaging is not silently promoted into DP-004 color mathematics. Source reservoirs, candidates, open laws and historical claims remain typed and separate. Prior DP-004 documents, decisions, audit, receipt, checkpoint and validator remain untouched. All existing tracked files except the additive CHANGELOG entry are preserved, including the language tree, 00–14 constitution, scenario/module canon and DP-001–DP-003.

## Validation and review

Commands:

```text
python -B chirality_fabric/tools/validate.py --local-root _inbox/fabric-recovery/reconstructed
node tools/validators/validate-bootstrap.mjs
python -X utf8 _inbox/fabric-recovery/audit.py
git diff --cached --check
```

Integrated Fabric validation passed: 66 source hashes, 20 control hashes, both SQLite databases and recorded counts, 12 R62/R61 API smoke commands, all 102 local source hashes and 36 local archive CRCs. Source bytes remain unchanged after querying. The repository validator passed all nine checks. The final audit checks the intended file set, Git size compatibility, preserved baseline paths and staged source bytes; staged review excludes all ZIPs and unrelated changes. Commit/push results are reported after execution, not pre-claimed here.

Three negative validator checks passed: a modified source, a modified control file and an unexpected source file were each rejected. Git attributes preserve source bytes and permit original source trailing spaces/terminal blank lines and CRLF endings; authoritative files were not reformatted.
