# Frontend architecture

```text
                 .gen source
                    |
              UTF-8 lexical layer
                    |
          one-statement-per-line parser
                    |
              typed source AST
                    |
       +------------+------------+
       |                         |
  source map                 diagnostics
       |                         |
       +------------+------------+
                    |
             semantic lowerer
                    |
                GIR-MODULE
                    |
              Section 09
        static checker / linker
                    |
                Section 08
                 GVM
```

The parser is deliberately small. All difficult legality questions remain where they belong: Section 09. The frontend cannot grant itself transport authority, evade linear ownership, erase a required QFT/GR bridge, leave a Portal open, or invent a backend capability.
