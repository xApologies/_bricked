# BLACKGLASS Interface

BLACKGLASS is the operations base/mainframe host. It is not BRANE and it is not the Genesis language.

Section 17 models the durable state boundary as:

```text
execution-derived state
  -> commit proposal
  -> validation / authority check
  -> admit
  -> durable object reference
```

Direct persistent mutation is unavailable in the semantic interface. This mirrors the source-derived state-plane rule:

```text
Modules compute.
Heart persists.
BRANE realizes.
Rainbow Road transports.
```

The reference Heart stores admitted payloads by immutable CAS reference and records proposal/admission receipts. BLACKGLASS 3.0 may change the concrete persistence engine without changing this semantic ABI.
