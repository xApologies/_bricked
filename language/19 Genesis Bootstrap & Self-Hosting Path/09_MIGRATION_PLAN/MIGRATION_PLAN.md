# Migration plan

The post-v1.0 self-hosting path is incremental:

1. move compiler tables and normalization logic into Genesis packages;
2. move parser/AST construction;
3. move static verifier and proof-ledger generation;
4. move semantic linker;
5. move optimizer/code generation;
6. replace the bootstrap compiler port with the Genesis-native compiler package;
7. run independent Stage-N fixed-point and differential conformance;
8. remove Python from the mandatory boot path only after parity is demonstrated.

BLACKGLASS 3.0 migration consumes the frozen Section-20 language/ABI. It must not be used as an excuse to change Genesis semantics during migration.
