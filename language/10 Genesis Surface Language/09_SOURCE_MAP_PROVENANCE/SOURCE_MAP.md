# Source map and provenance

Each GIR node receives a source-map record:

```json
{
  "node": "004_portal_open",
  "file": "FIRST_PORTAL.gen",
  "line": 9,
  "surface": "portal GR g1 with adm as p corridor ..."
}
```

The frontend receipt hashes normalized source, AST, lowered modules, linked GIR, and emitted GVM. This gives BLACKGLASS a deterministic chain from textual projection back to executable relationship graph.
