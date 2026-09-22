# Deterministic graph scheduler

The v0.1 compiler schedules GIR as follows:

1. infer producer->consumer data dependencies;
2. add explicit `dependency` and `effect_order` edges;
3. verify all referenced producers exist;
4. run Kahn topological sort;
5. choose the lexicographically smallest node ID among simultaneously ready nodes;
6. reject remaining-cycle graphs;
7. allocate output registers in emitted order.

This gives reproducible bytecode independent of JSON node ordering.
