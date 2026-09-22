# Design Invariants

1. **Base Fabric Immutability** — normal execution cannot mutate the base `.gcf` fabric image.
2. **Representation Is Not Ontology** — serialized chirality bytes are encodings of a 2×2×2 occupancy arrangement, not the arrangement itself.
3. **Backend Independence** — logical chirality/basin identity must not depend on one voltage, NAND type, CPU, or operating system.
4. **Explicit Physical Codec** — every hardware backend declares how logical states are encoded/read.
5. **Stable Addressing** — a Fabric Address resolves within one immutable fabric identity.
6. **Dynamic State Is Overlay State** — changes are append-only overlay records until explicitly checkpointed to a new derived fabric image.
7. **Checkpoint Creates New Identity** — materializing an overlay creates a new fabric artifact with new content hash; it never silently rewrites the parent.
8. **Scientific 3+1+1 Is Distinct From BRANE M5** — adapters are explicit.
9. **Adjacency Is Pluggable** — the implementation does not fabricate the source-open exact eight-site mote adjacency law.
10. **Receipts Are First Class** — read, transform, transport, close, and checkpoint operations can emit audit receipts.
