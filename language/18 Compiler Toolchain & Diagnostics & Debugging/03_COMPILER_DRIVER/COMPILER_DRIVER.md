# Compiler driver

A build is a closed transformation from `(source bytes, target, toolchain version, explicit options)` to a build bundle. The bundle contains `.gio`, disassembly, verifier proof, source map, and normalized build manifest. The driver performs the same compile/verify path whether invoked by `check`, `build`, `run`, `trace`, or `test`.
