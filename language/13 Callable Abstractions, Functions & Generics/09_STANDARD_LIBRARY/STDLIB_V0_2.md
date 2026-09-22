# Callable standard library v0.2

Section 13 upgrades selected Section 12 contract packages into executable callable libraries while preserving the v0.1 packages in the registry.

Added v0.2 packages/functions include:

- `genesis.std.core.callables::fork_geometric<G:GEOMETRIC>`
- `genesis.std.portal.callables::gr_transfer<G:GEOMETRIC>`
- `genesis.std.portal.callables::qft_transfer<G:GEOMETRIC>`
- `genesis.std.portal.callables::gr_transfer_then_seal<G:GEOMETRIC>`
- `genesis.std.bridge.callables::gr_to_qft<G:GEOMETRIC>`
- `genesis.std.bridge.callables::qft_to_gr<G:GEOMETRIC>`
- `genesis.std.bridge.callables::qft_to_gr_transfer<G:GEOMETRIC>`
- `genesis.std.quantum.callables::prepare_superpose_measure<G:GEOMETRIC>`
- `genesis.std.quantum.callables::prepare_channel_measure<G:GEOMETRIC>`
- `genesis.std.provenance.callables::seal_resource<T:RESOURCE>`
- `genesis.std.provenance.callables::require_closure<T:RESOURCE>`
- `genesis.std.brane.callables::lift_geometric<G:GEOMETRIC>`
- `genesis.std.road.callables::close_single_receipt_road<G:GEOMETRIC,R:RECEIPT>`

`genesis.std.fabric` and `genesis.std.atomic` are carried to v0.2 as executable fixture/data packages so a coherent v0.2 dependency stack can be built.

The library functions are intentionally small. They are executable conformance fixtures for the callable ABI, not a claim that the final Genesis standard library API has been frozen.
