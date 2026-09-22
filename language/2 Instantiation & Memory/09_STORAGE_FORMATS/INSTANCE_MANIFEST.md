# Geometric Instance Manifest

An instance manifest is immutable after commit and names:

- canonical MMO identity;
- representation/source hashes;
- mapping profile;
- region binding;
- `.gos` segment hash;
- parent instance if any;
- verification policy/result;
- history/provenance receipts;
- BRANE M^5 descriptor hash.

A runtime status ledger may reference the manifest and say LIVE/QUIESCED/RELEASED, but it does not rewrite the manifest.
