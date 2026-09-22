# Genesis Chirality Machine — Section 03
## Transformation Engine + Geometric Forking
Version 0.1.0 — 2026-08-21

Section 03 defines how a live **Geometric** (an instantiated MMO representation) changes state on chirality fabric without destroying its parent state, ancestry, or source provenance.

The implementation rule is:

```text
parent Geometric
    -> transformation request
    -> effect + capability admission
    -> deterministic transformation plan
    -> immutable delta segment (.gtd)
    -> invariant verification
    -> closure receipt
    -> child Geometric
```

**No transformation mutates a committed parent Geometric in place.** A transformation creates a child state whose operative fabric view is the parent segment chain plus one immutable transformation delta.

### What Section 03 implements

- typed transformation requests and plans;
- effect/capability admission;
- source-aware T-domain vs R-domain mutation policy;
- immutable `.gtd` delta-segment format;
- deterministic state roots and patch roots;
- transformation programs (ordered operator composition);
- native runtime operators: inherit, stabilize, redistribute, destabilize, normalize, chirality mirror, field set;
- invariant contracts;
- semantic identity policy;
- transactional commit/abort;
- closure receipts;
- append-only transformation ledger;
- child history/provenance;
- BRANE M^5 re-lift after transformation;
- synthetic and real-fixture conformance tests.

### Non-claims

This is an implementation layer. Transform operators used as test fixtures are computational operators over the mapped chirality representation. They are **not** claims that an arbitrary operator represents a physical molecular reaction.

### Recovery

Mount Section 01, then Section 02, then Section 03 Part A. Parts B-D provide real fixtures and source/implementation lineage.
