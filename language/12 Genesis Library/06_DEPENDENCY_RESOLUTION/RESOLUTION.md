# Dependency resolution

Resolution is a deterministic backtracking constraint solver over the local registry.

The solver accumulates all requirements for a name, selects candidate versions in descending order, recursively adds their dependencies, and backtracks on incompatibility. The resulting graph is then checked for cycles and emitted dependency-first.

The package runtime rejects missing packages, incompatible constraints, cyclic graphs and frozen-lock drift.
