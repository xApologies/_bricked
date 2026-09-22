# Module ownership and direct dependency discipline

Every source module has exactly one owning package in a build graph.

For an import `use X::symbol ...`, `X` must be:

1. a module owned by the importing package, or
2. a module owned by one of that package's **direct** declared dependencies.

Importing a module available only transitively is rejected. This prevents hidden dependency coupling and makes package provenance explicit.
