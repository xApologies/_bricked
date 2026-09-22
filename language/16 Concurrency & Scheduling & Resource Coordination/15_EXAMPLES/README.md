# Section 16 reference programs

1. `01_ROUND_ROBIN.gen` — deterministic equal-priority interleaving.
2. `02_EXCLUSIVE_RESOURCE.gen` — exclusive fabric lease with deterministic blocking/wake-up.
3. `03_SHARED_CAPACITY.gen` — capacity-2 shared Rainbow Bus lease.
4. `04_PRIORITY.gen` — strict deterministic priority ordering.
5. `05_RECURSIVE_COOPERATIVE.gen` — Section-15-compatible persistent recursion slices scheduled beside an ordinary task.
6. `06_DEADLOCK_WITNESS.gen` — expected `DEADLOCK`; preserves the wait-for-cycle witness rather than hiding the failure.
