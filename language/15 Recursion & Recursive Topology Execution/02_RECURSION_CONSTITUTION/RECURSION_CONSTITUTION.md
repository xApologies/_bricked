# Recursion constitution

A recursive relation is executable only when the runtime can answer four questions:

1. **Identity** — which recursive function/frame is continuing?
2. **Admission** — what contract permits another recursive edge?
3. **History** — what ancestry/visit state is inherited into the child frame?
4. **Closure** — what evidence proves a frame resolved before its value is inherited upward?

For a well-founded metric `m`, a self edge is admitted only when `m_child < m_parent`. For fuel recursion, `fuel_child = fuel_parent - 1`. For topology recursion, a child key must satisfy the declared cycle policy. Persistent recursion has no finite termination proof; therefore execution is sliced, yieldable, and resumable under a resource budget.
