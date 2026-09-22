# Proof ledger format

Each obligation records:

```json
{
  "id": "PO-TYPE-SAFETY",
  "status": "PASS",
  "witness": {"checked_nodes": 12, "refined_values": 11},
  "ruleset": "section09-v0.1.0"
}
```

Failed obligations carry diagnostics and prevent emission of a linked executable.
