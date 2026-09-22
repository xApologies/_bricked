# Invariant Residue Contract

Transport can preserve a selected subset of cell organization rather than relying on byte identity alone.

Supported residue fields in Section 04:

```text
occupancy_pattern
complement_pattern
handedness
state_class
sigma
chi
rho
lambda_
tau
flags
adjacency_index
lineage_index
identity_tag
```

A residue root is the SHA-256 digest of the selected fields over the Geometric's ordered logical cells. The logical cell ordinal, not the absolute fabric index, enters the digest; therefore a lossless relocation can preserve residue while changing physical address.

`content_root` is the residue root over the complete packed ChiralityCell and is the default lossless transport invariant.
