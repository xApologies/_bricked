# Debugger model

The reference debugger is trace/replay oriented. A tracing runtime executes the verified program normally while recording deterministic snapshots after each instruction. A debug session then supports breakpoints by source line or opcode, seek, step, continue, register inspection, receipt inspection, and provenance-root inspection.

There is no debugger-only mutation channel.
