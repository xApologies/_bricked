# Geometric Instance State Machine

```text
REGISTERED
   -> PLANNED
   -> RESERVED
   -> MATERIALIZING
   -> VERIFYING
   -> COMMITTED
   -> LIVE
   -> QUIESCED
   -> RELEASED
```

Failure from any pre-commit state -> `ABORTED`.

Transformation of LIVE state does not rewrite the committed parent. It creates:

`LIVE(parent) -> FORKED(child) -> child segment/delta -> LIVE(child)`

## Commit gate

COMMITTED requires:

- source hash verification;
- representation shape/schema verification;
- region reservation ownership;
- complete segment write;
- payload hash verification;
- address-bound checks;
- sample or full readback policy pass;
- receipt generation.
