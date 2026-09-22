# Static effect system

Effects inherited from the Section 08 machine contract:

`READ_FABRIC`, `WRITE_OVERLAY`, `ALLOCATE`, `RELATE`, `ADMIT`, `TRANSFORM`, `TRANSPORT`, `CLOSE`, `INHERIT`, `PROJECT`, `TRANSDUCE`, `MEASURE`, `QUANTUM_LINEAR`, `PROVENANCE`, `CONTROL`.

A semantic module may declare:

```json
"effects": ["ALLOCATE", "INHERIT", "READ_FABRIC"]
```

The checker computes actual effects from contained operations and requires:

```text
actual_effects(module) subset_of declared_effect_budget(module)
```

Omitting `effects` means the module is unconstrained by a local budget during bootstrap; linked production bundles should declare budgets.

Effects are authority boundaries. Linking does not cause Module A to inherit Module B's permissions.
