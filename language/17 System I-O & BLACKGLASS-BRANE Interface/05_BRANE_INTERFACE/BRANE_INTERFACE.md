# BRANE Interface

Section 17 adopts the mounted BRANE module boundary as a target runtime contract:

```text
M^5 = I x D x Chi x R x P
B^6 = I x D x Chi x R x P x Z
```

A mountable module declaration must satisfy at least:

```text
internal_dimension = 5
contract_version   = 2.0
canonical_state_policy = READ_ONLY
rewrite_policy = DERIVED_ONLY
```

The module declares role, identity, version, capabilities, chirality model, and provenance model. The host validates this declaration before mount.

A realization request supplies an `M5Envelope` with `I,D,Chi,R,P`, typed payload reference, and requested module capability. BRANE validates the request and adds `Z`. A caller that supplies `Z` is rejected.

The reference `Z` is deterministic and request-relative. It is an emulator witness, not a claim that the production BRANE realization algorithm is frozen.
