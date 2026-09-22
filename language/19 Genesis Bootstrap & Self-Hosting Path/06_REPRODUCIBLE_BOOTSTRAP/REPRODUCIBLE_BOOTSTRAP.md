# Reproducible bootstrap

A valid bootstrap closure requires:

1. canonical source bytes;
2. deterministic parser/verifier/encoder behavior;
3. no wall-clock timestamps in semantic artifacts;
4. no absolute filesystem paths in stage identity;
5. identical Stage-0/1/2 bytecode hashes;
6. verifier proof roots that agree across stages;
7. immutable source and bytecode objects in CAS;
8. a receipt chain linking each stage to its predecessor.

A mismatch is a hard bootstrap failure and blocks v1.0 freeze.
