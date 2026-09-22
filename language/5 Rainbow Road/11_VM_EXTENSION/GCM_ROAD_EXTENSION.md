# Genesis Chirality Machine — Road Extension

Section 01 reserved Portal-level VM concepts. Section 05 defines Road-level reference semantics above those opcodes:

```text
RDECLARE   declare Road template/request
RPREFLIGHT resolve all Portal/Corridor legs
RBUS_HOLD  reserve Rainbow Bus capacity lease
RSTEP      execute one closed Portal leg
RAUDIT     run end-to-end invariant audit
RCLOSE     emit Road closure receipt
RFAIL      emit FAILED / FAILED_PARTIAL receipt
RRECEIPT   append hash-chained Road ledger entry
```

These are virtual-machine semantics, not a claim that current x86 hardware implements chirality-native opcodes.
