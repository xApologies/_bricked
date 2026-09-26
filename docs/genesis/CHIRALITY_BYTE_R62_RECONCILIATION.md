# Chirality / Binary / Byte Reconciliation

Binary occupancy support: o:D->{0,1}.
Occupied loci may carry C={R,O,Y,G,B,V}.
Occupancy, chromatic state, adjacency, orientation and History remain distinct.

Example support 0 1 1 0 1 0 0 1 may carry 0 G G 0 R 0 0 Y.
Same binary occupancy != same Chirality state.
Design maxim: do not replace the bit; lift binary support into geometry.

R62 hierarchy remains Tile -> Seed(2x2) -> Byte/Bite(2x2x2 set-lift)
-> Block(4x4x4) -> recursive Fabric. Exact Seed->Byte lift OPEN.

Cube realization gives six 2x2 face restrictions plus adjacency/orientation/path
structure. DP-004's "six faces are Seeds" must be reconciled against R62 rather than
silently promoted. Exact face status and color/readout composition OPEN.

White = proposed combined/superposed spectral expression; exact algebra OPEN.
Black deferred.

Conventional files may be State Geometrics with G_file <-> b in {0,1}*.
Round-trip identity contract remains to be formalized.

Status: WORKING reconciliation; unresolved source mathematics remains OPEN.

The [R62 source](../../chirality_fabric/R62/01_CANON/CANONICAL_STATE_R62.md) remains unchanged. DP-004's cube-face geometry is retained as a working restriction; identifying every face with a canonical Seed is explicitly OPEN. Shared-vertex incidence does not prove the Seed set-lift or propagation law. The R62 truncated-average weights are a toy readout, not a physical color law. This is a new superseding qualification of the current [Byte](CHIRALITY_BYTE.md), [Seed](CHIRALITY_SEED.md) and [color](CHIRALITY_COLOR_ORGANIZATION.md) prose, not a rewrite of DP-004 history.

## Provenance

DP-006 accepted live-model delta on the working branch; see the [integration decision](../../provenance/decisions/0007-dp006-cumulative-genesis-architecture.md), [source receipt](../../provenance/sources/DP006_RECEIPT.json) and [OPEN ledger](../architecture/OPEN_MATHEMATICS.md). This does not merge or replace accepted main.
