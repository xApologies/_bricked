# Reference implementation

Package: `genesis_semantics`

Bootstrap commands:

```bash
python -m genesis_semantics check bundle.json
python -m genesis_semantics link bundle.json -o program.gvm
```

The package vendors the current Section 08 `genesis_vm` implementation under `genesis_semantics.vendor.genesis_vm` so the Section 09 core ZIP is runnable by itself.
