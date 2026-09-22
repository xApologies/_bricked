# Quantum information state model

Section 07 uses a generic finite-dimensional state model. It deliberately does not make `qubit` the primitive Genesis object.

A pure reference state is

`|psi> = sum_i a_i |b_i>`

with `sum_i |a_i|^2 = 1`.

A density state is a positive, trace-one operator represented in the reference backend as a finite complex matrix. The implementation validates Hermiticity and trace; full positive-semidefinite certification is intentionally limited to small reference cases.

Each state is attached to:

- a `state_id`;
- an optional `source_instance_id` / MMO identity;
- a basis or joint member ordering;
- a lifecycle/ownership token;
- a provenance trail;
- the QFT sector.

This is an execution model for language semantics, not a claim that every MMO literally is a finite qubit register.
