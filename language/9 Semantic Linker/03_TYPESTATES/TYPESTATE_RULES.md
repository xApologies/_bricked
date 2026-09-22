# Typestate rules

## Portal

```text
PORTAL<T,OPEN>
   | transport may occur
   v
PORTAL<T,OPEN>
   | close exactly once
   v
PORTAL<T,CLOSED>
```

The v0.1 GIR representation uses the same SSA Portal value for transport and close, so Section 09 tracks typestate in the verifier state rather than requiring a new SSA value for closure.

## Road

`ROAD_APPEND` moves the input Road version and returns a successor `ROAD<OPEN>`. This mirrors the persistent/versioned Road implementation in Section 05/08.

## QSTATE

```text
QSTATE<OWNED> --SUPERPOSE/CHANNEL--> moved + successor OWNED
QSTATE<OWNED> --ENTANGLE with OWNED--> both moved + successor OWNED
QSTATE<OWNED> --MEASURE--> consumed + QRESULT<CLASSICAL>
```

Generic `MOVE` cannot clone a QSTATE.
