# Persistent recursion

Some BLACKGLASS relationships may be intentionally long-lived. Section 15 does not model those as an infinite Python loop. A persistent recursive task executes only for a bounded slice and returns one of:

- `CLOSED` — its explicit close predicate became true.
- `SUSPENDED` — the slice budget ended and a continuation token was produced.

The continuation is content-addressed and includes task identity, state, step count, and inherited history root. Resume validates the continuation before execution continues. Section 16 can schedule these resumable tasks without changing the recursion semantics defined here.
