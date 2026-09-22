# Reference frontend

Package: `genesis_frontend`

Self-contained bootstrap usage from this directory:

```bash
python -m genesis_frontend parse ../../16_EXAMPLES/FIRST_PORTAL.gen
python -m genesis_frontend lower ../../16_EXAMPLES/FIRST_PORTAL.gen
python -m genesis_frontend build ../../16_EXAMPLES/FIRST_PORTAL.gen -o first_portal.gvm
python -m genesis_frontend run ../../16_EXAMPLES/FIRST_PORTAL.gen
```

The package vendors Section 09 `genesis_semantics`, which in turn vendors the Section 08 `genesis_vm` reference runtime.
