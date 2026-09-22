# Surface grammar examples

Core forms:
- `record Name { field: TYPE, ... }`
- `enum Name { Tag(TYPE), Empty, ... }`
- `let x : TYPE = expression`
- `if cond { ... } else { ... }`
- `match sum { Tag(v) => { ... } Empty => { ... } }`
- `repeat N { ... }`
- existing Section 10 base operations remain usable inside control regions.
