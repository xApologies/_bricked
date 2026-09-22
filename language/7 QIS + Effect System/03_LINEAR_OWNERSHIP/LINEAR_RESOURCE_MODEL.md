# Linear resource model

Quantum information is not modeled as an ordinary copyable value. The runtime registry gives each live nonclassical state one ownership token.

Allowed operations:

- `borrow_metadata`: inspect non-state metadata without duplicating amplitudes;
- `move`: transfer ownership to a new owner label while preserving the state ID;
- `consume`: terminate the live handle;
- `measure`: consume the coherent handle and produce a measured successor plus classical result;
- `classical_copy`: only after an explicitly classical result exists.

Forbidden operation:

- `clone_quantum_state` for any live PURE/DENSITY/JOINT quantum resource.

This is a compiler/runtime discipline inspired by quantum no-cloning and linear type systems. It is stronger than Python aliasing semantics and will become a Genesis type/effect rule.
