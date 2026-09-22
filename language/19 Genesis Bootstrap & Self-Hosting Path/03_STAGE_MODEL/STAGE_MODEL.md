# Bootstrap stage model

- **Stage 0:** trusted Python oracle compiler produces the first executable bootstrap controller.
- **Stage 1:** Stage-0 Genesis controller executes and requests compilation of its own source through `CompilerPort<compile>`.
- **Stage 2:** Stage-1 controller executes the same transaction again.
- **Fixed point:** byte-for-byte identical encoded program across Stage 0, Stage 1 and Stage 2.

The stage receipt records source digest, bytecode digest, program id, verifier proof root, compiler-port identity, host-oracle identity, and the prior stage digest.
