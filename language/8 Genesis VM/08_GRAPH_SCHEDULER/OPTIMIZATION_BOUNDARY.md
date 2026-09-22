# Optimization boundary

Optimizations may reorder operations only when they preserve:

- data dependencies;
- declared relationship/identity obligations;
- effect ordering;
- linear ownership;
- sector bridge ordering;
- Portal/Road closure;
- provenance ancestry.

The reference compiler intentionally performs no speculative reordering beyond deterministic topological scheduling.
