# Genesis Chirality Machine — Section 19

**Title:** Genesis Bootstrap + Self-Hosting Path

Section 19 establishes a deterministic bootstrap chain without falsely claiming that Genesis is already fully self-hosted. The Python compiler/runtime from Sections 17–18 remains the Stage-0 oracle. Genesis now owns the bootstrap controller and rebuild transaction, while the compiler implementation behind the typed compiler port is still host-resident.

The reference bootstrap demonstrates a Stage-0 → Stage-1 → Stage-2 fixed point: a Genesis bootstrap controller is compiled by the host oracle, executes, asks a typed BRANE compiler port to compile its own source, and the resulting bytecode reproduces identically on the next stage.

**Status:** BOOTSTRAP_FIXED_POINT / PARTIAL_SELF_HOST. **Not:** FULL_SELF_HOST.
