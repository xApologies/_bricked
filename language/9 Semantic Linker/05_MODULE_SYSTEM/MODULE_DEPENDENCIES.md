# Module dependency graph

Each `imports[].from` creates a module dependency. The semantic linker:

1. validates module names;
2. resolves import symbols;
3. rejects unresolved/ambiguous symbols;
4. rejects dependency cycles in v0.1;
5. derives deterministic module order lexically among otherwise independent modules.

A future version may introduce explicit recursive interfaces. v0.1 does not infer such semantics.
