# Reconstruction and source preservation

Original inputs: `C:\Users\rando\_bricked\_inbox\_chiralityFabric\ASSEMBLY.zip`, `Handoff.zip`, and `A.zip` through `U.zip`. All remain unchanged. A–U are binary transport parts of one checkpoint, not independent semantic modules.

1. Validate Handoff's 14 checksum entries and equality of its volume index with ASSEMBLY's index.
2. Match each local letter ZIP to the manifest filename by verified length and SHA-256. Copies under `_inbox/fabric-recovery/volumes/` use the exact manifest filenames; originals are not renamed.
3. Verify all 21 outer ZIP CRCs and embedded part manifests. Run the supplied `reassemble_r62.py` unchanged from that ignored directory; it verifies every inner part length/hash and the final checkpoint length/hash.
4. Validate the reconstructed ZIP CRC, extract all 102 entries, and validate 101 original checksum entries, all 56 physical-artifact hashes, all 36 embedded ZIP CRCs, both SQLite databases, R62 table counts and all six supplied R62 API smoke commands.
5. Keep the entire reconstruction locally. Commit the confirmed non-archive working scope, preserving bytes, original manifests and separate reservoirs. The supplied Handoff is a recovery checklist, not a Git policy; the user's explicit scope clarification governs Git selection.

All original-to-local paths and original-to-Git dispositions are in SOURCE_INVENTORY.json. Windows-forbidden characters in local archive names were replaced by hyphens only in staging and mapped reversibly. None of the committed R62 non-ZIP source paths needed normalization; only the common checkpoint wrapper was mounted at `R62/`.

The complete local extraction is `_inbox/fabric-recovery/reconstructed/`. The reassembled ZIP is in `_inbox/fabric-recovery/volumes/`. Historical source paths such as `/mnt/data` in preserved documents are provenance, not current host paths. Source archives, including four over 100 MiB, remain local by the user's selection; no LFS or pointers substitute for the committed working source files.

The original R62 checksum file covers 101 entries; its own hash is recorded by SOURCE_INVENTORY.json. Original manifests remain unedited and describe full-checkpoint scope. The integration inventory supplies the filtered Git view without rewriting historical evidence.

The retained original source PDFs and images preserve the source's distinct evidence/analogy classes. In particular the Density Ladder and world-model images do not become Fabric mathematics merely because their provenance is committed.

Reconstruction reports record actual local results. Original `QA_REPORT.json` files are historical evidence and are not rewritten. The integration audit and final operator receipt record current validation and push results.
