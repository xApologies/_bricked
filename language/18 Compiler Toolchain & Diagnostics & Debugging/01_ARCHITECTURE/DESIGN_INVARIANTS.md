# Design invariants

1. A diagnostic never changes program meaning.
2. A source map identifies the instruction produced by a source statement; it is not executable authority.
3. A debugger observes deterministic reference execution; it cannot write BLACKGLASS state except through the same verified operations as normal execution.
4. Build identity is content-addressed from normalized inputs and toolchain configuration.
5. Absolute host paths and wall-clock time are excluded from semantic build identity.
6. Rebuilding identical input with identical configuration yields byte-identical `.gio`, proof, disassembly, source map, and normalized manifest artifacts.
7. Runtime trace events retain instruction source, operation, register delta, and receipt/provenance linkage.
8. The verifier cannot be bypassed by build, run, trace, debug, or test commands.
9. Failure diagnostics carry stable codes and machine-readable JSON representations.
10. Tooling state is derived state; canonical Genesis/BLACKGLASS source remains immutable.
