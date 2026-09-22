# Section 02 Architecture

## 1. The object stack

```text
MMO                       canonical mapped molecular identity
  |
  +-- Representation      3+1+1, atomic profile, QFT, GR, readable projections
  |
  +-- GeometricInstance   one live binding of a representation to chirality fabric
        |
        +-- FabricRegion
        +-- OverlaySegment (.gos)
        +-- Runtime Deltas
        +-- History / Provenance
        +-- BRANE M^5 descriptor
```

The term **Geometric** is the runtime/object-system name for an instantiated MMO representation. It does not replace the canonical MMO identity.

## 2. Memory composition

```text
Immutable .gcf Fabric
        +
Committed .gos Geometric Segments
        +
optional ordered delta segments
        =
Operative Chirality Fabric View
```

The base fabric remains byte-identical. A Geometric segment is also immutable once committed. Transformation forks state by adding a child delta or by checkpointing to a new derived fabric image.

## 3. Address translation

A Geometric has an object-local coordinate system. The default dense layout is formulaic:

```text
voxel = linearize(x,y,z)
base  = region.start + voxel * cells_per_voxel
role  = base + role_offset
```

The formula is stored in the binding manifest; an enormous per-voxel address table is unnecessary.

## 4. 3+1+1 adapter boundary

The scientific field `(X,Y,Z,2,2)` is preserved as a scientific representation. It is **not** asserted to be identical to the 2x2x2 hardware cell or to BRANE's five organizational coordinates.

Section 02 provides an implementation projection from scientific field components into groups of hardware cells. The original field remains independently hash-addressable, so no information-loss claim is hidden.

## 5. BRANE handoff

Section 02 emits:

`M^5 = (I, D, Chi, R, P)`

where:

- I = canonical MMO identity + live instance identity;
- D = dependency closure / representation dependencies;
- Chi = chirality-fabric binding and chirality summary;
- R = recursive/history/instance lineage;
- P = provenance/source/receipt chain.

BRANE adds request-relative realization coordinate **Z**. Section 02 never fabricates Z.
