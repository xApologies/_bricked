# Equivalence

Reference differential execution compares exported semantic values and backend ledger roots using fresh Section 08 reference VMs. Optimization receipts preserve before/after GIR hashes, pass records, barrier witnesses, GVM hash, code-generation profile, and equivalence status.

Byte-for-byte equality of GVM is not required: compact code generation intentionally removes source labels. Semantic exports and ledger behavior are the invariant target.
