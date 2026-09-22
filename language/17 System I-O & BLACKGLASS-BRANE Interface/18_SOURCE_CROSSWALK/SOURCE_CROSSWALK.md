# Source Crosswalk

Section 17 is informed by the mounted BLACKGLASS/BRANE source lineage and keeps source status explicit.

Source-derived constraints used here:

- BLACKGLASS hosts/contains BRANE services; BLACKGLASS is not reduced to BRANE.
- BRANE host model: `B^6 = I x D x Chi x R x P x Z`; external modules: `M^5 = I x D x Chi x R x P`.
- Active external BRANE module contract: internal dimension 5, contract version 2.0, canonical state READ_ONLY, rewrite DERIVED_ONLY.
- BRANE owns request-relative realization `Z`.
- BLACKGLASS hardware is replaceable; durable identities should not depend on physical host identity.
- Suggested BLACKGLASS storage uses immutable/content-addressed source with paths treated as implementation detail.
- Trust-boundary crossings require a typed receipt or explicit policy decision.
- Durable state uses a persistence proposal/admission boundary rather than arbitrary module mutation.

Section-17 additions such as exact opcode numbers, reference syntax, deterministic emulator `Z`, and Python classes are implementation decisions, not retroactively claimed as source canon.
