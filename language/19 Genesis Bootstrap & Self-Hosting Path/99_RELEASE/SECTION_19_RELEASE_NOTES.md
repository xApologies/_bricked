# Section 19 release notes

Section 19 adds deterministic staged bootstrapping and a truthful self-host frontier. The Genesis bootstrap controller can rebuild its own executable image through a typed BRANE compiler port and reaches a byte-for-byte Stage-0/1/2 fixed point. Compilation itself still uses the declared Python Stage-0 oracle.

This is intentionally a partial-self-host milestone. Section 20 will freeze language/ABI/conformance behavior; completing compiler self-hosting can continue after the v1.0 freeze without changing v1.0 semantics.
