# Reference implementation

New packages:

```text
genesis_callables/
  parser.py       extended module/function/usefn parser
  expander.py     visibility resolution, recursion check, monomorphization, alpha-renaming
  compiler.py     callable frontend + proof receipts + Section 10 handoff
  model.py        callable AST and receipt records
  errors.py       explicit diagnostics

genesis_callable_packages/
  runtime.py      Section 12 package runtime extended for callable modules
```

The pre-existing Section 12 reference packages are vendored beside these modules so Part A is a self-contained reference implementation.

Run tests:

```text
PYTHONPATH=12_REFERENCE_IMPLEMENTATION python 15_TESTS/test_section13.py
```
