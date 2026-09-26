# Genesis mathematical-language integration audit

Date: 2026-09-26. Starting HEAD: `b5922796fadd35f11e58fdfbfd6c3c1cb4bda913`.
Branch: bootstrap/canonical-architecture. Repository origin verified as xApologies/_bricked; clean and synchronized before recovery.

## Recovery procedure and evidence

Immutable inbox: `C:\Users\rando\_bricked\_inbox\_genesisManuscripts`.
Actual Companion filename: `Companion .zip` (space before extension). Its three members are MANIFEST.json, README_REASSEMBLY.md and REASSEMBLE.py; all were read before manipulating parts and are preserved byte-for-byte in the [Companion directory](../../genesis_mathematics/provenance/Companion/README_REASSEMBLY.md).

The [pre-reconstruction source receipt](../../genesis_mathematics/provenance/SOURCE_RECEIPT.json) records all ten artifact names, sizes, signatures, hashes, roles and order, including Companion. A.part–I.part map by Companion labels and verified hashes to GENESIS_v3_0_A.part–GENESIS_v3_0_I.part. Only temporary copies were given those names; originals were not renamed. Nine raw byte segments total 885,094,360 bytes. The unchanged Companion script concatenated these copies in A–I order in `_inbox/manuscripts-recovery`, outside the immutable source inbox. No additional manuscript build is prescribed: the reconstructed ZIP contains the built manuscript and database.

Reconstructed filename: `GENESIS_MANUSCRIPT_v3_0_MATHEMATICS_ONLY_20260828.zip`.
SHA-256: `8b9a92ac56ab71ece3880e47ef6f8d47bc6a69beaab7e67994ed87b36f330209`.
Exact size: 885,094,360 bytes. All source-part hashes, final hash/size and archive CRC passed. Complete extraction: 70 files, 887,487,566 bytes. The common archive wrapper is mounted at `genesis_mathematics/v3.0/`; internal names/hierarchy and every included byte remain unchanged.

## Git inclusion and exclusions

Git contains all 68 non-archive files, 3,168,206 source bytes. BOOK is the primary manuscript; FOUNDATION is the retained v0.3 source; FORMAL holds 18 chapters; MOVEMENTS, LANGUAGE, APPENDICES, MACHINE, NOTES, PROVENANCE, RECOVERY and original README are retained. Duplicate named movements and aggregate manuscripts are not silently discarded. Largest included source: BOOK/GENESIS_MANUSCRIPT_v3_0_MASTER.md, 835,199 bytes. No included file approaches 50 MiB or exceeds 100 MiB.

Two explicitly historical source/work-layer ZIPs remain local:

| Source path | Bytes | Reason |
| --- | ---: | --- |
| SOURCES/GENESIS_THE_TOME_v0_3_GENESIS_MANUSCRIPT_UPDATE_20260828.zip | 260184342 | Prior full source archive; extracted foundation already retained in the supplied edition. |
| SOURCES/GENESIS_THE_TOME_v0_4_CHIRALITY_EXHAUSTIVE_INTEGRATION_20260828.zip | 624135018 | README explicitly classifies this as consulted source/work-layer evidence, not canonical mathematics-only manuscript. |

Both archives passed CRC and supplied hashes and remain in the complete local extraction. Their internal inventories were inspected; they include further historical/physical source archives. They were not recursively promoted into the mathematics-only source tree. Original MACHINE manifests remain unchanged and therefore reference local-only artifacts. The [integration inventory](../sources/GENESIS_MATHEMATICS_RECEIPT.json) distinguishes every Git/local disposition.

Also excluded from Git: original A.part–I.part and staging copies (transport), Companion ZIP container (three contents preserved), assembled ZIP (redundant recovery container), temporary extraction/scripts/log copies (work area). Source receipts and the actual assembly output are committed. No LFS or substitute pointer was introduced.

## Checks

- Nine source-part sizes/SHA-256 values: PASS; all ten original inbox artifact hashes rechecked after recovery: unchanged.
- Companion, reconstructed ZIP and both historical source ZIPs: CRC PASS.
- All 68 internal manifest entries and 68 checksum entries: PASS; integration inventory also covers the two manifest/checksum files themselves (70 total files).
- Manuscript validator with complete local extraction: PASS, 68 Git source hashes, three control hashes, all 70 extracted hashes, both local archive CRCs and original manifests.
- SQLite read-only integrity: ok; metadata 7, chapters 18, inclusion 12, frontiers 3, source_receipts 6; every chapter path resolves.
- Repository validator: all nine checks PASS, including the 87-file authenticated constitution and 171-scenario module canon.
- Preserved Fabric validator: PASS, 66 sources, 20 controls, two SQLite databases and 12 API checks.
- New documentation links: checked; source text and source-internal historical references remain unmodified.
- Final staged checks: additions only; original tracked blobs unchanged; no transport/temp archives or files over 100 MiB; source/control blobs match recorded bytes; whitespace check respects original source formatting.

## Authority and limitations

[Variants and OPEN issues](../../genesis_mathematics/provenance/VARIANTS_AND_OPEN.md) records inherited version headings, the mathematics-only editorial cutoff versus inherited physical references, Seed/White/connection scope differences and duplicate movement names. These remain source evidence, not edits to project mathematics. Environment-to-Bandwidth-generator mapping and SU(2)/SU(3) closure remain OPEN. No mathematical correctness claim follows from integrity checks. Existing language/, chirality_fabric/, DP-004, DP-006, State/Nexus/Shell/Sea, Road, Guardian and all prior provenance are unchanged.

## Commit identification

The final integration SHA is the commit that adds `provenance/sources/GENESIS_MATHEMATICS_RECEIPT.json`: recover it with `git log --diff-filter=A --format=%H -- provenance/sources/GENESIS_MATHEMATICS_RECEIPT.json`. A commit cannot contain its own eventual SHA without self-reference. The exact SHA and verified push result are recorded after execution in the completion report and local `_inbox/manuscripts-recovery/COMPLETION_RECEIPT.json`. No merge to main is performed.
