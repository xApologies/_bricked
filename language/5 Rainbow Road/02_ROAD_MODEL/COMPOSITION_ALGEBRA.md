# Road Composition Algebra

For closed Portals

```text
P1 : A -> B
P2 : B -> C
```

the sequential composition `P2 o P1` is admitted as a Road segment when:

1. the endpoint address of `P1` matches the source address of `P2`;
2. the sectors agree in Section-05 v0.1;
3. the output identity/preservation state of `P1` satisfies the input obligations of `P2`;
4. the declared invariant residue survives both legs;
5. every underlying Corridor independently satisfies Resolution/Bandwidth/chirality/closure gates.

For Road plans `R1 : A -> B` and `R2 : B -> C`, `compose(R1,R2)` concatenates waypoint and Corridor witnesses only after the same boundary/sector/preservation checks pass.

Associativity is treated as a **typed composition obligation**, not assumed globally across arbitrary Portal classes.
