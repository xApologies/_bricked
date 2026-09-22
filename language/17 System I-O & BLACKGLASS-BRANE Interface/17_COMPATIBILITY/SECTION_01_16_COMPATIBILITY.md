# Section 01–16 Compatibility

Section 17 is additive. It does not change the Section 01 hardware ABI, Geometric layout, transformation/Portal/Road rules, QFT/GR bridge, quantum effect ownership, GIR/GVM identity, static type/effect rules, package model, callables/generics, control/data algebra, recursion semantics, or logical concurrency.

Section 16 tasks may issue Section-17 system calls as explicit scheduling points. A native runtime may execute independent calls in parallel only if it preserves the declared receipt/order/resource contract.
