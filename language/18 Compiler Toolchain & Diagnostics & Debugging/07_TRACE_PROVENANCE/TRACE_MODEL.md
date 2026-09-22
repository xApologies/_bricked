# Trace and provenance

A trace event binds:

- instruction index and opcode,
- source location,
- register names changed by the instruction,
- post-instruction register snapshot,
- boundary receipt emitted by that instruction,
- current provenance root.

This makes the debugger a projection over already-authorized execution rather than a parallel execution semantics.
