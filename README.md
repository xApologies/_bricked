# _bricked — start here

[Genesis](genesis/README.md) is organized for people and applications around four domains:

| Domain | Geometry | Navigate |
| --- | --- | --- |
| State | R5 / D5 | [State](genesis/domains/state/README.md) |
| Nexus | H6 / D6 | [Nexus](genesis/domains/nexus/README.md) |
| Shell | Sigma7:8 / D7+D8 | [Shell](genesis/domains/shell/README.md) |
| Sea | S9:11 / D9+D10+D11 | [Sea](genesis/domains/sea/README.md) |

Applications start with [DOMAIN_REGISTRY.json](genesis/registries/DOMAIN_REGISTRY.json). Adjacency is `Sea <-> Shell <-> Nexus <-> State`; source authorities and cross-cutting systems are not additional domains.

- Source authorities: [mathematics](genesis_mathematics/README.md), [structural language](genesis/authorities/structural_language.md), [programming language](language/README.md), [Chirality Fabric](chirality_fabric/README.md).
- Cross-cutting systems: [Rainbow Road](genesis/systems/rainbow_road/README.md), [Guardian](genesis/systems/guardian/README.md), [registry](genesis/registries/CROSSCUTTING_REGISTRY.json).
- Game/development: [171-scenario module canon](development/modules/README.md), [Development Constitution](development/constitution/LEVEL_XX/CONSTITUTION.md), [game boundary](game/).
- Provenance: [authority map](genesis/AUTHORITY_MAP.md), [decisions](provenance/decisions/), [DP-007 audit](provenance/audits/DP007_INTEGRATION.md).

Read the [Project Constitution](PROJECT_CONSTITUTION.md) and [contribution rules](CONTRIBUTING.md). GitHub main remains accepted project state; this working branch proposes changes. Genesis-native semantics remain upstream of host/reference realization. OPEN mathematics is not completed by this navigation layer; no game runtime is implemented here.

Validation: `python -B tools/validators/validate-genesis.py`, `node tools/validators/validate-bootstrap.mjs`. The former validates registries, domain mounts, current documentation links and registry-only discovery. The latter checks preserved bootstrap/constitution invariants.
