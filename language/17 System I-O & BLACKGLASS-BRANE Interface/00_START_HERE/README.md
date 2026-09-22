# Genesis Chirality Machine — Section 17

**Title:** System I/O + BLACKGLASS/BRANE Interface

Section 17 defines the system boundary between Genesis programs and the host environment. System interaction is capability-typed, receipt-bearing, provenance-preserving, and explicit. Genesis code does not receive ambient filesystem, device, BLACKGLASS Heart, or BRANE-module authority.

Core rule:

```text
Genesis computation --typed request--> System Boundary --receipt--> Genesis computation
```

The reference implementation is a deterministic host simulator. It does not claim that BLACKGLASS 3.0 or the production BRANE host has already been migrated to Genesis. It establishes the contract that the later BLACKGLASS migration can target.

The architecture preserves the mounted BRANE distinction:

```text
M^5 = I x D x Chi x R x P
B^6 = I x D x Chi x R x P x Z
```

A module supplies `M^5`; BRANE owns request-relative realization `Z`. BLACKGLASS remains the operations base/host and is not reduced to BRANE.
