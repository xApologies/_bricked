# Conflicts and source decisions

## Resolved: Section 12 outer package differs from frozen release

The outer `Genesis/12 Genesis Library/GENESIS_CHIRALITY_MACHINE_SECTION_12_STDLIB_PACKAGE_RUNTIME_v0.1.0_20260821_PART_A_CORE.zip` has a different digest and source layout from Section 20's frozen core lock. Selected instead:

`Genesis/19 Genesis Bootstrap & Self-Hosting Path/GENESIS_CHIRALITY_MACHINE_SECTION_19_BOOTSTRAP_SELF_HOSTING_v0.1.0_20260821_PART_C_IMPLEMENTATION_LINEAGE.zip!/_section19_part_c/GENESIS_CHIRALITY_MACHINE_SECTION_12_STDLIB_PACKAGE_RUNTIME_v0.1.0_20260821_PART_A_CORE.zip`

SHA-256: `44092476eec432ed797f836d96445f3d4d768841c918aff5b42eccf17342eeeb`; exact match to Section 20's authoritative Section 12 lock. The outer alternative is excluded, not merged. Both candidate occurrences remain recoverable from the unchanged original source archive.

## Unresolved recovery conflicts

None. No competing source contents were silently merged and no semantic choice was made to resolve a source ambiguity.

## Inherited semantic gate requiring future human review

`S0_STRUCTURAL_ZERO_VS_EXISTENCE_CONFLICT` is explicitly unresolved in `20 GENESIS/01_RELEASE_FREEZE/GENESIS_V1_0_RELEASE_DESCRIPTOR.json`. It remains unchanged. This is an existing language-design gate, not a recovery-selection conflict. The release's tests explicitly prohibit silently reconciling it.
