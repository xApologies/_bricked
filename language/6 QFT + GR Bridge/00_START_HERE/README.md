# Genesis Chirality Machine — Section 06
## QFT/GR Representation Bridge + Sector Transduction Engine

Version `0.1.0` — implementation layer.

Section 06 makes the QFT/GR bridge executable **as a typed representation transduction**, without asserting that QFT and GR are identical objects and without fabricating a global inverse map.

The source-backed formal spine is:

```text
Common Chirality Fabric state F
       |                |
       | rho_Q          | rho_G
       v                v
    QFT view          GR view

R_QG = { (q,g) | exists F: q=rho_Q(F), g=rho_G(F) }
```

For Corridor `W` the source bridge defines the transport candidate:

```text
P_W^chi : F_a -> F_b
rho_Q o P_W^chi = U_Q(W) o rho_Q
rho_G o P_W^chi = U_G(W) o rho_G
```

Section 06 operationalizes the **software contracts** needed to represent and audit those relationships. It does **not** claim to finish the source's open physical typing/proof obligations.

### New executable capability

A Rainbow Road may now contain explicit sector boundaries:

```text
Portal<QFT> -> Bridge<QFT,GR> -> Portal<GR>
```

or the reverse. A Portal itself remains single-sector. Sector changes occur only through a Bridge receipt at a specific realized Geometric/address.

### Core laws

1. QFT and GR are distinct readable representations.
2. A Bridge changes the readable sector/view; it does not mutate the underlying Geometric.
3. No inverse `rho_Q^-1` or `rho_G^-1` is assumed.
4. Cross-sector correspondence is established by a common-ancestry witness.
5. The same logical MMO identity and declared invariant residue must survive unless an explicit future transduction contract says otherwise.
6. Mixed-sector Roads preserve every Portal and Bridge receipt in order.
7. Bridge execution never bypasses Corridor/Portal admission for actual transport.
