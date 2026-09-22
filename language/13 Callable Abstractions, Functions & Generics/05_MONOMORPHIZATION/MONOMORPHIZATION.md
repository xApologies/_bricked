# Deterministic monomorphization

Genesis callable ABI v0.1 uses ahead-of-GIR monomorphization.

For each call:

```text
call F<T1,...,Tn> (v1,...,vm) as out
```

the compiler performs:

1. Resolve `F` to its canonical `module::function` identity.
2. Check generic and value arities.
3. Check generic bounds.
4. Compute `specialization_id = hash(function_definition, concrete_type_args)`.
5. Compute a distinct call-site identity.
6. Substitute type parameters.
7. Substitute formal value parameters.
8. Alpha-rename every locally produced identity with a call-site namespace.
9. Bind the return-producing local directly to the caller's requested output name.
10. Expand nested calls recursively.
11. Compute actual underlying effects.
12. Check effect containment.
13. Emit ordinary core Genesis.
14. Run the full Section 10/09/11/08 toolchain.

## Why locals are renamed

Two calls may use the same function-local names. Without alpha-renaming, GIR would observe value redefinitions. The reference convention uses internal names like:

```text
__c7_gr_transfer_admission
__c7_gr_transfer_portal0
```

These names are compiler-generated serialization details, not user-facing semantic identities.

## Why the return local is rebound

The final producing operation is emitted directly with the caller's requested output identity. No extra generic MOVE is introduced. This matters because generic MOVE is forbidden for QSTATE and would otherwise create ambiguous ownership semantics.
