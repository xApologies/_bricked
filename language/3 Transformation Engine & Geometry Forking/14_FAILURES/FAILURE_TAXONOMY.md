# Section 03 failure taxonomy

- `TRANSFORM_STALE_PARENT` — expected parent state root does not match.
- `TRANSFORM_EFFECT_DENIED` — capability profile rejects requested effect.
- `TRANSFORM_SELECTOR_INVALID` — selector resolves outside or ambiguously within the Geometric.
- `TRANSFORM_IDENTITY_POLICY_INVALID` — semantic identity change is undeclared/underspecified.
- `TRANSFORM_INVARIANT_VIOLATION` — requested preservation contract fails.
- `TRANSFORM_DELTA_INTEGRITY` — `.gtd` header/payload/hash validation fails.
- `TRANSFORM_POST_ROOT_MISMATCH` — independently reconstructed child root differs from planned root.
- `TRANSFORM_PARENT_MUTATED` — a parent segment hash changed during transaction.
- `TRANSFORM_BASE_FABRIC_MUTATED` — `.gcf` base fabric hash changed.
- `TRANSFORM_ABORTED` — transaction failed before closure; no child is canonical.
