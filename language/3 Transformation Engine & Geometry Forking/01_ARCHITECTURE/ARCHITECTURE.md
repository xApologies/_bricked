# Section 03 Architecture

## 1. State is persistent, transformation is a fork

A committed Geometric is an addressable history-bearing state. Section 03 therefore rejects anonymous in-place mutation as its canonical state transition.

```text
                       +--> child A (.gtd)
parent (.gos + chain) -+
                       +--> child B (.gtd)
```

Both children retain the parent as ancestry. The parent remains byte- and hash-stable.

## 2. Operative view

```text
immutable .gcf fabric
+ root .gos instantiation segment
+ zero or more ordered .gtd transformation deltas
= operative Geometric state
```

Later deltas shadow earlier cells only at addresses explicitly written by that delta.

## 3. Transformation transaction

```text
REQUEST
  |
  v
PRECONDITION / STALE-ROOT CHECK
  |
  v
EFFECT ANALYSIS
  |
  v
CAPABILITY ADMISSION
  |
  v
PLAN
  |
  v
STAGE PATCH IN MEMORY
  |
  v
INVARIANT CHECKS
  |
  +---- failure ----> ABORT (no committed state)
  |
  v
WRITE IMMUTABLE .gtd
  |
  v
REOPEN + HASH VERIFY
  |
  v
CLOSURE RECEIPT
  |
  v
CHILD INSTANCE + BRANE M^5
```

## 4. Semantic separation

A transformation may change a **representation state** without declaring a new canonical molecular identity. The request therefore carries an explicit semantic identity policy:

- `PRESERVE_MMO`: same canonical MMO, new live instance;
- `DERIVE_REPRESENTATION`: same canonical MMO, new representation identity;
- `DERIVE_MMO`: new canonical MMO identity must be supplied explicitly.

No low-level cell write is allowed to silently infer a new molecule.

## 5. Capability boundary

Pipeline/domain policy is modeled as an effect capability set. The recovered architecture distinguishes T-domain formation, which may write chirality, from R-domain environmental exposure, which reads chirality without rewriting existence occupancy. Section 03 makes that distinction executable.

## 6. Closure

A transformation closes only if:

1. parent pre-state root matches the declared parent;
2. requested effects are admitted;
3. all emitted addresses remain inside the parent's fabric region;
4. invariant contract passes;
5. the delta file reopens and verifies;
6. the post-state root equals the planned post-state root;
7. parent segment(s) and base fabric remain unchanged;
8. a closure receipt and lineage record are produced.
