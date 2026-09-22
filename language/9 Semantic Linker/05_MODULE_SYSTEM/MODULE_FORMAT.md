# GIR semantic module format

```json
{
  "ir": "GIR-MODULE",
  "module": "transport",
  "version": "0.1.0",
  "effects": ["ADMIT", "TRANSPORT", "CLOSE", "PROVENANCE"],
  "imports": [
    {"local": "%source", "from": "fixture", "symbol": "geo", "type": "GEOMETRIC"}
  ],
  "exports": [
    {"symbol": "destination", "value": "%g1", "type": "GEOMETRIC<CLOSED,QFT>"}
  ],
  "gir": {
    "nodes": [],
    "edges": []
  }
}
```

Imports are **typed symbolic edges**, not textual inclusion. Exports name values that remain traceable to their module-local producer.
