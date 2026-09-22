# Source recovery

Source: `C:\Users\rando\_bricked\_inbox\Genesis_lang.zip`.
SHA-256: `64208af9ea2edd5beec10599fb7e0997d11db4afa8e38e9b3f178bd9683c1f7b`.
Pre-recovery HEAD: `beccdcd107ef0f80cd369898a827b400a6e208b9`.

The complete recursive archive inventory contains 150,216 non-ZIP file occurrences and 2,036 nested ZIP occurrences. The inventory was scanned without errors. Archive-qualified paths use `!/` to enter a ZIP. The original ZIP remains unchanged in the ignored local inbox; it is not needed to use the recovered working source tree.

## Selection authority

Section 20 declares GENESIS 1.0.0 / FROZEN / CONFORMANT REFERENCE RELEASE. Its `01_RELEASE_FREEZE/SECTION_01_19_CORE_LOCK.json` authenticates the Part-A implementation packages. All 19 selected packages match those exact SHA-256 values. The Section 20 Part-A package supplies the freeze itself. Per-domain START_HERE and recovery records identify Part A as the working implementation and Parts B onward as fixtures, source capsules, and lineage. `_lang/GENESIS_LANGUAGE_SOURCESET_v0.1.zip` supplies the seven linguistic PDFs; all seven match its manifest.

The outer Section 12 package does not match the frozen lock. Its exact locked revision was recovered from Section 19 Part C. This is resolved by cryptographic release provenance, not by guessing from a filename. See CONFLICTS.md and SOURCE_PACKAGES.json.

Preserved: architecture, contracts, source, schemas, handwritten examples, tests, standard-library packages, required vendored dependencies, source crosswalks, and original release evidence. Excluded: archive wrappers/history, noncanonical duplicate revisions, reproducible reference builds/runs, and Python caches. No source-language terms or semantic contracts were edited. No file was removed merely for exceeding a size threshold; the 103 oversized dependency indexes belong to excluded historical API/source capsules, not the release-locked working cores.

## Evidence and scope

`SOURCE_PACKAGES.json` identifies all 21 selected packages and their SHA-256 values. `RECOVERED_FILES.json` maps each of the 1,740 recovered source files to its exact archive occurrence, length, and SHA-256. It excludes the newly authored recovery documents and test launcher. Every recovered file is byte-identical to its selected ZIP entry.

Import-required vendored files are retained even where bytes recur across domains: removing them would break the supplied standalone implementations or change release dependency binding. Reproducible copies under reference build/run directories are excluded; 64 are byte-identical to retained source files. Original manifests and test-result records remain evidence of the released packages, not claims that generated outputs are still present.

The full source inventory and intermediate inspection files remain local under `_inbox/`; they are audit aids, not substitute source registries. The committed `language/` tree itself is the working artifact. Existing project architecture, modules, provenance, and scenario canon are unchanged.
