# Bridge Object

A Bridge is a typed sector-transduction transaction:

```text
Bridge<S,T>(Geometric@Address)
```

where `(S,T)` is one of:

```text
(QFT,GR)
(GR,QFT)
```

Bridge execution:

1. characterize the immutable source Geometric;
2. construct source-sector representation `rho_S`;
3. construct target-sector representation `rho_T` from the same underlying witness;
4. validate `R_QG` common ancestry;
5. audit invariant roots and preservation contract;
6. emit immutable Bridge receipt;
7. update the logical sector/address view for subsequent Portal actions;
8. add bridge history/provenance metadata to the runtime instance envelope without rewriting its segment chain.

The Bridge does not consume Rainbow Bus capacity because it does not traverse a Corridor. Future hardware-specific transduction resources may add a separate resource class.
