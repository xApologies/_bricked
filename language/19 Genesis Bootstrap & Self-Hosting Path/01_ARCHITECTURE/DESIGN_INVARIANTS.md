# Design invariants

1. Genesis semantics remain defined by the frozen section contracts, not by Python implementation accidents.
2. Stage-0 is explicitly trusted and explicitly named in every bootstrap receipt.
3. A fixed point is reproducibility evidence, not an independent proof of compiler correctness.
4. The bootstrap controller may request compilation only through a declared typed compiler port.
5. The compiler port receives immutable CAS references and emits immutable CAS references.
6. Bootstrap stages may not mutate source artifacts.
7. Stage identity is content-derived; wall-clock time and host paths are excluded.
8. Self-hosting status is monotonic and auditable per component: HOST_ORACLE, GENESIS_CONTROLLED, GENESIS_NATIVE, or DEFERRED.
9. No component may be labelled GENESIS_NATIVE merely because Genesis invokes a host implementation.
10. BLACKGLASS durable updates remain proposal/admission transactions.
