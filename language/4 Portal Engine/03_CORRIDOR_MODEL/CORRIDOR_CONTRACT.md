# Corridor Contract

A software Corridor edge is an admitted local segment carrying the minimum data required to test the working mathematics.

```text
CorridorEdge {
  source_domain
  target_domain
  sectors
  chirality_classes
  residue_classes
  resolution
  bandwidth
  capacity
  cost
  color_index
  closure_supported
}
```

A path `W = (e1,...,en)` is admissible only if every edge satisfies the request and capacity constraints.

### Path-level conditions

* continuation: edge endpoints compose;
* chirality: every edge admits the payload chirality class;
* identity: Portal preservation contract keeps required identity fields;
* invariant residue: residue class and computed residue root remain allowed;
* Resolution: `min(edge.resolution) >= R_min`;
* Bandwidth: `min(edge.bandwidth) >= B_min` and available capacity is sufficient;
* closure: final edge and target domain support requested closure;
* sector: all edges support the Portal sector unless an explicit bridge is declared.

The path planner returns a witness with every intermediate domain and edge. Composition into Rainbow Road is intentionally deferred to Section 05.
