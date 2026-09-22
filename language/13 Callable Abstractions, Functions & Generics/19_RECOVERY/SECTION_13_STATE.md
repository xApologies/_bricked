# Section 13 recovery state

Canonical section title: **Callable Abstractions, Functions + Generics**.

Current execution strategy: static monomorphization into the existing core Genesis relationship graph. No runtime generic dictionaries and no new GVM function opcode semantics are required.

Stable syntax added:

```text
pub fn ...
fn ...
usefn module::function as local
call function<T...> (args...) as output
return local
```

Key invariants: explicit generic bounds, acyclic call graph, deterministic specialization, alpha-renamed locals, effect containment, full Section 09 recheck, QSTATE linearity retained, Portal/Road closure retained, Bridge requirements retained, direct package dependency discipline retained.

Reference test target: 48 tests. Reference package target: six end-to-end applications.

Next architectural layer after Section 13 should be selected from actual remaining language gaps rather than assumed. Candidates include control-flow/data algebra and native callable ABI, but the callable layer itself is usable now.
