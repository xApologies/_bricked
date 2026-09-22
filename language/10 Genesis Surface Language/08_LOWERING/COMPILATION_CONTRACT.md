# Compilation contract

For each source file:

1. parse without inventing missing tokens;
2. reject duplicate local output identities;
3. lower each statement to one GIR node;
4. attach a source-map witness;
5. derive exact effects;
6. construct a `GIR-MODULE`;
7. run the Section 09 module checker;
8. only then expose the module to the semantic linker.

A multi-file build then uses Section 09 symbol resolution/linking and Section 08 compilation unchanged.
