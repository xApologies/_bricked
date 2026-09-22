# Portal Lifecycle

```text
DECLARED
  -> VALIDATED
  -> CAPACITY_RESERVED
  -> DESTINATION_RESERVED
  -> OPEN
  -> TRANSFERRING
  -> ARRIVED
  -> CLOSED
  -> INHERITED
```

Failure from any pre-close state resolves to `FAILED` plus a failure receipt. Uncommitted route/destination reservations are released or aborted.

`CLOSED` means the destination state was independently re-read, the requested target address was satisfied, preservation checks passed, and provenance includes the complete route witness.
