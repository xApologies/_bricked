# Reference execution loop

```text
verify bytecode
initialize frame + register file
mount backend
while PC < instruction_count:
    decode instruction
    fetch typed arguments
    enforce dynamic typestate / linear rules
    dispatch semantic opcode to backend
    store typed result
    append backend receipts/provenance
    update PC/control flow
halt only when transaction closure invariants are satisfied
emit execution receipt
```

The backend is not allowed to redefine opcode meaning. It realizes the contract for a target execution environment.
