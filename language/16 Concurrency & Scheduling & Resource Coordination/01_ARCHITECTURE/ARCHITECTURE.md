# Architecture

Execution path:

`Genesis source -> frontend/GIR -> static semantics -> GVM -> Section 16 logical scheduler -> Section 01–15 execution services -> backend realization`

Section 16 introduces five runtime objects: `Task`, `Schedule`, `Resource`, `Lease`, and `WaitGraph`. A task is a schedulable continuation of admitted Genesis work. A lease is explicit authority to use a finite resource. The wait graph is derived state used for deadlock detection and auditing.

No language semantics depend on Python threads, host process IDs, wall-clock timing, or operating-system scheduling.
