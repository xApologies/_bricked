# Reference CLI

- `check SOURCE`: parse + verify; emit diagnostics on failure.
- `build SOURCE -o DIR`: emit deterministic build bundle.
- `run SOURCE --base DIR [--seed endpoint:path=file]`: build and execute.
- `disasm SOURCE`: print deterministic disassembly.
- `trace SOURCE --base DIR`: execute and emit trace JSON.
- `test CASE...`: execute `.gtest.json` cases.
- `doctor`: validate reference implementation imports and core contracts.

Exit status 0 means requested operation satisfied its contract. Non-zero means compile, verification, execution, test, or toolchain contract failure.
