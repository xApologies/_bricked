# Transformation Fork

A live Geometric is persistent history, not mutable anonymous memory.

```text
parent instance
    -> transformation request
    -> child plan
    -> delta/child segment
    -> invariant checks
    -> closure receipt
    -> child instance
```

The parent remains readable and hash-stable. This provides the object-level basis for later Portal transformation/transport history.
