# Architecture

```text
                         project source
                              |
                      genesis.pkg.json
                              |
                       manifest validator
                              |
                 +------------+-------------+
                 |                          |
          dependency constraints      module ownership
                 |                          |
                 v                          v
          deterministic resolver ----> import discipline
                 |
            registry entries
                 |
       content hash verification
                 |
        content-addressed store
                 |
          genesis.lock.json
                 |
      package effect/capability audit
                 |
        dependency-first source set
                 |
          Section 11 toolchain
                 |
                GVM
                 |
             execution
```

## Boundary

Section 12 is a distribution/composition layer. The following remain beneath it and are not redefined here:

- GIR/GVM instruction semantics,
- chirality-fabric execution semantics,
- Portal/Rainbow Road closure,
- QFT/GR transduction,
- quantum linear ownership,
- static effect semantics,
- optimizer equivalence rules.

A package cannot grant semantic authority that the static checker or backend does not already permit.
