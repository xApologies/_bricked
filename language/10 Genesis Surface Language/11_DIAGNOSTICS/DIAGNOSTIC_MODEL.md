# Diagnostics

Frontend diagnostics are structured as:

```text
CODE file:line: message
```

Primary v0.1 frontend codes:

- `GEN_VERSION`
- `MODULE_HEADER`
- `MODULE_CLOSE`
- `STATEMENT_UNKNOWN`
- `SYNTAX`
- `ATTR_JSON`
- `DUPLICATE_VALUE`
- `EXPORT_UNKNOWN`
- `SOURCE_TYPE`
- `SEMANTIC_CHECK`

Section 09 diagnostics are preserved verbatim after lowering, including bridge, linear ownership, typestate, effect, closure, and capability failures.
