# Section 04 Architecture

## Purpose

The Portal Engine is the boundary between *state transformation* and *state transportation*. A Transformation changes a Geometric's organization while keeping it at the same fabric region. A Portal transports/re-realizes a closed Geometric state at another relational address and physical fabric region.

## Layered architecture

```text
Geometric / MMO
  current closed state
        |
        v
Payload Characterizer
  structural root / invariant residue / chirality envelope
        |
        v
Corridor Admission Engine
  source + target + sector + R/B + chirality + closure constraints
        |
        v
Route Planner
  admissible path witness W = e1...en
        |
        v
Capacity Reservation
        |
        v
Portal Transaction State Machine
 DECLARED -> VALIDATED -> RESERVED -> OPEN -> TRANSFERRING
          -> ARRIVED -> CLOSED -> INHERITED
        |
        v
Destination Re-realization
  immutable .gos segment in a new fabric region
        |
        v
Closure + Receipt + BRANE M^5 re-lift
```

## Scope

Section 04 implements *one Portal transaction*. Persistent multi-Portal Rainbow Road composition is Section 05. QFT/GR bridge execution is typed here by sector but full cross-sector transduction is deferred to its dedicated section.

## Source mathematics preserved

The implementation operationalizes the working Corridor definition:

```text
C_ab = Pi_b o P_W o L_a
```

by separating it into source lift/characterization, route transport, and target projection/re-realization. The implementation does **not** claim that a software route proves physical S3/S4 corridor realization.
