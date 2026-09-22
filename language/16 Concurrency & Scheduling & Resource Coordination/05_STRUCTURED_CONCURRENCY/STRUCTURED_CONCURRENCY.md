# Structured concurrency

Section 16 v0.1 uses explicit `spawn ... as ...` plus `join ...` declarations. Spawn handles form the program's structured task scope. A joined task must resolve to a terminal state before normal schedule closure.

Nested task scopes, actor mailboxes, channels, and distributed scheduling are intentionally deferred. The v0.1 surface is sufficient to establish deterministic task ownership, cancellation, resource cleanup, and closure semantics before adding richer asynchronous abstractions.
