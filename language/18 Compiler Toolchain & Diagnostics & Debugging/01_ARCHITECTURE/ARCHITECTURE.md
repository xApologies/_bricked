# Section 18 architecture

```text
.gen source
   │
   ├── source index ───────────────► stable spans / source map
   │
   ▼
Section 17 parser/compiler/verifier
   │                     │
   │ failure             └──► structured diagnostic
   ▼
verified SystemProgram
   │
   ├── deterministic build manifest
   ├── encoded .gio
   ├── disassembly
   ├── verification proof
   └── source map
   │
   ▼
Tracing runtime
   │
   ├── instruction events
   ├── boundary receipts
   ├── register snapshots
   └── provenance root
   │
   ▼
Replay debugger / test runner / build comparison
```

The Section 17 verifier remains authoritative. Section 18 has no "force" mode.
