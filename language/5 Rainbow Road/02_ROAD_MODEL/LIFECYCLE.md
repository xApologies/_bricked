# Road Lifecycle

```text
DECLARED
  -> PREFLIGHTED
  -> BUS_RESERVED
  -> RUNNING
  -> LEG_CLOSED [repeats]
  -> END_TO_END_AUDIT
  -> CLOSED
  -> INHERITED
```

Terminal failure states:

* `FAILED` — no Portal leg closed;
* `FAILED_PARTIAL` — one or more Portal legs closed before failure.

No terminal state implies deletion of already-closed Portal history.
