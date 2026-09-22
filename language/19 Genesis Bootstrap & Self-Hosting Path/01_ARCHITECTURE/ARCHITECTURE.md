# Section 19 Architecture

```text
trusted host seed (Python oracle)
        |
        v
Stage-0 compiler + verifier
        |
        v
bootstrap_controller.gen --------+
        |                         |
        v                         |
Stage-0 GIO bytecode              |
        |                         |
        v                         |
Genesis Bootstrap Runtime         |
        |                         |
        +--> typed BRANE Compiler Port
                    |
                    v
             compile same source
                    |
                    v
               Stage-1 GIO
                    |
                    v
             execute Stage-1
                    |
                    +--> compile same source
                              |
                              v
                         Stage-2 GIO
```

Closure condition for this section:

`SHA256(Stage0) == SHA256(Stage1) == SHA256(Stage2)`

This proves deterministic rebuild closure for the bootstrap controller against the declared Stage-0 oracle. It does not prove the host compiler is correct and it does not remove the host compiler from the trusted computing base.
