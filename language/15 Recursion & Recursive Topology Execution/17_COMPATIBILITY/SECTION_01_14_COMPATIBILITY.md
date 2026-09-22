# Sections 01–14 compatibility

Section 15 is additive. It does not renumber any Section 01–14 opcode. The new recursion opcode window begins at `0x0090`, immediately after the Section 14 control/data window.

The Section 14 regression suite was rerun unchanged against its own reference implementation: 62/62 PASS. Section 15 does not redefine Portal, Rainbow Road, QFT/GR bridge, quantum ownership, package, callable, optimizer, or control/data semantics.

The current Section 15 surface subset is intentionally narrow. It proves the recursive frame ABI and termination/history contracts first; subsequent compiler integration can merge these forms into the full Section 10–14 parser without changing the recursive bytecode semantics.
