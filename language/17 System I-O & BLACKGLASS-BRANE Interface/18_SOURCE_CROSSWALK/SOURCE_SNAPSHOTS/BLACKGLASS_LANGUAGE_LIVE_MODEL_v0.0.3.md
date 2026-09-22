# BLACKGLASS Programming Language — Live Model v0.0.3

Status: ACTIVE DESIGN / CHIRALITY-ATOMIC INGEST COMPLETE
Lead development: Astraeus
Audit / continuity: Vera
Bootstrap implementation: Python

## Prime design stance

BLACKGLASS is a chirality-native configuration-space language. Chirality is not a Boolean decoration and not merely left/right orientation. It participates in admissibility: which arrangements and transitions are structurally allowed.

The first implementation remains a Python reference interpreter, but Python object semantics are not language canon.

## Current semantic kernel

A runtime state must be able to represent at least:

- environment / boundary context
- occupancy / adjacency
- chirality / admissibility
- ancestry / inheritance
- persistence / recoverability
- Resolution (distinguishable organization)
- Bandwidth (available organizational freedom)
- closure / normalization state
- extensible structural channels
- provenance / transformation trace

## Runtime operator family

Nominal constructive evolution:

`inherit -> propagate -> stabilize -> redistribute -> close -> normalize`

Failure/divergence branch:

`destabilize`

Recovered operator spellings remain:

- `.·` inherit
- `··` propagate
- `.°.` stabilize
- `.·· .°` redistribute
- `··° ·°` destabilize
- `·°·` close
- `■ .· ■` normalize

Exact final parser syntax remains open pending the next authoritative dot-notation source.

## Equation layer — semantic candidates

Prime observation/evolution form:

`Psi_(n+1) = Chi(Psi_n tensor T) compose R_c`

Interpretation for language design: transform a current continuity/configuration state through inherited coupling, chirality-aware redistribution, and recoverable closure to produce a descendant state.

Additional recovered forms:

- `M_u = (chi_R tensor chi_L) compose A`
- `M_(n+1) = Chi(M_n tensor T)`
- `C = (M_u compose R) equivalent M_s`
- `P = (chi_R compose B_c)`
- `M_c equivalent (chi_R tensor chi_L) -> A`

These are not yet grammar productions. They are semantic/operator constraints to be tested in the reference interpreter.

## 3 + 1 + 1 substrate contract

The ER-foam source makes the semantic dimensional contract explicit:

- `x,y,z` = occupancy-adjacency structure
- `c` = chirality ordering
- `p` = recursive persistence / inheritance

Reference tensor: `(operator, x, y, z, chirality, persistence)` with seed shape `(7,2,2,2,2,2)`.

Critical implementation distinction: **array rank is not ontology**. The operator axis is a grammar/channel axis, not one of the 3+1+1 dimensions. Atomic fixtures use source/set-lift arrays with channel axes and carry history partly through pipeline/ancestry records. The language must distinguish semantic dimensions from storage layout.

## T-domain capability model (Pipeline 1)

Active recovered T0-T7 roles:

- T0: chirality memory substrate / compressed ancestry
- T1: chirality admissibility amplification
- T2: adjacency geometry routing
- T3: propagation topology reinforcement
- T4: knot-admissibility / weak persistence asymmetry
- T5: bounded shell redistribution / proto-material dynamics
- T6: dynamic continuity ecology / coupling preparation
- T7: closure equilibrium / coupling-ready writeout

Pipeline 1 is the topology-genesis side and may have read-write chirality access.

## R-domain capability model (Pipeline 2 — later audited branch)

- R0: continuity initialization / ecology entry
- R1: propagation / interaction-surface transport
- R2: controlled occupancy/continuity redistribution
- R3: proto-interaction awareness / persistent coupling ecology
- R4: corridor formation / elastic coupling
- R5: ordered topology resolution / constrained topology collapse
- R6: constrained survivability stabilization
- R7: oscillatory persistence / ecology-readiness exposure

Pipeline 2 is read-only with respect to chirality and existence/non-existence occupancy. It may write ecology, exposure, adaptation, arbitration, closure, and audit records.

This strongly suggests a language-level **capability/effect system** rather than relying on convention:

- a `T` context may carry `chirality: write` capability where allowed;
- an `R` context carries `chirality: read`;
- illegal mutation should fail before/at evaluation as an admissibility violation.

## Manifold/object versus environment rule

A recurring source lock is:

- manifold = topology identity state/object
- pipeline = environmental continuity domain

The object should not be mutated merely to make it fit a domain. The domain supplies constraints; the manifold responds.

Programming-language consequence: distinguish **state data** from **evaluation environment** in the core type/effect model.

## Channel/schema rule

Recovered fixtures show:

- blank manifold: 11 channels
- hydrogen v2: 13 channels
- oxygen Phase 5: 31 channels

Therefore fixed channel count is not language canon. Structural channels need an explicit extensible schema with adapters/versioning.

A direct interface mismatch exists between Pipeline 2 v0.4's stated 11-channel accepted primary shape and later H/O fixtures with 13/31 channels. Do not hide this with implicit truncation or padding. Require a declared adapter/schema transform.

## Chirality/set-lift storage observations

- Blank chirality statecode is a balanced 0/1 checkerboard over 32^3.
- Blank source and set-lift tensors are zero-populated scaffolds.
- Hydrogen uses `(13,32,32,32)` source projection and `(13,32,32,32,2)` right/left set-lift.
- Oxygen uses `(31,32,32,32)` and `(31,32,32,32,2)` with a ±1 chirality field.

These are fixtures, not mandatory language dimensions or resolutions.

## Observer/intelligence separation

Runtime transformation and observer/intelligence interpretation remain distinct:

Runtime: `inherit, propagate, stabilize, redistribute, destabilize, close, normalize`

Observer/intelligence: `observe, distinguish, relate, predict, resolve, remember, learn`

The interpreter kernel should first implement runtime transformation. Observer/intelligence can later be a reflective/meta layer over runtime state and provenance.

## Explicit unresolved semantic gates

### Gate S0 — set-state ontology conflict

Sources disagree in wording around `∅` and `{∅}`:

- chirality recovery material: `∅` = no structure / does not exist; `{∅}` = structure exists
- quantum-wave equation material: `empty-set` = distinguishable existence state; `empty-set-containing-empty-set` = unresolved recursive potential

Do not reconcile by assumption. Lock exact source chronology/meaning before the language assigns primitive literals.

### Gate P2 — Pipeline 2 branch drift

An earlier/stale README describes R4-R7 as disturbance/adaptation/arbitration/closure. Later completion lock and canonical audits explicitly lock R4 corridor formation, R5 ordered resolution, R6 survivability, R7 oscillatory persistence. Use the later audited branch for active semantics; retain the earlier wording as provenance.

### Gate CH — channel schema mismatch

Pipeline 2 v0.4 accepts 11-channel primary shapes, while H and O fixtures expose 13 and 31 channels. A typed schema/adapter contract is required before these become executable fixtures.

## What is deliberately not promoted

The following remain reference/test material rather than language axioms:

- specific hydrogen/oxygen chemistry behavior
- particle interpretations or claims of validated atomic physics
- fixed 32^3 resolution
- fixed voltage mappings
- element-specific output expectations
- gravity/dark-matter interpretations

They may be excellent integration tests without defining the language.

## Next executable design gates

1. Define `State`, `Environment`, `Boundary`, `ChannelSchema`, and `Ancestry` data contracts.
2. Define chirality value/orientation/admissibility algebra without resolving Gate S0 prematurely.
3. Define operator effect signatures for all seven runtime primitives.
4. Define T/R domain capabilities and mutation guards.
5. Define closure/recoverability invariants and an explicit transformation trace.
6. Define schema adapters for 11/13/31-channel fixtures.
7. Build the first Python semantic kernel and tests.
8. Only then lock surface syntax.
