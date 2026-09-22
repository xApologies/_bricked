# Identity and forking

Every transformation creates a new `instance_id` because the live history has advanced.

The canonical MMO identity is preserved by default. A child therefore represents a new state/history of the same mapped molecular object rather than a new molecule by implication.

If a transformation intends to define a new representation identity, use `DERIVE_REPRESENTATION` and supply/derive a representation label.

If a transformation intends to define a new canonical MMO, use `DERIVE_MMO` and supply the new canonical MMO ID explicitly. Section 03 never invents molecular semantics from raw field edits.

The lineage relation is:

```text
child.parent_instance_id = parent.instance_id
child.history = parent.history + TRANSFORMATION_CLOSED
child.provenance = parent.provenance + transformation receipt
```
