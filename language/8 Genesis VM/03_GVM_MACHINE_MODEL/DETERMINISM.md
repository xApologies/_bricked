# Determinism contract

For all non-measurement operations, the reference GVM is deterministic under canonical serialization.

Measurement must receive either:

- an external result from a physical backend; or
- an explicit deterministic reference seed/sample token in simulation.

The seed/result becomes provenance. Hidden process-global randomness is forbidden in normative execution.
