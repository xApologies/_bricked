# Geometric Address

Human-readable object-local URI:

`geom://<mmo>/<instance>/<role>/<x>/<y>/<z>`

It resolves through the instance binding manifest to a `FabricAddress128`.

The URI is stable for the lifetime of an instance. Moving or checkpointing an instance creates a new binding identity and explicit relocation lineage rather than silently changing the old address.
