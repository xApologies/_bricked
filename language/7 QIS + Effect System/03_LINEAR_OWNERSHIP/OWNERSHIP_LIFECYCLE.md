# Ownership lifecycle

```text
ALLOCATED -> OWNED -> MOVED -> OWNED
                    -> MEASURED -> CLASSICAL_RESULT + POST_MEASURE_STATE
                    -> CONSUMED

OWNED --borrow_metadata--> OWNED
OWNED --clone--> ERROR
```

The registry is deterministic and auditable. An ownership receipt records old owner, new owner, state ID, operation, and timestamp.
