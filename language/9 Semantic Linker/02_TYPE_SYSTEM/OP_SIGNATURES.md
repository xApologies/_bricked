# Selected static signatures

```text
FABRIC_MOUNT()                                -> FABRIC
FABRIC_ALLOC(FABRIC)                          -> REGION
GEO_INSTANTIATE(FABRIC, REGION)               -> GEOMETRIC<CLOSED,UNBOUND>
GEO_FORK(GEOMETRIC<CLOSED,S>)                 -> GEOMETRIC<CLOSED,S>
RELATE(GEOMETRIC, X)                          -> RELATION
ADMIT(GEOMETRIC)                              -> ADMISSION
TRANSFORM(GEOMETRIC<CLOSED,S>, ADMISSION)     -> GEOMETRIC<CLOSED,S>
PORTAL_OPEN(GEOMETRIC<CLOSED,S>, ADMISSION)   -> PORTAL<T,OPEN>
PORTAL_TRANSPORT(PORTAL<T,OPEN>, GEOMETRIC)   -> GEOMETRIC<CLOSED,T>
PORTAL_CLOSE(PORTAL<T,OPEN>, GEOMETRIC<...,T>) -> RECEIPT<PORTAL_CLOSE>
ROAD_BEGIN(GEOMETRIC)                         -> ROAD<OPEN>
ROAD_APPEND(ROAD<OPEN>, RECEIPT)              -> ROAD<OPEN>
ROAD_CLOSE(ROAD<OPEN>, GEOMETRIC)             -> RECEIPT<ROAD_CLOSE>
BRIDGE_SECTOR(GEOMETRIC<CLOSED,S>, S, T)      -> BRIDGE<S,T>
Q_PREPARE(GEOMETRIC)                          -> QSTATE<OWNED>
Q_SUPERPOSE(QSTATE<OWNED>)                    -> QSTATE<OWNED> [moves input]
Q_ENTANGLE(QSTATE<OWNED>, QSTATE<OWNED>)      -> QSTATE<OWNED> [moves both]
Q_CHANNEL(QSTATE<OWNED>)                      -> QSTATE<OWNED> [moves input]
Q_MEASURE(QSTATE<OWNED>)                      -> QRESULT<CLASSICAL> [consumes input]
BRANE_LIFT(GEOMETRIC)                         -> M5
PROVENANCE_SEAL(X)                            -> RECEIPT<PROVENANCE>
```

`S` and `T` are sector refinements. An `UNBOUND` Geometric may acquire a sector on first admitted sector-specific transport. Once sector-bound, a different sector requires an explicit Bridge witness.
