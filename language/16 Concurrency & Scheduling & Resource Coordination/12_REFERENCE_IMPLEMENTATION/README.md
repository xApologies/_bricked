# Python reference implementation

`genesis_concurrency` is the Section 16 oracle/reference implementation. It defines deterministic logical scheduling, finite-capacity leases, block/wake behavior, cancellation cleanup, deadlock witnesses, bytecode encoding, and Section-15-compatible recursive continuation slices.

It is not the target runtime and does not define a requirement to use Python or OS threads in BLACKGLASS.
