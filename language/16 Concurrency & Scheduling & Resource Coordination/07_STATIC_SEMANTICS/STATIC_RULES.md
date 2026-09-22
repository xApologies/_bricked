# Static rules

The Section 16 verifier checks:

- Genesis concurrency surface version 0.5.0.
- All spawn templates exist and handles are unique.
- Join handles resolve to spawned tasks.
- Capacities, priorities, and quantums are bounded.
- Every task ends in explicit `close`.
- Resource names and lease units are valid.
- A task cannot statically double-acquire the same resource.
- A task cannot statically release a resource it has not acquired.
- A task cannot reach source-level close with an unreleased resource.
- Work and recursion slice budgets are positive.

Deadlock is intentionally a runtime property in v0.1; the runtime emits a witness if it occurs.
