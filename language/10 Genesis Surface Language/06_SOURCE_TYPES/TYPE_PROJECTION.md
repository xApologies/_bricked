# Source type projection

Source annotations use Section 09 refined type syntax on interfaces. Node result declarations lower to the stable Section 08 coarse VM type tag.

Examples:

```text
source export                         node/GVM type
GEOMETRIC<CLOSED,QFT>       ->        GEOMETRIC
PORTAL<GR,OPEN>              ->        PORTAL
QSTATE<OWNED>                ->        QSTATE
RECEIPT<PORTAL_CLOSE>        ->        RECEIPT
```

This keeps source interfaces expressive without teaching the Section 08 bytecode encoder a second parametric type grammar.
