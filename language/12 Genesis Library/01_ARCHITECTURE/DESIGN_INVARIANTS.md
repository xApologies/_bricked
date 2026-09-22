# Design invariants

1. **Package identity is content-addressed.** Name/version are coordinates; the SHA-256 content root is the immutable package identity witness.
2. **Resolution is deterministic.** Given the same registry state, root manifest and resolver version, the lockfile is byte-for-byte reproducible.
3. **A lockfile freezes identities, not merely names.** Frozen mode checks name, version and content hash.
4. **No transitive-import leakage.** A package may import its own modules or modules from a direct declared dependency only.
5. **Manifest effect budgets are upper bounds.** Source modules may not silently exercise effects absent from their package manifest.
6. **Package capabilities do not grant execution authority.** They are requirements/compatibility declarations; Section 09/backend checks remain final.
7. **Dependency order is dependency-first and acyclic.** Cycles are rejected at the package boundary.
8. **The package manager never rewrites source semantics.** It selects, validates and supplies source modules to the compiler.
9. **Standard-library status is explicit.** Contract-only packages are not misrepresented as executable libraries.
10. **Source Genesis and Computational Genesis remain distinct corpora.** Section 12 packages Computational Genesis artifacts only.
