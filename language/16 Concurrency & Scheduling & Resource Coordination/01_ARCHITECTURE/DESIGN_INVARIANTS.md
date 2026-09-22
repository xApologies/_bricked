# Design invariants

- Logical time is monotone and deterministic.
- Same program + same declared resources + same backend capability contract => same reference schedule receipt.
- Equal-priority tasks use deterministic round-robin requeue order.
- Priority is explicit and bounded; hidden host priorities are not semantic input.
- Resource acquisition is explicit; no invisible locks.
- Exclusive leases require sole ownership of the full declared capacity.
- Shared leases consume declared capacity units.
- Task close requires zero live leases.
- Cancellation releases all owned leases and preserves an audit event.
- Persistent recursion enters Section 16 only through validated Section-15-compatible continuation tokens.
- `SUSPENDED`, `BLOCKED`, `CLOSED`, `FAILED`, and `CANCELLED` are distinct states.
- Deadlock is reported with a wait-for cycle; it is not converted into success.
