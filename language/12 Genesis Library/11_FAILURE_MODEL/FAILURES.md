# Failure model

Representative Section 12 failures:

- `MANIFEST_INVALID`
- `VERSION_INVALID`
- `DEPENDENCY_MISSING`
- `DEPENDENCY_CONFLICT`
- `DEPENDENCY_CYCLE`
- `LOCK_DRIFT`
- `PACKAGE_HASH_MISMATCH`
- `MODULE_DUPLICATE`
- `MODULE_UNRESOLVED`
- `DIRECT_DEPENDENCY_REQUIRED`
- `EFFECT_BUDGET_EXCEEDED`
- `SOURCE_MISSING`
- `GENESIS_VERSION_UNSUPPORTED`

These failures occur before or around compilation. Section 09–11 errors are preserved rather than translated into misleading package-manager success states.
