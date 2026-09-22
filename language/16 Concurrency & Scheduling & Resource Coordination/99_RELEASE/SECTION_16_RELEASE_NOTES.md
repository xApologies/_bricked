# Section 16 v0.1.0 release notes

Section 16 establishes deterministic logical concurrency independent of host operating-system thread semantics. It adds task state, explicit finite resource leases, shared/exclusive coordination, deterministic wake-up, structured spawn/join scope, cancellation cleanup, deadlock witnesses, and schedulable Section-15-compatible persistent recursion continuations.

The reference scheduler is intentionally cooperative. This gives Genesis a stable semantic oracle before native BLACKGLASS backends attempt true parallel execution.

Validation at release: 64/64 Section 16 tests PASS; 60/60 Section 15 regression PASS; 6/6 reference scenarios match expected status (5 CLOSED, 1 intentional DEADLOCK witness).
