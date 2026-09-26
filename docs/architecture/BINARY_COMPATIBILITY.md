# Binary Compatibility

Status: ACCEPTED WORKING direction; round-trip identity contract OPEN.

Genesis is a native state-space substrate. Conventional binary computing is supported through State-level projection/serialization. A conventional file may be represented as a State Geometric with `G_file <-> b in {0,1}*`; identity preservation through that round trip remains to be formalized.

Binary occupancy `o:D->{0,1}` is distinct from chromatic state, adjacency, orientation and History. The same occupancy pattern can support different Chirality states. See the [R62 reconciliation](../genesis/CHIRALITY_BYTE_R62_RECONCILIATION.md).

The [Horizon boundary](GENESIS_HORIZON.md) still requires decode, validation and admission for inbound bytes, and permitted exposure/serialization for outbound state. CPU, RAM, registers, opcodes, stack frames, LOAD/STORE, binary addresses, operating-system concepts and host scheduling are reference/lowering/transduction mechanisms; they do not automatically become native ontology. Supporting binary projection introduces no direct host write to State.

Source: DP-006 02/04/06; [decision](../../provenance/decisions/0007-dp006-cumulative-genesis-architecture.md). Exact projection/identity mathematics stays [OPEN](OPEN_MATHEMATICS.md).
