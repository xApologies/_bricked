# Genesis Chirality Machine — Section 04
## Portal Transaction Engine + Corridor Admission

Version `0.1.0` — implementation layer.

Section 04 makes information transportation executable. Sections 01–03 established the immutable chirality fabric, Geometric/MMO instantiation, and immutable transformation forks. Section 04 adds a first-class Portal transaction and a Corridor admission/routing engine.

### Core law

```text
Corridor = mathematically admissible route.
Portal   = one typed information-transfer transaction over a Corridor.
```

A successful Portal does not mutate its source Geometric. It re-realizes the selected closed information state at a destination fabric region, emits a route witness, preserves the declared invariant residue, and closes with a hash-chained receipt.

### Execution path

```text
closed source Geometric
    -> source address
    -> payload characterization
    -> Corridor search
    -> preservation/admission checks
    -> route-capacity reservation
    -> destination-region reservation
    -> Portal OPEN
    -> chirality-conditioned transport/re-realization
    -> ARRIVAL verification
    -> target closure
    -> destination Geometric
    -> BRANE M^5 re-lift
    -> Portal CLOSED receipt
```

### Recovery

Part A is the implementation core. Part B contains real fixture transactions. Parts C/D contain lineage and mathematical source capsules. Mount Section 01–03 before this package when reconstructing the full implementation chain.
