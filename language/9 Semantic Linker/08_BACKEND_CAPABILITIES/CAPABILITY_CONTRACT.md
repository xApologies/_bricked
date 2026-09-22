# Backend capability contract

A backend capability manifest advertises:

- ABI version;
- supported GIR/GVM operation names;
- supported effects;
- sectors (`GENERIC`, `QFT`, `GR`, etc.);
- feature flags such as `portal`, `rainbow_road`, `sector_bridge`, `quantum_linear`, and `provenance_receipts`.

A linked program is rejected before bytecode execution when required capabilities are absent. This prevents "compile succeeded, backend cannot possibly realize it" from becoming a runtime discovery mechanism.
