# Reference bootstrap sources

`bootstrap_controller.gen` is a Genesis program that owns the rebuild transaction. It reads its own immutable source, places it in CAS, mounts a typed compiler port, requests compilation, and submits the compiler result through the BLACKGLASS proposal/admission boundary.

The compiler behind the port is deliberately Stage-0 host code in Section 19. The fixed-point run therefore demonstrates Genesis-controlled deterministic rebuilding, not full compiler self-hosting.
