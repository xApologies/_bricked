# Control Flow Constitution

`if <BOOL> { ... } else { ... }` emits an explicit branch and verifies both paths.

`match <sum> { Tag(binding) => { ... } ... }` emits tag tests and branches; closed sums require exhaustive coverage.

`repeat N { ... }` is statically unrolled. Section 14 intentionally excludes unbounded `while`/recursive repetition; Section 15 owns that termination problem.
