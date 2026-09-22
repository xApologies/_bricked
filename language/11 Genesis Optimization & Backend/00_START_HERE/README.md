# Section 11 — Genesis Optimizer + Backend Code Generation

Section 11 sits after the Section 10 frontend and before packaging/standard-library work. It accepts the linked, statically verified GIR graph from Section 09, performs conservative proof-preserving optimization, then generates Section 08 GVM bytecode.

```text
Genesis .gen
  -> Section 10 frontend
  -> Section 09 linked + statically checked GIR
  -> Section 11 optimizer / code generator
  -> Section 08 GVM verifier + bytecode
  -> Section 01–07 execution stack
```

The optimizer is deliberately conservative. Portal closure, Rainbow Road history, sector bridges, quantum linear ownership, measurement, provenance, and effect order are semantic barriers. Section 11 does not optimize through those barriers merely to reduce instruction count.
