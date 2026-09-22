# BRANE M^5 Adapter

Section 02 emits an organizational descriptor:

```json
{
  "I": {...},
  "D": {...},
  "Chi": {...},
  "R": {...},
  "P": {...}
}
```

No `Z` field is emitted.

## Mapping

- **I**: canonical MMO id, MMO version, instance id, representation id, invariant digest.
- **D**: dependency closure ids/hashes, source representation dependencies, parent instance if any.
- **Chi**: fabric tag, region, segment hash, mapping profile, chirality summary/readiness.
- **R**: recursive depth/context, history chain, parent/child lineage, closure state.
- **P**: source archive hashes, adapter version, instantiation receipts, provenance classes.

BRANE consumes M^5 and supplies request-relative realization **Z**.

### Non-equivalence guard

Scientific `(X,Y,Z,2,2)` data is not unpacked as `(I,D,Chi,R,P)`. M^5 is metadata/organizational adaptation around the scientific representation.
