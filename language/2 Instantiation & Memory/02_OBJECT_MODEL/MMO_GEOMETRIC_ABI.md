# MMO / Geometric ABI v0.1

## Canonical MMO

```text
MappedMolecularObject
  canonical_id
  version
  aliases[]
  dependency_closure[]
  provenance[]
  invariants[]
  representations{}
  closure_policy
```

## ScientificRepresentation

```text
representation_id
kind
shape
axis_labels
source_hashes
channel_registry
codec/units
validation_status
```

## GeometricInstance

```text
instance_id
canonical_mmo_id
representation_id
fabric_tag
region
layout_profile
segment_id
state
parent_instance_id?
history_chain[]
provenance_chain[]
brane_m5_descriptor?
```

### Identity rule

`MMO != Representation != GeometricInstance != FabricRegion`.

They are related by typed mappings and receipts.
