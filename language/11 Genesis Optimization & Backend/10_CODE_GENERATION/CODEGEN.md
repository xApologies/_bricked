# Backend code generation

Section 11 currently targets the Section 08 GVM ABI. Three code-generation profiles are defined:

- `reference` — normal GVM with source node labels;
- `audit` — source labels plus Section 11 optimization certificate in program metadata;
- `compact` — same semantics, but strips per-instruction source labels after compilation.

The GVM target is an execution backend, not the definition of Genesis semantics. Future native chirality-machine, FPGA, GPU, or specialized targets can implement the same code-generation contract.
