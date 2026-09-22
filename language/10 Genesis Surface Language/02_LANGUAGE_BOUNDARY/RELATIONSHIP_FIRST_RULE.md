# Relationship-first rule

Genesis source should make relationships and state transitions visible rather than burying them inside object-method syntax.

Preferred:

```genesis
rel g0 -> "environment://trinity" as r
portal GR g0 with adm as p corridor "Red->Violet"
ve g0 through p -> "trinity://node-B" as g1
tor p with g1 as receipt
```

Not the native canonical projection:

```text
g0.portal(GR).send(nodeB).close()
```

The canonical form exposes source, relation/route, destination, and closure as separate graph-producing statements.
