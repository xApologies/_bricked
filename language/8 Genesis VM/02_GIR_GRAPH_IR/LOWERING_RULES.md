# GIR -> GVM lowering

1. Validate GIR schema and node uniqueness.
2. Infer data dependencies from `%value` arguments.
3. Merge explicit dependency/effect-order edges.
4. Reject illegal graph cycles.
5. Topologically schedule nodes deterministically.
6. Allocate typed virtual registers to GIR outputs.
7. Lower each GIR operation to one GVM instruction in v0.1.
8. Preserve node IDs and source-map metadata.
9. Run the GVM verifier.
10. Encode deterministic bytecode and emit a content hash.

Future optimization passes may fuse or split nodes, but they must preserve declared identity, effect, closure, ownership, and provenance obligations.
