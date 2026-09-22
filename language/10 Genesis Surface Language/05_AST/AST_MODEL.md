# AST model

The AST is intentionally semantic-light. It records:

- module name and source version;
- typed imports;
- executable statements with source line, operation family, output identity, arguments, attributes, and optional declared type;
- explicit exports.

It does not decide whether a Portal may cross a sector boundary, whether a QSTATE has been moved, or whether closure is complete. Those are Section 09 obligations after lowering.
