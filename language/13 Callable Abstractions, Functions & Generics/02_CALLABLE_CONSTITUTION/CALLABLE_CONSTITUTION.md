# Callable constitution

A callable is a statically named, typed graph template:

```text
Function = (identity, generic parameters, value parameters,
            return contract, effect contract, body graph, visibility)
```

A call is admissible when all of the following hold:

- the callable identity resolves unambiguously;
- visibility permits access;
- generic arity matches;
- each concrete generic type satisfies its bound;
- value arity matches;
- recursive expansion is absent;
- body expansion terminates;
- expanded effects are contained in the declared effect set;
- the resulting module passes Section 09 static semantics;
- the returned value's refined type satisfies the specialized return contract;
- backend capabilities satisfy the final linked GIR.

## Function identity

Within one module, function names are unique. Cross-module identity is `module::function`. Imported callable names are local aliases only; they do not alter the function's canonical identity.

## Call identity

Each call receives a deterministic compiler receipt identity `gcall-*`. Each concrete generic specialization receives `gmono-*`. Multiple calls to the same specialization have different call identities while sharing the same specialization identity.

## Value identity

Arguments are not copied by the callable layer. They are substituted into the specialized body. This is particularly important for linear quantum resources: a function that attempts to use an owned QSTATE twice will fail the ordinary Section 09 linearity check after expansion.
