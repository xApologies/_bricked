# Generic type system

Section 13 uses explicit static type parameters. A generic variable stands for a complete Genesis type expression, including refined typestates such as:

```text
GEOMETRIC<CLOSED,QFT>
PORTAL<GR,OPEN>
QSTATE<OWNED>
RECEIPT<PROVENANCE>
M5
```

A declaration such as:

```text
<G:GEOMETRIC>
```

admits refined Geometric instances. The constraint is checked using the Section 09 compatibility relation. The generic layer does not define an independent type universe.

## Substitution

For a call:

```text
call f<GEOMETRIC<CLOSED,GR>> (x) as y
```

with declaration:

```text
fn f<T:GEOMETRIC> (x:T) -> T ...
```

Section 13 specializes `T := GEOMETRIC<CLOSED,GR>` before lowering to GIR.

## Explicit type arguments

v0.1 requires explicit generic type arguments. This avoids silently inventing an inference system before variance, trait constraints, associated types, and linear-resource inference have been specified.

## Future extension boundary

Possible later additions include type argument inference, const generics, effect generics, sector parameters, chirality/admissibility constraints, and capability traits. None are silently assumed by Section 13.
