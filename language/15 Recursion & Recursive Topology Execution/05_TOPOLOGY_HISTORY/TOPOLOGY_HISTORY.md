# Recursive topology and history

Section 15 supplies a cycle-aware recursive topology executor for relationship graphs. The executor is deterministic: adjacency lists are traversed in declared order, every visit has a path, cycle encounters are recorded, and each resolved node contributes a closure digest to the final history root.

Supported cycle policies in v0.1:

- `skip`: record the cycle/revisit and do not recurse into the repeated node.
- `error`: reject the traversal at the first repeated active/visited node.

The traversal result is therefore not merely a set of nodes; it is an ordered history object containing visits, edges, cycle witnesses, closure order, and a deterministic history root.
