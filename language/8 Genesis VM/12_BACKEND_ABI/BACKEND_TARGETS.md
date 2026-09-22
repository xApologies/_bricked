# Backend targets

The same GVM contract can be realized by:

- Python reference backend — current oracle;
- native CPU runtime;
- GPU accelerator backend;
- FPGA hardware emulator/prototype;
- custom chirality-fabric controller;
- quantum-device adapter for supported `QSTATE` subprograms;
- deterministic simulator/testing backend.

Backend replacement must not change GIR/GVM semantic meaning.
