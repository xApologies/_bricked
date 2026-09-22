# Refined type model

Section 08 exposes coarse VM tags such as `GEOMETRIC`, `PORTAL`, `QSTATE`, and `RECEIPT`. Section 09 overlays static refinements that are erased to those coarse tags when lowering to GVM.

Examples:

```text
GEOMETRIC<CLOSED,UNBOUND>
GEOMETRIC<CLOSED,QFT>
GEOMETRIC<CLOSED,GR>
PORTAL<QFT,OPEN>
PORTAL<GR,CLOSED>
ROAD<OPEN>
QSTATE<OWNED>
QSTATE<MOVED>
QRESULT<CLASSICAL>
BRIDGE<QFT,GR>
RECEIPT<PORTAL_CLOSE>
M5
```

A declaration may intentionally be coarse:

```text
GEOMETRIC
PORTAL
RECEIPT
```

A coarse declaration accepts a compatible refined instance. Thus `GEOMETRIC` can describe `GEOMETRIC<CLOSED,QFT>`, while `GEOMETRIC<CLOSED,GR>` does not accept a QFT Geometric.

These refinements are static semantics. The GVM still uses the stable Section 08 type tags.
