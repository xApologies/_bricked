# Partial Failure Semantics

Road execution is append-only.

If Portal `k` fails after `k-1` legs closed:

```text
Road.status = FAILED_PARTIAL
completion_frontier = target_(k-1)
closed_portals = [P1,...,P(k-1)]
failed_leg = k
```

The implementation:

* retains every closed destination Geometric;
* retains every closed Portal receipt;
* emits a Road failure receipt;
* releases the Road-level Bus lease;
* does not pretend that already-observed history never occurred.

A later recovery workflow may intentionally continue from the completion frontier as a new Road run.
