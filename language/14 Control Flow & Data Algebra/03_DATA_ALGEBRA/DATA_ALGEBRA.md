# Data Algebra

Product type: `record Pair { left: INT, right: INT }`.

Sum type: `enum Choice { Left(INT), Right(TEXT), Empty }`.

Built-ins: `OPTION<T> = Some(T) | None`; `RESULT<T,E> = Ok(T) | Err(E)`.

Pure operations: `eq`, `not`, `and`, `or`, `add`, `sub`, `lt`, `le`, record construction/projection, variant construction/tag test/payload extraction.

## Match default ordering
A `_` default case is permitted only as the final case. Exhaustive explicit matches may omit `_`; the compiler proves coverage from the declared enum variants and lowers the final remaining variant without an extra impossible branch.
