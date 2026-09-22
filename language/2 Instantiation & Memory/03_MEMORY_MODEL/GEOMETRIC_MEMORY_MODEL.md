# Geometric Memory Model

## Base + segment + delta

A runtime view is layered:

```text
read(address):
    newest matching delta
    else committed Geometric segment
    else immutable fabric cell
```

No layer below the newest state is destroyed.

## Allocation

Writable Geometrics receive exclusive regions. The allocator tracks reservations separately from the fabric bytes.

Region lifecycle:

`FREE -> RESERVED -> COMMITTED -> QUIESCED -> RELEASED`

A reservation has a lease/transaction id and can be rolled back without touching the fabric.

## Dense and sparse layouts

- `DENSE`: every spatial voxel is assigned the same role-group layout. Deterministic and simple.
- `OCCUPIED`: only voxels satisfying a declared occupancy predicate are allocated; requires an explicit sparse index.

Version 0.1 defaults to DENSE for reproducible MMO execution. Sparse mapping is implemented as an optional profile, not a replacement.

## Role group

A voxel may map to several fabric cells. For the current 3+1+1 profile:

- four cells preserve the four `(2,2)` chirality-field components;
- one control cell stores runtime chirality/admissibility/persistence/readout-control summaries when those source fields exist.

Exact support arrays such as mass density or occupancy remain in the source representation registry unless separately mapped by an explicit role profile.
