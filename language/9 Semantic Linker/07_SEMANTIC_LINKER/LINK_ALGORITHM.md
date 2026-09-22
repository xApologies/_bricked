# Semantic link algorithm

```text
parse modules
  -> validate names and declared interfaces
  -> build export symbol table
  -> resolve + type-check imports
  -> topologically order module dependency DAG
  -> alpha-rename each node and local SSA value
  -> substitute imported aliases with resolved global values
  -> rewrite internal edges
  -> merge nodes/edges
  -> choose declared bundle exports
  -> run linked static checker
  -> check backend capabilities
  -> emit proof-obligation ledger
  -> attach module/source map metadata
  -> compile with Section 08 GIR -> GVM
  -> verify GVM
  -> encode deterministic bytecode
  -> emit content-addressed link receipt
```
