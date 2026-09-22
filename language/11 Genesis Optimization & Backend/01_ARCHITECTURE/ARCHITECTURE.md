# Architecture

```text
                 linked GIR
                    |
              graph analysis
                    |
      +-------------+-------------+
      |             |             |
  dependency     effect       linear/closure
   analysis      barriers        barriers
      |             |             |
      +-------------+-------------+
                    |
          optimization profile
          O0 / OAUDIT / O1
                    |
              optimized GIR
                    |
        Section 09 re-verification
                    |
           capability re-check
                    |
             GVM code generation
                    |
       reference / audit / compact
                    |
          Section 08 verifier
                    |
               .gvm bytecode
```

The optimizer never grants authority. Any optimized graph must independently pass the Section 09 checker and the target backend capability gate before code generation.
