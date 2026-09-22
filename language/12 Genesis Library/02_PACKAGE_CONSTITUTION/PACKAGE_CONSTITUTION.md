# Package constitution

Canonical package descriptor: `genesis.pkg.json`.

Required identity fields:

- `manifest = "GENESIS-PACKAGE"`
- `schema_version = "0.1.0"`
- `name`
- `version`
- `genesis = "0.1.0"`
- `kind` (`library`, `contract`, or `application`)

A package optionally declares source modules, direct dependencies, an effect budget, backend capability requirements, and root entry exports.

The manifest is not itself the final package identity. The runtime hashes all package-controlled files to produce a content root. The resolved lockfile binds dependency coordinates to those roots.
