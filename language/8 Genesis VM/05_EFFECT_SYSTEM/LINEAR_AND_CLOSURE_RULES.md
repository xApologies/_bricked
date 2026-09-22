# Linear and closure rules

## Linear quantum state

A QSTATE starts `OWNED`. Operations may move it, transform it into a successor, entangle it into a joint successor, or consume it through measurement. A consumed/moved source cannot be used again as if it remained independently owned.

## Portal closure

`PORTAL_OPEN` produces an open Portal. A transport may occur only through an admitted/open Portal. `PORTAL_CLOSE` emits a closure receipt. An open Portal live at `HALT` is a verifier/runtime error unless the program explicitly declares a failure/partial frontier.

## Road closure

A Road may accumulate independently closed Portal receipts. `ROAD_CLOSE` emits an end-to-end closure receipt. Partial execution is preserved as history rather than destructively rolled back.
