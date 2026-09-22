# Section 15 reference implementation

`genesis_recursion` is the executable Python oracle for the Section 15 recursion contract. It compiles the `genesis 0.4.0` recursion subset to deterministic recursive bytecode and runs it using frame-local registers, runtime contract checks, deterministic closure receipts, and inherited history roots.

The package also provides the cycle-aware topology executor and suspend/resume persistent-recursion reference model.
