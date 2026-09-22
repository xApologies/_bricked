# Pass catalog

| Pass | O0 | OAUDIT | O1 | Rule |
|---|---:|---:|---:|---|
| canonicalize | no | yes | yes | deterministic object/edge form |
| dedupe_edges | no | yes | yes | remove byte-identical duplicate edges |
| const-hash fold | no | no | deferred | GIR v0.1 has no typed HASH literal, so the rewrite is intentionally disabled |
| coalesce_alias_move | no | no | yes | only `MOVE @alias_only=true`; never QSTATE |
| dead_pure_elimination | no | no | yes | retain all effectful/export-reachable nodes |

The current executable Genesis examples are intentionally effect-heavy, so O1 generally preserves their semantic instruction count. This is expected; Section 11 prefers a no-op optimization over an unsafe rewrite.
