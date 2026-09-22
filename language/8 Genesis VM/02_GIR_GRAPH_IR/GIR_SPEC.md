# GIR 0.1 — Genesis Graph Intermediate Representation

A GIR program is a typed directed graph of semantic operations.

## Core shape

```json
{
  "ir": "GIR",
  "version": "0.1.0",
  "name": "first_portal",
  "nodes": [
    {
      "id": "mount",
      "op": "FABRIC_MOUNT",
      "out": "%fabric",
      "type": "FABRIC",
      "args": [],
      "attrs": {"uri": "fabric://reference"}
    }
  ],
  "edges": [],
  "exports": ["%receipt"]
}
```

## Dependency semantics

Dependencies are obtained from both:

- explicit `edges` of kind `dependency` or `effect_order`;
- data references in node `args` beginning with `%`.

The compiler constructs one partial order, checks it for illegal cycles, and emits a deterministic topological schedule. Ties are resolved by node ID so compilation is reproducible.

## Why SSA-like values

A named GIR value is assigned once. Identity-bearing runtime objects can have many successor resources, but each successor receives a new value name. This directly supports append-only ancestry.

## Cycles and recursion

A dependency graph cycle is not used to mean runtime recursion. Recursion/control loops are represented through explicit basic blocks in lower GVM control flow. This keeps dependency cycles distinct from executable loops.
