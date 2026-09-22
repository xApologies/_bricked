# Surface examples

```genesis
genesis 0.1.0
module first_portal {
  en fabric : FABRIC = mount "fabric://chirality/reference-v1"
  en region : REGION = alloc fabric cells 4096
  en g0 : GEOMETRIC = instantiate fabric region mmo @hydrogen_reference
  rel g0 -> "environment://trinity" as relation
  admit g0 as adm @{"admitted":true,"bandwidth":1.0,"resolution":1.0}
  transform g0 with adm as g1 @{"kind":"identity-preserving-reference-transform"}
  portal GR g1 with adm as p corridor "corridor://red-violet"
  ve g1 through p -> "trinity://node-B" as g2
  tor p with g2 as portal_receipt
  lift g2 as m5 @{"P":"receipt-ledger","R":"closed"}
  export g2 : GEOMETRIC<CLOSED,GR>
  export portal_receipt : RECEIPT<PORTAL_CLOSE>
  export m5 : M5
}
```
