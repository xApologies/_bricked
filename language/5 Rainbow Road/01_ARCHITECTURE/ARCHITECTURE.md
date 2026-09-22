# Rainbow Road Architecture

## Why Road is a first-class object

A Portal answers: **can this information cross this boundary now?**

A Rainbow Road answers: **can a persistent identity traverse an ordered family of independently closed boundary crossings while remaining recoverable end-to-end?**

The Road therefore owns composition semantics that a Portal does not:

* ordered Portal ancestry;
* waypoint continuity;
* end-to-end preservation obligations;
* Road-level capacity lease;
* combined Resolution/Bandwidth envelope;
* combined chirality/color trajectory;
* transport-holonomy witness;
* partial-failure history;
* Road identity and reusable Road plan registry.

## Runtime stack

```text
MMO / Geometric
   |
   v
RainbowRoadRequest
   |
   v
Road Composer / Preflight
   |         \
   |          -> Corridor plan per Portal leg
   v
Rainbow Bus Capacity Manager
   |
   v
Section-04 Portal Engine
   |
   +--> closed intermediate Geometric --+
   |                                      |
   +--------------------------------------+
   |
   v
End-to-End Closure Auditor
   |
   v
RainbowRoadReceipt + final BRANE M^5 inheritance
```

## Road execution is not a software rollback transaction

This implementation intentionally refuses destructive rollback. A committed Portal creates a new immutable Geometric and a closure receipt. If a downstream leg fails, those objects remain valid history. Road status becomes `FAILED_PARTIAL` and reports the exact completion frontier.
