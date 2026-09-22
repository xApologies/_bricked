# Toolchain constitution

Section 18 defines the operational shell around Genesis compilation and execution. The shell is intentionally replaceable: Python implements the reference toolchain, but build identity and diagnostic contracts are language-level artifacts rather than Python semantics.

The toolchain has six responsibilities: deterministic compilation; structured diagnostics; source-to-machine correlation; receipt-linked tracing; replay/debug inspection; and reproducible test/build orchestration.

The toolchain has no authority to relax a static proof obligation, synthesize a missing capability, rewrite BRANE ownership of Z, or commit BLACKGLASS state outside the Section 17 proposal/admission boundary.
