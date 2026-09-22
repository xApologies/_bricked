# Bootstrap constitution

The bootstrap chain has three authorities:

- **semantic authority** — the Genesis language/VM contracts established in Sections 01–18;
- **seed authority** — the minimum host implementation required to enter the system;
- **rebuild authority** — the Genesis-controlled program that deterministically requests and verifies rebuilding.

Section 19 moves rebuild orchestration into Genesis while preserving the host compiler as an explicit seed dependency. Full self-hosting is achieved only when the parser, verifier, linker, code generator, and required runtime can be rebuilt from Genesis-owned implementation sources without invoking the Python oracle.
