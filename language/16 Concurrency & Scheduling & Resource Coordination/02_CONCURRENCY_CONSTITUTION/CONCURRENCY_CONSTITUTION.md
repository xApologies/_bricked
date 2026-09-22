# Concurrency constitution

Concurrency is the admissible interleaving or backend-parallel realization of multiple independent or partially dependent Genesis execution continuations.

The semantic unit is a **task**, not a host thread. A task may advance, yield, block on a resource, suspend as a recursive continuation, close, fail, or be cancelled. The scheduler owns progression authority; resources own finite-capacity admission authority.

Structured concurrency v0.1 is represented by an explicit spawn set and join set. A program does not report ordinary closure until its declared join set reaches terminal states.
