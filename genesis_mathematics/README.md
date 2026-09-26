# Genesis mathematical / structural language corpus

This independent source-authority tree preserves Genesis Manuscript v3.0, Mathematics-Only Edition, reconstructed from Companion-governed A–I raw byte segments. It is distinct from the [Genesis Programming Language](../language/README.md), [Chirality Fabric](../chirality_fabric/README.md) and [project architecture](../docs/architecture/UNIFIED_GENESIS_FRAMEWORK.md). It does not replace those authorities or the smaller spoken/structural-language source material.

## Read the source

1. [Original README](v3.0/README.md) and [cutoff note](v3.0/NOTES/WHERE_WE_CUT_OFF_AND_WHY.md).
2. [Primary manuscript](v3.0/BOOK/GENESIS_MANUSCRIPT_v3_0_MASTER.md).
3. [Dependency spine](v3.0/APPENDICES/MATHEMATICS_ONLY_DEPENDENCY_SPINE.md) and [inclusion/exclusion matrix](v3.0/APPENDICES/INCLUSION_EXCLUSION_MATRIX.json).
4. FORMAL/ contains chapters 39–56; FOUNDATION/ retains v0.3; MOVEMENTS/ retains the cognitive Rosetta and individual movements; LANGUAGE/ contains the propagation-language map; MACHINE/ holds the original database, manifest and checksums; PROVENANCE/ and RECOVERY/ retain source history and instructions.

The common archive wrapper is mounted at v3.0/. Every non-archive file is unchanged, without path renaming, deduplication or mathematical edits. All 68 files are present. The two historical SOURCES ZIPs remain local, as documented in the [recovery audit](../provenance/audits/GENESIS_MATHEMATICS_INTEGRATION.md) and [complete inventory](../provenance/sources/GENESIS_MATHEMATICS_RECEIPT.json). A clone contains the complete extracted manuscript working corpus, not those historical archives or the original transport parts. Original manifests still describe the full recovered archive, including local-only historical ZIPs.

The edition excludes downstream natural-law realization from its declared core. Historical passages remain in the cumulative master; they have not been edited away. Source variants and their scope limits are recorded in [conflicts and OPEN issues](provenance/VARIANTS_AND_OPEN.md). Successful recovery is not mathematical validation.

Run `python -B genesis_mathematics/tools/validate.py` from the repository root to verify the Git source files, Companion controls and SQLite structure. With the complete local extraction, pass `--local-root _inbox/manuscripts-recovery/extracted/GENESIS_MANUSCRIPT_v3_0_MATHEMATICS_ONLY_20260828` to check all original files, manifests and ZIPs.
