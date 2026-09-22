# Section 12 recovery state

Title: **Genesis Standard Library + Package/Dependency Runtime**

Folder: `GENESIS_CHIRALITY_MACHINE_SECTION_12_STDLIB_PACKAGE_RUNTIME_v0.1.0_20260821`

Recovery anchor:

```text
project manifest
  -> deterministic local dependency resolution
  -> content SHA-256 identities
  -> lockfile
  -> content store
  -> module ownership/direct import audit
  -> effect-budget audit
  -> Section 11 optimized compiler path
  -> GVM execution
```

The standard-library v0.1 registry includes executable fabric/atomic fixture packages plus contract-only packages for Portal, Rainbow Road, Bridge, Quantum, Provenance and BRANE semantics.

Next logical section after Section 12: tooling/runtime ergonomics and development environment (diagnostics, REPL/build driver, debugger/trace tooling) or, if language capability is prioritized, callable abstractions/functions/generics so the stdlib can move beyond contract packages.
