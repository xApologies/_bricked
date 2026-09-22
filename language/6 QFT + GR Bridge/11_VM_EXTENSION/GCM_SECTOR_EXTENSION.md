# Genesis Chirality Machine — Sector Extension

Provisional machine-level semantic operations:

```text
READ_QFT_VIEW instance,address -> rep
READ_GR_VIEW  instance,address -> rep
BRIDGE_QG     qft_view -> gr_view  [via common fabric witness]
BRIDGE_GQ     gr_view  -> qft_view [via common fabric witness]
ASSERT_ANCESTRY rep_a,rep_b
EMIT_BRIDGE_RECEIPT
```

These are Layer-Zero/VM semantic operations. They are not proposed CPU opcodes and do not replace the Section-01 Hardware ABI.
