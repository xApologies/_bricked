# QFT/GR Common-Ancestry Relation

Source formalism:

```text
R_QG = { (q,g) | exists F: q = rho_Q(F), g = rho_G(F) }
```

Runtime representation:

```text
R_QG(q,g) is admitted when:
  q.sector == QFT
  g.sector == GR
  q.fabric_witness_id == g.fabric_witness_id
  canonical MMO identity agrees
  required invariant roots agree
  provenance policy passes
```

The relation is symmetric as a correspondence relation in this software layer. The actual transformation maps used to create/read each sector remain directionally typed.
