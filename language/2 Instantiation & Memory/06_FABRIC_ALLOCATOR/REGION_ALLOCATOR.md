# Fabric Region Allocator

The allocator is deterministic first-fit in v0.1.

Input:
- fabric cell count;
- existing committed/reserved regions;
- required cells;
- alignment;
- optional guard cells.

Output:
- reservation id;
- start index;
- usable count;
- total reserved span;
- allocation receipt.

Future allocators may use locality, affinity, NUMA/device topology, Corridor proximity, or BRANE placement hints. Those are policy extensions, not ABI changes.
