# Termination and closure

Termination and closure are not synonyms.

- **Termination** answers whether a recursive computation reaches a finite return.
- **Closure** answers whether a returning frame has resolved all obligations that may be inherited by its parent.

`decreases` and `fuel` provide finite execution contracts. `visit_once` provides cycle exclusion plus a depth ceiling. Persistent recursion explicitly has no static finite termination claim and therefore returns `SUSPENDED` continuations at slice boundaries.

A recursion proof receipt records contract mode, maximum depth observed, recursive edge count, frame closure count, history root, and whether the result halted or suspended.
