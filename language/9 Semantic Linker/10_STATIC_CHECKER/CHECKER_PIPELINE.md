# Static checker pipeline

For a module or linked GIR graph:

1. seed the type environment from typed imports;
2. schedule local nodes using data and effect-order dependencies;
3. validate opcode argument arity/kinds;
4. infer refined output type;
5. compare any declared coarse/refined type;
6. collect effects;
7. update Portal/Road/QSTATE typestate;
8. record Bridge witnesses and validate cross-sector Portal usage;
9. validate linear ownership;
10. reject leaked OPEN Portal/Road resources;
11. validate declared exports.

Diagnostics are deterministic and include a code, node/module context, and message.
