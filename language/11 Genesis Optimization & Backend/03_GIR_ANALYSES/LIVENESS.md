# Liveness

A node is live if it is effectful, exported, or transitively required by a live node. Dead-node removal is legal only for nodes whose effect set is empty. When a removed pure node occurs in an explicit `effect_order` chain, Section 11 conservatively bypasses the removed node to preserve predecessor/successor ordering.
