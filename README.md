# _bricked

Canonical game-development repository: [xApologies/_bricked](https://github.com/xApologies/_bricked).

GitHub `main` is the canonical accepted project state. This bootstrap is a proposal on a working branch.

The complete 87-file level constitution has been imported byte-for-byte from `dev.zip`. See [bootstrap provenance](provenance/decisions/0001-bootstrap.md) and the [source manifest](provenance/sources/dev-import.json).

## Repository map

| Path | Purpose |
| --- | --- |
| `docs/` | Canonical specifications, design, cybersecurity, shared Genesis, visual language, glossary, diagrams |
| `development/` | Level constitution, module development, shared systems, development checkpoints |
| `game/` | Reserved runtime implementation boundaries; no runtime implemented |
| `content/` | Art, audio, VFX, UI, shaders, Blender assets |
| `data/` | Level, object, state, algorithm and test data |
| `tools/` | Validators, exporters, generators, developer tools |
| `tests/` | Unit, integration, regression, adversarial and performance tests |
| `platform/` | iOS, Android and desktop packaging/integration boundaries |
| `provenance/` | Decisions, checkpoint records, source records and audits |

The directory tree and all created files are recorded in [the bootstrap inventory](provenance/audits/bootstrap-inventory.md).

Read [PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md), [CONTRIBUTING.md](CONTRIBUTING.md), the [module canon](development/modules/README.md), and the [shared Genesis index](docs/genesis/README.md).

## Validation

Run `node tools/validators/validate-bootstrap.mjs`. Checks cover directory boundaries, module totals, OPEN placeholders, and the imported file hashes and exact file set. No gameplay or Genesis mathematics is implemented by this validator.
