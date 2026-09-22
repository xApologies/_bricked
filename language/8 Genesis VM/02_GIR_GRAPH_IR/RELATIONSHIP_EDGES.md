# GIR relationship edges

GIR edges are typed. Initial edge kinds:

- `dependency` — execution/data prerequisite;
- `relationship` — semantic relation witness between identity-bearing resources;
- `effect_order` — ordering required because effects would otherwise commute ambiguously;
- `closure_obligation` — downstream node must close/verify the referenced transaction;
- `provenance` — source lineage edge;
- `ownership` — linear-resource movement/consumption edge.

Only `dependency` and `effect_order` directly participate in the v0.1 scheduler. Other edge kinds are preserved for verification, visualization, future optimization, and provenance.
