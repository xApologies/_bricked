# Capability profiles

## GENERIC_LIVE
Allows mapped state-field changes but rejects `IDENTITY_TAG_WRITE` by default.

## PIPELINE_T
Formation-domain profile. Allows chirality and occupancy writes in addition to persistence/admissibility/locality/translation state.

## PIPELINE_R
Environmental/exposure profile. Chirality and occupancy are read-only. This makes the recovered Pipeline-2 distinction executable instead of documentary.

## PROJECTION_ONLY
Read-only. Used when producing downstream projections without changing the parent Geometric.

## ADMIN_DERIVATION
Explicitly privileged profile for controlled identity-tag/structural migrations. Not used by ordinary transformation programs.
