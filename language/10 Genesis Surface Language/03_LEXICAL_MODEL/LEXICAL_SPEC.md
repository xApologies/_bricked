# Lexical specification v0.1

- Encoding: UTF-8.
- One executable statement per physical line in v0.1.
- `#` and `//` start comments outside quoted strings.
- Strings use JSON-compatible double quotes.
- Identifiers: `[A-Za-z_][A-Za-z0-9_]*`.
- Module names additionally permit `.`.
- MMO handles are opaque tokens beginning with `@`, e.g. `@hydrogen_reference`.
- Refined types use Section 09 syntax, e.g. `GEOMETRIC<CLOSED,QFT>`.
- Optional operation attributes are appended as `@{...}` where the object is valid JSON.
- Statements may optionally terminate with `;`.

The `@{...}` object is intentionally an escape-safe attribute carrier for machine-facing data while the semantic vocabulary stabilizes. Attributes never override the opcode selected by the source statement.
