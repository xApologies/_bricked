# Reference implementation

`genesis_vm` is a zero-third-party-dependency Python bootstrap implementation of GIR compilation, GVM verification, bytecode encoding/decoding, and a deterministic semantic reference backend.

It intentionally models backend resources abstractly. It proves the execution contract can be exercised before binding every opcode directly into the larger Section 01–07 Python packages.

Run:

```bash
python -m unittest discover -s ../../17_TESTS -p 'test_*.py' -v
```
