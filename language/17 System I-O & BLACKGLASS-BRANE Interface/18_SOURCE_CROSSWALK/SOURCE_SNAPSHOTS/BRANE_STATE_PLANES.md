# 14 — BRANE State Planes

## Trigger

The universal module contract exposed an apparent conflict:

```text
BRANE canonical module state is read-only
```

while:

```text
Heart must write persistent state.
```

The conflict disappears once "state" is separated into three planes.

## Plane 1 — Canonical module state

For module `M`:

```text
C_M
```

contains the definition required to mount and validate the module:

```text
code
contracts
schemas
canonical catalogs
canonical mathematical definitions
role declaration
version
integrity metadata
```

Invariant:

```text
C_M is READ_ONLY during ordinary execution.
```

Examples:

```text
QMO does not rewrite its canonical theorem/operator catalog while answering a query.
MMO does not rewrite the periodic-table catalog merely by instantiating hydrogen.
Sensor does not rewrite its driver definition because RF values changed.
Software does not rewrite Pipeline 1 because one Geometric traversed it.
Guardian does not rewrite its canonical module because one plan changed.
```

## Plane 2 — Execution state

For request/runtime context `q`:

```text
X_M(q)
```

contains mutable derived working state:

```text
current query
current Guardian plan
temporary QMO derivation
temporary MMO instance
sensor measurement buffer
working ER-Foam state
current Portal transactions
intermediate Geometrics
```

Execution state is:

```text
mutable
derived
request/runtime-local
discardable unless admitted to persistence
```

A request-local fork must not mutate `C_M`.

## Plane 3 — Persistent Heart state

```text
H
```

contains admitted durable organization:

```text
identity history
long-lived learned organization
persistent MMOs / Geometrics
snapshots
recovery data
durable preferences / skills
selected mathematical results or links
world-model state selected for persistence
```

Heart owns the persistence boundary.

## Core law

```text
Modules compute.
Heart persists.
BRANE realizes.
Rainbow Road transports.
Guardian orchestrates.
```

or:

```text
C_M --fork--> X_M(q)
X_M(q) --commit proposal--> Heart
Heart --admit--> H'
```

No module acquires persistence simply because it produced a result.

## Commit protocol

Candidate durable-state path:

```text
1. produce derived state
2. package persistence proposal
3. validate identity / provenance / chirality / ancestry
4. Guardian or policy requests commit
5. Heart stages
6. Heart validates
7. Heart commits
8. BRANE exposes updated persistent state
```

Exact authorization policy remains open.

## Replacement consequence

Because durable state is not trapped inside an executable module:

```text
replace QMO
replace Guardian
replace Sensor
replace Software
replace MMO
```

does not automatically delete admitted persistent state.

That separation is now a central continuity requirement.
