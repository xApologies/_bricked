# Architecture

Section 08 made the execution language real. Section 09 makes it **linkable and statically governable**.

```text
GIR Module A       GIR Module B       GIR Module C
    |                  |                  |
    +---- typed imports / exports --------+
                       |
                 Symbol Resolver
                       |
              Module Dependency DAG
                       |
        +--------------+---------------+
        |              |               |
   Type checker    Effect checker   Capability checker
        |              |               |
        +---------- Proof ledger -------+
                       |
                Semantic Linker
                       |
          alpha-renamed unified GIR
                       |
               Section 08 compiler
                       |
                     GVM
```

## Core law

**Linkage may combine graphs; it may not erase the boundaries that establish identity, provenance, ownership, sector transition, or closure obligations.**

Every linked output carries a module map and content-addressed link receipt so the flattened executable graph can be traced back to each contributing module and symbol.
