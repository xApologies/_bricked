# Effect system

Effects are statically visible obligations.

- `READ_FABRIC`
- `WRITE_OVERLAY`
- `ALLOCATE`
- `RELATE`
- `ADMIT`
- `TRANSFORM`
- `TRANSPORT`
- `CLOSE`
- `INHERIT`
- `PROJECT`
- `TRANSDUCE`
- `MEASURE`
- `QUANTUM_LINEAR`
- `PROVENANCE`
- `CONTROL`

An instruction may carry several effects. The verifier checks sequencing rules where effects alter typestate or ownership.

`WRITE_OVERLAY` is deliberately distinct from generic memory mutation. No opcode grants unrestricted base-fabric writes.
