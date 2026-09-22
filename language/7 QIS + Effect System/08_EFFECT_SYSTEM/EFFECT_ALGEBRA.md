# Quantum effect algebra

Effects are compiler-visible declarations:

`READ_META, SUPERPOSE, ENTANGLE, UNITARY, CHANNEL, DEPHASE, MEASURE, CLASSICALIZE, QFT_PORTAL_TRANSPORT, STRUCTURAL_TRANSDUCE, RECOVER`.

Each effect specifies:

- required input typestate;
- output typestate;
- whether ownership is consumed/moved;
- whether norm/trace is preserved;
- whether coherence may decrease;
- whether entanglement may be destroyed;
- permitted sector;
- whether a classical result is emitted.

Effects compose only when output typestate satisfies the next effect's input contract.
