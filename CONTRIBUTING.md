# Contributing

Start from accepted GitHub `main`, inspect repository instructions, and create a working branch. Preserve existing files. Submit a pull request to `main` for review; a branch or ZIP checkpoint does not constitute accepted state.

Follow [PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md). Keep specifications in `docs/` and `development/`, and future runtime implementation in `game/`. Do not implement runtime as part of this bootstrap.

Use the complete authenticated `development/constitution/LEVEL_XX/` template for every playable scenario . Preserve all stages and expanded sections. Use **NOT USED + rationale** where appropriate. Reference shared canonical specifications rather than copying or redefining shared architecture. Keep unresolved definitions explicitly OPEN.

For architectural changes, record sources, rationale, affected paths and unresolved questions in `provenance/`, and update `CHANGELOG.md`. Verify all 00–14 requirements before designating any level Gold.

Run `node tools/validators/validate-bootstrap.mjs` for bootstrap checks. The imported template file set and hashes must match the recorded source.

## Source preservation

Obtain the exact supplied `dev.zip`, record its origin and SHA-256, inspect its entries, and import the complete canonical subtree and templates without changing their contents or hierarchy. Compare all imported entries and file hashes against the source. Record that audit and replace the explicit missing-package status only after successful verification. Resolve any conflicts with existing files visibly.

The repository was empty at bootstrap. An empty initial commit establishes `main` as the PR base; the architecture is proposed separately on `bootstrap/canonical-architecture`.
