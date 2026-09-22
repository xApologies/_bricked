# Memory model

GVM intentionally exposes several distinct stores:

1. **Typed register file** — ephemeral execution values.
2. **Resource table** — handles to identity-bearing immutable/versioned objects.
3. **Fabric address space** — Section 01 hardware/fabric substrate.
4. **Overlay/derived state** — permitted dynamic writes over stable fabric identity.
5. **Receipt ledger** — append-only provenance/closure history.
6. **Frame stack** — control-flow implementation state.

These stores are not collapsed into one generic byte-addressable heap because doing so would erase the distinctions the earlier sections were built to preserve.
