# Self-host frontier

Section 19 intentionally separates *control ownership* from *implementation ownership*.

| Component | Section 19 status | Meaning |
|---|---|---|
| Bootstrap controller | GENESIS_NATIVE | Authored in Genesis and executed as Genesis bytecode |
| Bootstrap transaction / stage sequencing | GENESIS_CONTROLLED | Sequenced by Genesis execution |
| Source/CAS transport | GENESIS_CONTROLLED | Uses Section 17 typed I/O boundary |
| Compiler-port request | GENESIS_CONTROLLED | Typed BRANE request from Genesis |
| Parser | HOST_ORACLE | Python reference implementation |
| Static verifier | HOST_ORACLE | Python reference implementation |
| Bytecode encoder | HOST_ORACLE | Python reference implementation |
| Compiler-port adapter | HOST_ORACLE | Bootstrap bridge to Stage-0 compiler |
| Runtime/VM | HOST_ORACLE | Python reference implementation |
| BLACKGLASS migration | DEFERRED | Begins after Genesis v1.0 freeze |

The machine-readable frontier is in `15_EXAMPLES/self_host_frontier.json`.
