# Failure model

Section 13 introduces explicit callable diagnostics. Representative codes:

- `CALLABLE_SYNTAX` — malformed function/generic/parameter declaration.
- `FUNCTION_DUPLICATE` — duplicate function or callable alias collision.
- `CALLABLE_IMPORT_UNRESOLVED` — imported function does not exist.
- `CALLABLE_NOT_PUBLIC` — cross-module call targets a private function.
- `CALLABLE_UNRESOLVED` — call target cannot be resolved.
- `GENERIC_ARITY` — wrong number of type arguments.
- `GENERIC_BOUND` — concrete type violates a generic constraint.
- `GENERIC_TYPE` — malformed concrete type expression.
- `CALL_ARITY` — wrong number of value arguments.
- `RETURN_MISSING` / `RETURN_MULTIPLE` / `RETURN_SYNTAX` — invalid return structure.
- `RETURN_NOT_LOCAL` — v0.1 callable attempts to return a value it did not produce locally.
- `FUNCTION_EFFECT_EXCEEDED` — expanded effect set exceeds declared effect contract.
- `RECURSION_UNSUPPORTED` — direct or indirect recursive call graph.
- `CALLABLE_PROOF_FAILED` — specialized return/effect/Section 09 proof ledger did not close.

Lower-layer failures remain authoritative after expansion, including `LINEAR_ALIAS`, `LINEAR_USE_AFTER_MOVE`, `PORTAL_UNCLOSED`, `ROAD_UNCLOSED`, `BRIDGE_REQUIRED`, type mismatches, backend capability failures, package dependency failures, and optimizer differential-equivalence failures.
