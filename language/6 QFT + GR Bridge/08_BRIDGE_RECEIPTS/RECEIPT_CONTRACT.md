# Bridge Closure Receipt

A successful Bridge receipt contains:

```text
bridge_id
source_sector
target_sector
source_instance_id
canonical_mmo_id
address
source_representation_view_id
target_representation_view_id
fabric_witness_id
source_content_root
target_content_root
source_residue_root
target_residue_root
preservation contract
R_QG witness
source segment hashes
base fabric hash
physics_status
lifecycle
```

`physics_status` is explicitly `SOFTWARE_REFERENCE_TRANSDUCTION` in v0.1.0.
