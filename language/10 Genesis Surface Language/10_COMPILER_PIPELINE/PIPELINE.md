# Compiler pipeline

```text
.gen
 -> lexical normalization
 -> parse
 -> AST validation
 -> lower to GIR-MODULE
 -> Section 09 check_module
 -> Section 09 link_bundle
 -> Section 08 compile_gir
 -> GVM verify
 -> bytecode
 -> VM/backend execution
```

The frontend intentionally reuses the previously established semantic layers rather than duplicating their rules.
