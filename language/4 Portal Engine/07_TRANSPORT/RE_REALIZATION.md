# RE_REALIZE Transport

The transport engine reads the source's composite state through its `.gos` + `.gtd` chain and writes the resulting logical cells into a new `.gos` segment at the reserved destination region.

This has four useful properties:

1. the source is untouched;
2. the destination is independently readable without the source chain;
3. content/residue roots can be compared across distinct physical addresses;
4. the operation models information transportation as re-realization rather than pointer reassignment.

Section 04 does not claim that this software copying operation is the final custom-hardware Portal mechanism. It is the executable reference semantics for future backends.
