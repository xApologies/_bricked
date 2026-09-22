# Section 18 release notes

- Adds deterministic compiler driver and normalized build identity.
- Adds stable machine-readable diagnostics with source spans.
- Adds instruction-level source maps.
- Adds receipt-linked deterministic tracing with register snapshots.
- Adds replay debugger with line/opcode breakpoints, step, seek, continue, register and receipt inspection.
- Adds `.gtest.json` conformance test runner.
- Adds reproducibility comparison across independent output directories.
- Adds reference CLI for check/build/run/disasm/trace/test/repro/doctor.
- Does not add a verifier bypass, debugger mutation channel, or new BLACKGLASS authority.

Validation: Section 18 77/77 PASS; Section 17 regression 80/80 PASS; 7/7 system programs CLOSED under tracing; 7/7 reproducibility witnesses PASS; 3/3 gtest cases PASS.
