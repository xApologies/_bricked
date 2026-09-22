# Content addressing

Compiler output includes:

- canonical GIR hash;
- canonical GVM program hash;
- bytecode SHA-256;
- backend ABI version required;
- source-map node IDs;
- verifier result.

A bytecode decoder verifies the embedded digest before execution.
