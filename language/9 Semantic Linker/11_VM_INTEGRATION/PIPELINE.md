# Section 08 integration

The reference linker vendors the Section 08 Python VM package solely so Part A is executable in isolation.

```text
link_bundle()
  -> linked GIR
  -> Section 09 static PASS
  -> Section 08 compile_gir()
  -> Section 08 verify()
  -> Section 08 encode()
  -> .gvm
```

The vendored package is byte-for-byte copied from the current Section 08 core implementation in this build. Its presence does not create a second semantic authority; Section 08 remains the execution-model source layer.
