# GCM Portal Extension

Section 01 reserved the opcodes:

```text
POPEN  0x30
PXFER  0x31
PCLOSE 0x32
RECEIPT 0x33
```

Section 04 supplies their first executable reference semantics:

* `POPEN`: validate Portal plan, reserve Corridor capacity and destination region.
* `PXFER`: stream the source logical Geometric through the admitted route contract into destination re-realization.
* `PCLOSE`: read back destination, validate invariants/target, commit destination region, release route reservation.
* `RECEIPT`: emit/hash-chain the Portal closure or failure receipt.

These are virtual-machine semantics. They do not prescribe a future physical electrical protocol.
