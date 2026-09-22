# Storage + Content Addressing

The reference host exposes sandboxed roots for `SOURCE`, `DERIVED`, and `AUDIT`. Relative paths are normalized and path traversal outside the endpoint root is rejected.

Durable immutable objects use:

```text
sha256:<64 lowercase hex digits>
```

CAS write is idempotent: bytes with the same digest map to the same object. Existing bytes are verified before reuse. Host filesystem layout is not part of Genesis object identity.

Recommended BLACKGLASS precedence remains:

```text
irreplaceable source > durable persistent state > rebuildable indexes > scratch
```
