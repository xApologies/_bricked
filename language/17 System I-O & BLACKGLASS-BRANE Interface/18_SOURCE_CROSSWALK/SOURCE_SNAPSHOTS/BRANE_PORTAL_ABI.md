# 15 — BRANE Portal ABI

## Status

**v0.6 NEXT HANDLE / ACTIVE CANDIDATE CONTRACT**

Rainbow Road is BRANE-owned transport infrastructure.

The object crossing it is a **Portal transaction**.

The Portal ABI binds the pre-existing Portal vocabulary to the BRANE five-to-six-dimensional embedding rule.

## Principle

A source module supplies a five-coordinate transaction description.

BRANE validates, routes, and realizes it.

The source module does **not** assign `Z`.

## Pre-realization Portal envelope

Candidate normalized form:

```text
Portal5
{
    transaction_id

    source_module
    source_address

    target_module
    target_address

    payload_type
    payload_ref
    payload_fingerprint

    I  identity
    D  dependency
    Χ  chirality / admissibility
    R  recursive context
    P  provenance

    resolution_required
    bandwidth_required

    persistence_intent
    preservation_contract
    invariant_residue
    ancestry

    closure_target
    failure_policy

    route_constraints
}
```

Compactly:

```text
P_ij^5
=
(
    payload;
    source,
    target;
    I,D,Χ,R,P;
    Resolution,
    Bandwidth;
    preservation,
    ancestry,
    closure
)
```

## BRANE realization

If admissible:

```text
BRANE.validate(P_ij^5) = PASS
```

BRANE selects an admitted Corridor / Rainbow Road and produces an execution realization:

```text
P_ij^6
=
ι_BRANE(P_ij^5)
=
(P_ij^5, Z)
```

`Z` belongs to realized execution, not to the module-owned envelope.

## Realization receipt

Candidate receipt:

```text
PortalReceipt6
{
    transaction_id
    route_id
    corridor_id
    portal_sequence

    source_fingerprint
    target_fingerprint
    payload_fingerprint

    realization_Z

    admitted_resolution
    admitted_bandwidth

    preservation_result
    closure_result

    status
    failure_reason

    provenance
    timestamp_or_sequence
}
```

The timestamp is operational metadata and is not automatically the identity of `Z`.

## Payload rule

Portal payloads are typed objects, not unstructured byte blobs at the architecture level.

Possible payload classes include:

```text
QMO object / derivation
MMO object / molecular profile
Geometric
sensor percept
Guardian request
Software result
Heart commit proposal
Heart read result
health / diagnostic record
```

Binary serialization may exist underneath, but BRANE reasons over the typed envelope.

## Heart write rule

A peer module cannot write Heart directly.

A durable write is represented as a Portal whose target is the Heart/Library role and whose payload includes:

```text
persistence_intent = COMMIT_PROPOSAL
```

Heart then applies its own staging/validation/commit contract.

## Sensor rule

Sensor Fabric emits perceptual/measurement Portals.

It cannot mutate Guardian, Software, QMO, MMO, or Heart by memory reference.

## QMO/MMO rule

QMO and MMO may cooperate through BRANE:

```text
QMO -> Portal -> Software
MMO -> Portal -> Software
Software -> Portal -> QMO/MMO/Guardian
```

but neither API directly rewrites the other.

## Failure atomicity

Candidate transport invariant:

```text
failed Portal != partial cross-module mutation
```

A failure must result in:

```text
REJECT
ROLLBACK
QUARANTINE
RETRYABLE_FAILURE
UNRESOLVED
```

with explicit provenance.

## Route vocabulary

Preserve:

```text
Rainbow Bus  = transport capacity / fabric
Corridor     = admissible route
Portal       = one transfer transaction
Rainbow Road = persistent composed route
```

The Portal ABI defines the transaction layer; it does not replace Corridor/Road mathematics.
