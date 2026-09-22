# GVM verifier rules

The v0.1 verifier checks:

- valid opcodes and register range;
- register use-after-definition;
- declared output type consistency;
- source-map uniqueness where present;
- no obvious use of consumed linear QSTATE values;
- Portal open/close typestate pairing;
- Road close pairing;
- explicit sector bridge declarations where a program declares a sector transition;
- valid control-flow targets for direct GVM programs;
- HALT/RETURN structure;
- no base-fabric mutation opcode exists;
- required effect declarations match the opcode table.

The reference runtime repeats dynamic checks because external backends may reject requests based on runtime state.
