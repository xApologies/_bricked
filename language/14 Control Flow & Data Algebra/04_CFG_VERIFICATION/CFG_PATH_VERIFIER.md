# CFG / Path-aware verifier

The straight-line verifier from Section 08 is insufficient once explicit branches exist. Section 14 symbolically explores all reachable control-flow paths and checks use-before-definition, register SSA, branch condition types, QSTATE linear liveness, Portal/Road typestates, valid targets, and closure at every reachable halt.

This admits mutually exclusive QSTATE consumption while still rejecting double consumption on any single path. A Portal closed on only one side of a branch is rejected because another reachable halt leaks OPEN state.

## Exhaustive match path normalization
The compiler does not create a synthetic impossible fallthrough after an exhaustive match. After all earlier tag tests fail, the final explicit exhaustive case is lowered as guaranteed; a `_` default, when present, must be the final case. This keeps verifier path counts aligned with semantically possible match alternatives.
