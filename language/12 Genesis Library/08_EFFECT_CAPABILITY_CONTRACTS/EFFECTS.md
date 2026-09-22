# Effect and capability contracts

Each manifest's `effects` field is an upper bound on the effects exercised by that package's own source modules. Section 12 lowers each module through the Section 10 frontend and rejects undeclared effects.

`backend_capabilities` is descriptive/required compatibility metadata. It cannot authorize an operation. The Section 09 capability checker and selected backend remain authoritative.
