# Routing Policy

Section 04 implements deterministic constrained shortest-path selection over a directed multigraph.

Ranking order:

```text
1. all hard admission predicates pass
2. lowest summed edge cost
3. fewest hops
4. highest route minimum bandwidth
5. lexical path ID tie-break
```

This prevents nondeterministic recovery behavior. Future Section 05 may add multipath, coherent/QFT route state, policy routing, and persistent road optimization.
