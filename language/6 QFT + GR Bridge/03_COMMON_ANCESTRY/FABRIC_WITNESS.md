# Common Fabric Witness

The Section-06 software ancestry witness is a deterministic hash over:

```text
canonical MMO identity
Geometric instance identity
fabric tag
fabric region
full-cell content root
selected invariant-residue root
source representation identity
```

For cross-sector correspondence, QFT and GR views need not have the same `representation_view_id`; they must bind to the same `fabric_witness_id` (or a future explicitly declared admissible-equivalence witness).

The witness proves only **software lineage and readout ancestry**. It is not itself a proof of physical QFT/GR unification.
