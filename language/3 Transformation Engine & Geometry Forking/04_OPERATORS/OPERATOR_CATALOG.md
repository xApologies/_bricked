# Native transformation operator catalog

The Section 03 operators are computational transformations over mapped chirality cells.

| Operator | Primary effect | Meaning in runtime model |
|---|---|---|
| `INHERIT` | lineage | child continuation with no cell rewrite |
| `STABILIZE_RHO` | persistence | increase persistence component within bounds |
| `DESTABILIZE_RHO` | persistence | decrease persistence component within bounds |
| `SET_TAU` | translation | set/shift translation-readiness component |
| `SET_SIGMA` | admissibility | set/shift admissibility component |
| `REDISTRIBUTE_RHO` | persistence | pairwise redistribution preserving selected pair sum |
| `NORMALIZE_COMPONENTS` | declared fields | bounded re-centering of selected Q0.16 components |
| `MIRROR_CHIRALITY` | chirality + occupancy | mirror the cell's chirality representation |
| `SET_CELL_FIELDS` | explicit | low-level typed fixture/admin operator |

`INHERIT`, `STABILIZE`, `REDISTRIBUTE`, `DESTABILIZE`, `CLOSE`, and `NORMALIZE` align with the previously recovered runtime primitive family, but this implementation does not claim that these fixture algorithms exhaust their scientific meaning.
