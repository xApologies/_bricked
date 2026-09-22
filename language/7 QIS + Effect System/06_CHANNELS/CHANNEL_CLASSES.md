# Channel classes

Section 07 recognizes these semantic channel classes:

- `IDENTITY`
- `UNITARY`
- `ISOMETRIC_REFERENCE`
- `CPTP_REFERENCE`
- `DEPHASING`
- `PROJECTIVE`
- `CLASSICALIZE`
- `STRUCTURAL_TRANSDUCTION`

`UNITARY` requires a square matrix with `U†U = I` within tolerance.

`CPTP_REFERENCE` uses Kraus operators and verifies the trace-preservation condition `sum K†K = I` within tolerance. Complete positivity is inherited from the Kraus representation used by the reference backend.

`STRUCTURAL_TRANSDUCTION` is intentionally **not** a quantum channel claim. It names the Section 06 QFT/GR structural bridge boundary.
