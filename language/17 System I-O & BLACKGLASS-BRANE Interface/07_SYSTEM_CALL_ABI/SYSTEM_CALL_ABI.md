# System Call ABI

Section 17 reserves GVM system opcode window `0x00B0..0x00BB`:

```text
0x00B0 READ
0x00B1 WRITE_DERIVED
0x00B2 APPEND_AUDIT
0x00B3 CAS_PUT
0x00B4 CAS_GET
0x00B5 BRANE_MOUNT
0x00B6 BRANE_REALIZE
0x00B7 BLACKGLASS_PROPOSE
0x00B8 BLACKGLASS_ADMIT
0x00B9 DEVICE_REQUEST
0x00BA ASSERT_EQ
0x00BB SYS_CLOSE
```

These are semantic system operations. A native backend may lower them to OS/filesystem/database/driver calls, IPC, a BRANE service boundary, or custom hardware services.

Each operation emits a deterministic `BoundaryReceipt` or a typed failure witness.
