# 0001 — Bootstrap canonical development architecture

Date: 2026-09-20
Status: proposed for acceptance through a PR to main.

## Authority and rationale

The [user's bootstrap request](../sources/bootstrap-request.txt) specifies the architecture, module canon, shared specification names and constitutional requirements. The supplied development package provides the expanded level templates. No new gameplay or mathematical design decisions are introduced.

## Initial state and Git workflow

The workspace and GitHub repository were empty: no files, commits, branch refs or repository policy files existed. GitHub reported the default branch name main. An empty initial commit establishes main as a base for the requested PR; all bootstrap content is committed separately on bootstrap/canonical-architecture. This does not accept the proposed architecture into main.

## Exact source import

The package arrived at _inbox/dev.zip during implementation. Its original bytes are preserved in [provenance/checkpoints/dev.zip](../checkpoints/dev.zip), a recovery/source artifact rather than accepted canonical state.

The complete subtree at
`_bricked_LIVE_MODEL_CKPT003_2026-09-20/11_DEVELOPMENT_CONSTITUTION/LEVEL_XX_IMPLEMENTATION_SCAFFOLD/`
maps to `development/constitution/LEVEL_XX/`.

All 87 files, including expanded and legacy templates, are preserved without consolidation, rewriting, or omissions. Every extracted file was compared against its ZIP entry using SHA-256. The [source manifest](../sources/dev-import.json) records the archive hash, source entries, destination paths, lengths and file hashes. Git attributes disable text conversion for this subtree to preserve the imported bytes.

The rest of the checkpoint remains preserved in the original ZIP. Its historical level seeds and live-model documents are not promoted into canonical module definitions. The current request's 171-scenario canon governs this bootstrap.

## Boundaries and ambiguities

- Source filenames and their legacy terminology are preserved exactly, including LEVEL_XX_IMPLEMENTATION_SCAFFOLD references inside documents; only the containing directory is mapped to the requested LEVEL_XX path.
- Template Genesis sections describe per-level instantiation. The single shared specification locations remain docs/genesis; those requested placeholders remain OPEN. Existing source hints are not extrapolated into missing mathematics.
- The package contains historical project material beyond the requested constitution. It is retained in the ZIP without silently adopting or reconciling it as current game design.
- Other scenario identifiers, missing normalization details, mathematics and behavior remain OPEN.
- The empty initial main commit is a workflow necessity for an otherwise empty repository, not approval of this PR.

Specifications stay separate from reserved runtime boundaries. The validator is development tooling only. No game runtime is implemented and no level is certified Gold. The [inventory](../audits/bootstrap-inventory.md) records every created file.
