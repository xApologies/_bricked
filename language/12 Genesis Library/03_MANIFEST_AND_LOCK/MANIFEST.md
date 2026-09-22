# Manifest and lockfile

`genesis.pkg.json` describes intent. `genesis.lock.json` records the deterministic realized dependency graph.

A lock entry contains:

- package name,
- resolved version,
- content SHA-256 root,
- direct dependency requirements,
- module names,
- dependency-first order.

Frozen builds reject hash drift even when a package retains the same name and version.
