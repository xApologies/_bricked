# Superposition semantics

Superposition is coherent state-space composition, not a list of simultaneous classical values.

The reference constructor accepts named branches and complex amplitudes, normalizes them, and produces a `PURE` state. Branch labels are semantic basis labels. The runtime does not infer physical basis meaning from their names.

Compiler consequence: a superposed value cannot be branched on by ordinary classical `if` without an explicit measurement or readout effect.
