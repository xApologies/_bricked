# Trust boundary and trusting-trust discipline

A three-stage fixed point shows reproducibility under the same seed compiler. It cannot by itself detect a malicious or systematically wrong Stage-0 compiler that reproduces its own behavior. Section 20 must therefore treat the Python implementation as an oracle to be tested against conformance vectors, independent encodings where practical, and semantic proof obligations.

Section 19 never uses the word `self-hosted` as a release status. The truthful status is `PARTIAL_SELF_HOST` because Genesis controls rebuilding but the compiler implementation remains host-resident.
