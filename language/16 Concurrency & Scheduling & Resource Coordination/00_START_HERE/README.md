# Genesis Chirality Machine — Section 16

**Title:** Concurrency + Scheduling + Resource Coordination

Section 16 adds a deterministic logical concurrency layer above the Section 01–15 machine. The semantic scheduler is not an OS thread API. Genesis tasks, resource leases, suspension, wake-up, cancellation, and deadlock witnesses are defined independently of the CPU/GPU/FPGA backend that may eventually realize them in parallel.

Core rule: concurrency changes *when admitted work advances*, not the identity or semantics of the underlying Geometric, Portal, Road, chirality fabric, or Section-15 recursion continuation.

The reference implementation uses a deterministic cooperative scheduler with priority classes and round-robin fairness among equal-priority ready tasks. Physical parallelism is a backend realization choice and must preserve the same observable schedule/closure contract where determinism is required.
