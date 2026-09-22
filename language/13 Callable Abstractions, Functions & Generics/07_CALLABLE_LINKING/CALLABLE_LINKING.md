# Callable linking

Callable linking occurs before GIR module linking.

Two namespaces coexist:

- value namespace: Section 10 `use module::symbol as local : TYPE`;
- callable namespace: Section 13 `usefn module::function as local`.

Callable imports resolve only to public functions. The canonical function remains owned by its source module/package.

## Package rule

If package A uses `usefn` to import a callable from a module owned by package B, B must be a direct declared dependency of A. A may not reach through B to use a function owned by transitive package C.

## Function bodies and captures

v0.1 functions are closed over their parameters and explicit nested callable references. There is no supported lexical capture mechanism. A body that references an unavailable value simply fails after expansion in the ordinary Section 09 unknown-value checks.

## Linking order

Callable resolution does not change the deterministic dependency ordering of Section 12 packages or Section 09 GIR modules. Function bodies are expanded into the caller module; the resulting value imports retain their normal module dependency edges.
