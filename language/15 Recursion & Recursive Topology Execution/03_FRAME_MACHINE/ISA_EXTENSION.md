# Recursion ISA extension

Section 15 reserves `0x0090..0x0097` for recursive frame semantics.

| Opcode | Value | Meaning |
|---|---:|---|
| `RCALL` | `0x0090` | create child frame and transfer arguments |
| `RRETURN` | `0x0091` | return one closed value to parent frame |
| `RECURSION_CLOSE` | `0x0092` | seal current frame and emit local closure witness |
| `HISTORY_ENTER` | `0x0093` | extend inherited visit/history state |
| `HISTORY_CHECK` | `0x0094` | test/reject repeated topology key |
| `FUEL_GUARD` | `0x0095` | consume/check recursive fuel |
| `YIELD_RECURSION` | `0x0096` | suspend persistent recursion with continuation |
| `RESUME_RECURSION` | `0x0097` | resume a validated continuation |

The reference compiler currently emits `RCALL`, `RRETURN`, and `RECURSION_CLOSE` directly; metric/fuel/history admission is carried in the call and function metadata and enforced by both verifier and runtime.
