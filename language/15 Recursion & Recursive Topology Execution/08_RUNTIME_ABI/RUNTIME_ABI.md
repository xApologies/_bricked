# Runtime ABI

The recursive VM receives a verified `RecursiveProgram` and executes it with frame-local registers. The machine returns `RecursiveExecutionResult` containing exports plus a deterministic receipt.

Runtime enforcement repeats critical static checks: maximum depth, strictly decreasing metric, fuel exhaustion, visit-history repetition, closed-frame return, instruction-step budget, and continuation integrity. This duplication is intentional: the compiler is not a trusted authority over runtime resource safety.
