# Static recursion rules

- A `rec fn` must declare exactly one recursion contract.
- `max_depth` is required for `decreases` and `visit_once` in v0.1 and must be `1..4096`.
- `fuel N` must be `1..4096`.
- A `recur f(...)` statement may target only the current function in v0.1.
- For `decreases m`, the argument supplied to the metric parameter must have affine provenance `m + k` where `k < 0`.
- Recursive call arity and parameter types are checked.
- Recursive CFG branches must close on every `return` path.
- Mutual recursive strongly-connected components are rejected.
- Recursive calls may not implicitly capture unresolved linear resources.
