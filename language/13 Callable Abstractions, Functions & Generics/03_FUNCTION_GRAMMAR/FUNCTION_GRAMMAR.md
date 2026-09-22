# Function grammar

Section 13 accepts both `genesis 0.1.0` and the additive callable surface marker `genesis 0.2.0`. Expanded output is normalized to the Section 10-compatible `genesis 0.1.0` core language.

## Declaration

```text
[pub] fn NAME[<GENERIC (, GENERIC)*>]
    (PARAM (, PARAM)*) -> TYPE
    [effects [EFFECT (, EFFECT)*]] {
        BODY
        return LOCAL_VALUE
    }
```

Generic:

```text
T
T:BOUND
```

Parameter:

```text
name:TYPE
```

Examples:

```text
pub fn fork_geometric<G:GEOMETRIC> (source:G) -> G effects [TRANSFORM,INHERIT] {
  en child : G = fork source
  return child
}
```

```text
pub fn prepare_superpose_measure<G:GEOMETRIC>
    (source:G) -> QRESULT<CLASSICAL>
    effects [QUANTUM_LINEAR,MEASURE] {
  q prepare source as q0
  q superpose q0 as q1
  q measure q1 as result
  return result
}
```

## Callable imports

```text
usefn genesis.std.portal.callables::gr_transfer as transfer
```

A `usefn` does not produce a runtime value. It binds a compile-time callable identity.

## Calls

```text
call transfer<GEOMETRIC<CLOSED,UNBOUND>> (source) as destination
```

Multiple arguments:

```text
call combine<T,U> (left,right) as result
```

Parentheses are canonical. A whitespace argument form is also accepted by the reference parser for simple values.

## Return

Callable ABI v0.1 requires one `return` and requires it to name a value produced inside the function body. This avoids creating an unmodeled generic alias/move operation, especially for linear resources.

## Nested calls

Function bodies may call other functions. Expansion is recursive but the call graph must be acyclic.
