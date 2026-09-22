# Architecture

Execution path: `Genesis 0.3 source -> Section 14 AST -> typed lowering -> GVM/CF v0.2 -> reference chirality-machine backend`.

Control is represented by explicit `BRANCH`/`JUMP` regions. Data is immutable and register/SSA-oriented. Branch-local identities do not escape in v0.1; no hidden phi nodes, mutation, rollback, or unbounded host-language loops are synthesized.
