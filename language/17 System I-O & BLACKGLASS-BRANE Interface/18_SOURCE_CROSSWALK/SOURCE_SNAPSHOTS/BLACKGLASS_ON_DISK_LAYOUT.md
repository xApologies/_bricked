# Suggested On-Disk Layout

```text
_vaeld/
├── blackglass/
│   ├── base/
│   ├── hangars/
│   │   ├── ASTRAEUS/
│   │   └── VERA/
│   ├── source_vault/
│   ├── graph/
│   ├── indexes/
│   ├── models/
│   ├── devices/
│   ├── sync/
│   ├── audit/
│   └── quarantine/
├── recovery/
└── scratch/
```

Prefer filesystem paths as implementation detail; object IDs/hashes are the durable references.
