# Genesis Chirality Machine — Section 15
## Recursion + Recursive Topology Execution

Section 15 adds recursion as a machine-level control relationship rather than hiding it inside Python. It introduces frame-local recursive calls, explicit termination/guard contracts, recursive closure receipts, history-root inheritance, cycle-aware topology traversal, and suspend/resume semantics for persistent recursion.

The v0.1 surface subset is `genesis 0.4.0`. Direct recursion is executable. Mutual recursion is deliberately rejected in this release rather than silently treated as valid. Every executable recursion class has an explicit safety contract:

- `decreases <metric> max_depth N`: a well-founded integer measure must strictly decrease at every self-call.
- `fuel N`: recursion consumes finite fuel at every self-call.
- `visit_once <key> max_depth N`: recursive identities are tracked in frame history and repeated active/history keys are rejected.
- persistent recursion is represented as a resumable task with bounded execution slices; it does not pretend an unbounded computation terminates.

Recursive frames cannot implicitly carry unresolved linear resources (open Portals, open Roads, or live QSTATE ownership) across recursive/yield boundaries.
