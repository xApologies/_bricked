# Section 12 — Genesis Standard Library + Package/Dependency Runtime

Section 12 adds deterministic package identity, dependency resolution, lockfiles, a content-addressed local package store, package-level provenance, and the first executable Genesis standard-library package set.

```text
Genesis project
   -> genesis.pkg.json
   -> local/offline registry
   -> semantic-version resolver
   -> content-addressed package store
   -> genesis.lock.json
   -> package/module ownership audit
   -> package effect-budget audit
   -> Section 10 frontend
   -> Section 09 static semantics/linker
   -> Section 11 optimizer/codegen
   -> Section 08 GVM
   -> Sections 01–07 execution stack
```

The package layer does **not** redefine Genesis semantics. It selects and authenticates source modules and then hands those modules to the already-defined compiler stack.

The initial standard library is intentionally small. Genesis v0.1.0 does not yet have parameterized functions/generics, so Section 12 separates:

- executable reusable source packages (fabric and fixture modules), and
- contract packages that register subsystem/effect/capability surfaces without pretending to provide abstractions the language cannot yet express.

All resolution is local/offline in this reference implementation. Network distribution is deliberately out of scope.
