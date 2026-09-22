# Symbol resolution

Symbol identity is `(module, exported-symbol)`.

The linker never resolves by bare value spelling across modules. `%g0` in two modules is unrelated until a typed import binds one module-local alias to another module's declared export.

During linking:

```text
module node id     01_mount    -> fixture::01_mount
module SSA value   %g0         -> %fixture::g0
import alias        %source     -> %fixture::g0
```

This alpha-renaming makes capture impossible without an explicit linker defect.
