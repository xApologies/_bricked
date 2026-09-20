# Bootstrap inventory

All 167 listed files are created by this bootstrap. No pre-existing tracked files were modified. Git administrative files and the preserved, ignored local _inbox/dev.zip source drop are excluded.

## Resulting directory tree

```text
_bricked/
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── PROJECT_CONSTITUTION.md
├── README.md
├── content
│   ├── art
│   │   └── .gitkeep
│   ├── audio
│   │   └── .gitkeep
│   ├── blender
│   │   └── .gitkeep
│   ├── shaders
│   │   └── .gitkeep
│   ├── ui
│   │   └── .gitkeep
│   └── vfx
│       └── .gitkeep
├── data
│   ├── algorithms
│   │   └── .gitkeep
│   ├── levels
│   │   └── .gitkeep
│   ├── objects
│   │   └── .gitkeep
│   ├── states
│   │   └── .gitkeep
│   └── tests
│       └── .gitkeep
├── development
│   ├── checkpoints
│   │   └── .gitkeep
│   ├── constitution
│   │   └── LEVEL_XX
│   │       ├── 00_RELEASE
│   │       │   ├── CHANGELOG.md
│   │       │   ├── DEFINITION_OF_DONE.md
│   │       │   ├── LEVEL_MANIFEST.template.json
│   │       │   └── README.md
│   │       ├── 01_DESIGN
│   │       │   ├── DEPENDENCIES.md
│   │       │   ├── LEARNING_OBJECTIVES.md
│   │       │   ├── LEVEL_BRIEF.md
│   │       │   └── PLAYER_FANTASY.md
│   │       ├── 02_CYBERSECURITY
│   │       │   ├── ASSET_MAP.md
│   │       │   ├── ATTACK_PATHS.md
│   │       │   ├── DEFENDER_MODEL.md
│   │       │   ├── LANDSCAPE.md
│   │       │   ├── THREAT_MODEL.md
│   │       │   └── TRUST_BOUNDARIES.md
│   │       ├── 03_GENESIS_MODEL
│   │       │   ├── 11D_SANDBOX.md
│   │       │   ├── BANDWIDTH.md
│   │       │   ├── CHIRALITY_FABRIC.md
│   │       │   ├── DECS.md
│   │       │   ├── GENESIS_FIELD.md
│   │       │   ├── GHOSTING.md
│   │       │   ├── GUARDIAN_CDN.md
│   │       │   ├── PROPAGATION.md
│   │       │   ├── PSSP.md
│   │       │   ├── RECURSION_CONTRACT.md
│   │       │   ├── RESOLUTION.md
│   │       │   └── SYSTEMS.md
│   │       ├── 04_STATE_MODEL
│   │       │   ├── BRICK_STATES.md
│   │       │   ├── CHIRALITY_CYCLES.md
│   │       │   ├── INITIAL_STATE.md
│   │       │   ├── PROVENANCE.md
│   │       │   ├── STATE_MACHINE.md
│   │       │   ├── STATE_MODEL.md
│   │       │   ├── TRANSITIONS.md
│   │       │   ├── WIN_BRICK.md
│   │       │   └── WIN_STATE.md
│   │       ├── 05_ALGORITHMS
│   │       │   ├── ALGORITHM_CATALOG.md
│   │       │   └── ALGORITHM_TEMPLATE.md
│   │       ├── 06_PSEUDOCODE
│   │       │   ├── FLAG_LOGIC.pseudo
│   │       │   ├── GUARDIAN.pseudo
│   │       │   ├── LEVEL_CONTROLLER.pseudo
│   │       │   ├── OBJECT_INTERACTIONS.pseudo
│   │       │   └── RECURSION.pseudo
│   │       ├── 07_VISUALIZATION
│   │       │   ├── ART_HANDOFF.md
│   │       │   ├── LANDSCAPE.md
│   │       │   ├── PSSP_VIEWS.md
│   │       │   ├── STATE_TO_VISUAL_MAP.md
│   │       │   ├── VFX_EVENTS.md
│   │       │   └── VISUAL_CONTRACT.md
│   │       ├── 08_INTERACTION
│   │       │   ├── GESTURE_INTERFACE.md
│   │       │   ├── INPUT_STATE_MAP.md
│   │       │   ├── PLAYER_VERBS.md
│   │       │   ├── TERMINAL_GESTURE.md
│   │       │   └── TERMINAL_INTERFACE.md
│   │       ├── 09_FLAGS_AND_KEYS
│   │       │   ├── DECS_KEY_SPEC.md
│   │       │   ├── FLAG_KEY_SPEC.md
│   │       │   ├── FLAG_SPEC.md
│   │       │   └── PROGRESSION_EFFECTS.md
│   │       ├── 10_TESTING
│   │       │   ├── ACCEPTANCE_MATRIX.md
│   │       │   ├── ADVERSARIAL.md
│   │       │   ├── REFERENCE_RUNS.md
│   │       │   ├── REGRESSION_TESTS.md
│   │       │   └── TEST_VECTORS.json
│   │       ├── 11_DIAGRAMS
│   │       │   ├── DIAGRAM_REQUIREMENTS.md
│   │       │   ├── GENESIS_MAP.md
│   │       │   ├── LEVEL_FLOW.md
│   │       │   ├── NETWORK_MAP.md
│   │       │   ├── SEQUENCE.md
│   │       │   └── STATE_GRAPH.md
│   │       ├── 12_MACHINE_READABLE
│   │       │   ├── acceptance_registry.template.json
│   │       │   ├── algorithm_registry.template.json
│   │       │   ├── level_contract.template.json
│   │       │   ├── object_registry.template.json
│   │       │   └── state_registry.template.json
│   │       ├── 13_IMPLEMENTATION_HANDOFF
│   │       │   ├── CODEX_HANDOFF.md
│   │       │   ├── GENESIS_LANGUAGE_MAP.md
│   │       │   ├── HANDOFF.md
│   │       │   ├── PYTHON_SANDBOX_REQUIREMENTS.md
│   │       │   └── RENDER_REQUIREMENTS.md
│   │       ├── 14_PROVENANCE
│   │       │   ├── DECISIONS.md
│   │       │   ├── LEDGER.md
│   │       │   ├── OPEN_QUESTIONS.md
│   │       │   ├── SHA256SUMS.txt
│   │       │   └── SOURCE_MAP.md
│   │       ├── CONSTITUTION.md
│   │       ├── README.md
│   │       ├── TREE_STACK.md
│   │       └── WORKFLOW.md
│   ├── modules
│   │   ├── M01_GENESIS
│   │   │   └── README.md
│   │   ├── M02_CODE
│   │   │   └── README.md
│   │   ├── M03_NETWORK
│   │   │   └── README.md
│   │   ├── M04_VIRTUALIZE
│   │   │   └── README.md
│   │   ├── M05_VIRTUAL_BOXING
│   │   │   └── README.md
│   │   ├── M06_RAID
│   │   │   └── README.md
│   │   ├── M07_FLEET
│   │   │   └── README.md
│   │   ├── M08_SOVEREIGN
│   │   │   └── README.md
│   │   └── README.md
│   └── systems
│       ├── BOOT_NAVIGATION
│       │   └── .gitkeep
│       └── SHARED_SYSTEMS
│           └── .gitkeep
├── docs
│   ├── architecture
│   │   └── .gitkeep
│   ├── cybersecurity
│   │   └── .gitkeep
│   ├── design
│   │   └── .gitkeep
│   ├── diagrams
│   │   └── .gitkeep
│   ├── genesis
│   │   ├── 11D_ARCHITECTURE.md
│   │   ├── BANDWIDTH.md
│   │   ├── CHIRALITY_BYTE.md
│   │   ├── CHIRALITY_CYCLES.md
│   │   ├── CHIRALITY_FABRIC.md
│   │   ├── DECS.md
│   │   ├── GENESIS_FIELD.md
│   │   ├── GENESIS_LANGUAGE.md
│   │   ├── GHOSTING.md
│   │   ├── GUARDIAN_CDN.md
│   │   ├── PSSP.md
│   │   ├── RAINBOW_ROAD.md
│   │   ├── README.md
│   │   └── RESOLUTION.md
│   ├── glossary
│   │   └── .gitkeep
│   └── visual_language
│       └── .gitkeep
├── game
│   ├── gameplay
│   │   └── .gitkeep
│   ├── genesis
│   │   └── .gitkeep
│   ├── levels
│   │   └── .gitkeep
│   ├── networking
│   │   └── .gitkeep
│   ├── persistence
│   │   └── .gitkeep
│   ├── platform
│   │   └── .gitkeep
│   ├── rendering
│   │   └── .gitkeep
│   ├── sandbox
│   │   └── .gitkeep
│   └── security
│       └── .gitkeep
├── platform
│   ├── android
│   │   └── .gitkeep
│   ├── desktop
│   │   └── .gitkeep
│   └── ios
│       └── .gitkeep
├── provenance
│   ├── audits
│   │   ├── .gitkeep
│   │   ├── bootstrap-inventory.md
│   │   └── bootstrap-validation.txt
│   ├── checkpoints
│   │   ├── .gitkeep
│   │   └── dev.zip
│   ├── decisions
│   │   ├── .gitkeep
│   │   └── 0001-bootstrap.md
│   └── sources
│       ├── .gitkeep
│       ├── bootstrap-request.txt
│       └── dev-import.json
├── tests
│   ├── adversarial
│   │   └── .gitkeep
│   ├── integration
│   │   └── .gitkeep
│   ├── performance
│   │   └── .gitkeep
│   ├── regression
│   │   └── .gitkeep
│   └── unit
│       └── .gitkeep
└── tools
    ├── dev
    │   └── .gitkeep
    ├── exporters
    │   └── .gitkeep
    ├── generators
    │   └── .gitkeep
    └── validators
        └── validate-bootstrap.mjs
```

## Files created

- `.gitattributes`
- `.gitignore`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `PROJECT_CONSTITUTION.md`
- `README.md`
- `content/art/.gitkeep`
- `content/audio/.gitkeep`
- `content/blender/.gitkeep`
- `content/shaders/.gitkeep`
- `content/ui/.gitkeep`
- `content/vfx/.gitkeep`
- `data/algorithms/.gitkeep`
- `data/levels/.gitkeep`
- `data/objects/.gitkeep`
- `data/states/.gitkeep`
- `data/tests/.gitkeep`
- `development/checkpoints/.gitkeep`
- `development/constitution/LEVEL_XX/00_RELEASE/CHANGELOG.md`
- `development/constitution/LEVEL_XX/00_RELEASE/DEFINITION_OF_DONE.md`
- `development/constitution/LEVEL_XX/00_RELEASE/LEVEL_MANIFEST.template.json`
- `development/constitution/LEVEL_XX/00_RELEASE/README.md`
- `development/constitution/LEVEL_XX/01_DESIGN/DEPENDENCIES.md`
- `development/constitution/LEVEL_XX/01_DESIGN/LEARNING_OBJECTIVES.md`
- `development/constitution/LEVEL_XX/01_DESIGN/LEVEL_BRIEF.md`
- `development/constitution/LEVEL_XX/01_DESIGN/PLAYER_FANTASY.md`
- `development/constitution/LEVEL_XX/02_CYBERSECURITY/ASSET_MAP.md`
- `development/constitution/LEVEL_XX/02_CYBERSECURITY/ATTACK_PATHS.md`
- `development/constitution/LEVEL_XX/02_CYBERSECURITY/DEFENDER_MODEL.md`
- `development/constitution/LEVEL_XX/02_CYBERSECURITY/LANDSCAPE.md`
- `development/constitution/LEVEL_XX/02_CYBERSECURITY/THREAT_MODEL.md`
- `development/constitution/LEVEL_XX/02_CYBERSECURITY/TRUST_BOUNDARIES.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/11D_SANDBOX.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/BANDWIDTH.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/CHIRALITY_FABRIC.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/DECS.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/GENESIS_FIELD.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/GHOSTING.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/GUARDIAN_CDN.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/PROPAGATION.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/PSSP.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/RECURSION_CONTRACT.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/RESOLUTION.md`
- `development/constitution/LEVEL_XX/03_GENESIS_MODEL/SYSTEMS.md`
- `development/constitution/LEVEL_XX/04_STATE_MODEL/BRICK_STATES.md`
- `development/constitution/LEVEL_XX/04_STATE_MODEL/CHIRALITY_CYCLES.md`
- `development/constitution/LEVEL_XX/04_STATE_MODEL/INITIAL_STATE.md`
- `development/constitution/LEVEL_XX/04_STATE_MODEL/PROVENANCE.md`
- `development/constitution/LEVEL_XX/04_STATE_MODEL/STATE_MACHINE.md`
- `development/constitution/LEVEL_XX/04_STATE_MODEL/STATE_MODEL.md`
- `development/constitution/LEVEL_XX/04_STATE_MODEL/TRANSITIONS.md`
- `development/constitution/LEVEL_XX/04_STATE_MODEL/WIN_BRICK.md`
- `development/constitution/LEVEL_XX/04_STATE_MODEL/WIN_STATE.md`
- `development/constitution/LEVEL_XX/05_ALGORITHMS/ALGORITHM_CATALOG.md`
- `development/constitution/LEVEL_XX/05_ALGORITHMS/ALGORITHM_TEMPLATE.md`
- `development/constitution/LEVEL_XX/06_PSEUDOCODE/FLAG_LOGIC.pseudo`
- `development/constitution/LEVEL_XX/06_PSEUDOCODE/GUARDIAN.pseudo`
- `development/constitution/LEVEL_XX/06_PSEUDOCODE/LEVEL_CONTROLLER.pseudo`
- `development/constitution/LEVEL_XX/06_PSEUDOCODE/OBJECT_INTERACTIONS.pseudo`
- `development/constitution/LEVEL_XX/06_PSEUDOCODE/RECURSION.pseudo`
- `development/constitution/LEVEL_XX/07_VISUALIZATION/ART_HANDOFF.md`
- `development/constitution/LEVEL_XX/07_VISUALIZATION/LANDSCAPE.md`
- `development/constitution/LEVEL_XX/07_VISUALIZATION/PSSP_VIEWS.md`
- `development/constitution/LEVEL_XX/07_VISUALIZATION/STATE_TO_VISUAL_MAP.md`
- `development/constitution/LEVEL_XX/07_VISUALIZATION/VFX_EVENTS.md`
- `development/constitution/LEVEL_XX/07_VISUALIZATION/VISUAL_CONTRACT.md`
- `development/constitution/LEVEL_XX/08_INTERACTION/GESTURE_INTERFACE.md`
- `development/constitution/LEVEL_XX/08_INTERACTION/INPUT_STATE_MAP.md`
- `development/constitution/LEVEL_XX/08_INTERACTION/PLAYER_VERBS.md`
- `development/constitution/LEVEL_XX/08_INTERACTION/TERMINAL_GESTURE.md`
- `development/constitution/LEVEL_XX/08_INTERACTION/TERMINAL_INTERFACE.md`
- `development/constitution/LEVEL_XX/09_FLAGS_AND_KEYS/DECS_KEY_SPEC.md`
- `development/constitution/LEVEL_XX/09_FLAGS_AND_KEYS/FLAG_KEY_SPEC.md`
- `development/constitution/LEVEL_XX/09_FLAGS_AND_KEYS/FLAG_SPEC.md`
- `development/constitution/LEVEL_XX/09_FLAGS_AND_KEYS/PROGRESSION_EFFECTS.md`
- `development/constitution/LEVEL_XX/10_TESTING/ACCEPTANCE_MATRIX.md`
- `development/constitution/LEVEL_XX/10_TESTING/ADVERSARIAL.md`
- `development/constitution/LEVEL_XX/10_TESTING/REFERENCE_RUNS.md`
- `development/constitution/LEVEL_XX/10_TESTING/REGRESSION_TESTS.md`
- `development/constitution/LEVEL_XX/10_TESTING/TEST_VECTORS.json`
- `development/constitution/LEVEL_XX/11_DIAGRAMS/DIAGRAM_REQUIREMENTS.md`
- `development/constitution/LEVEL_XX/11_DIAGRAMS/GENESIS_MAP.md`
- `development/constitution/LEVEL_XX/11_DIAGRAMS/LEVEL_FLOW.md`
- `development/constitution/LEVEL_XX/11_DIAGRAMS/NETWORK_MAP.md`
- `development/constitution/LEVEL_XX/11_DIAGRAMS/SEQUENCE.md`
- `development/constitution/LEVEL_XX/11_DIAGRAMS/STATE_GRAPH.md`
- `development/constitution/LEVEL_XX/12_MACHINE_READABLE/acceptance_registry.template.json`
- `development/constitution/LEVEL_XX/12_MACHINE_READABLE/algorithm_registry.template.json`
- `development/constitution/LEVEL_XX/12_MACHINE_READABLE/level_contract.template.json`
- `development/constitution/LEVEL_XX/12_MACHINE_READABLE/object_registry.template.json`
- `development/constitution/LEVEL_XX/12_MACHINE_READABLE/state_registry.template.json`
- `development/constitution/LEVEL_XX/13_IMPLEMENTATION_HANDOFF/CODEX_HANDOFF.md`
- `development/constitution/LEVEL_XX/13_IMPLEMENTATION_HANDOFF/GENESIS_LANGUAGE_MAP.md`
- `development/constitution/LEVEL_XX/13_IMPLEMENTATION_HANDOFF/HANDOFF.md`
- `development/constitution/LEVEL_XX/13_IMPLEMENTATION_HANDOFF/PYTHON_SANDBOX_REQUIREMENTS.md`
- `development/constitution/LEVEL_XX/13_IMPLEMENTATION_HANDOFF/RENDER_REQUIREMENTS.md`
- `development/constitution/LEVEL_XX/14_PROVENANCE/DECISIONS.md`
- `development/constitution/LEVEL_XX/14_PROVENANCE/LEDGER.md`
- `development/constitution/LEVEL_XX/14_PROVENANCE/OPEN_QUESTIONS.md`
- `development/constitution/LEVEL_XX/14_PROVENANCE/SHA256SUMS.txt`
- `development/constitution/LEVEL_XX/14_PROVENANCE/SOURCE_MAP.md`
- `development/constitution/LEVEL_XX/CONSTITUTION.md`
- `development/constitution/LEVEL_XX/README.md`
- `development/constitution/LEVEL_XX/TREE_STACK.md`
- `development/constitution/LEVEL_XX/WORKFLOW.md`
- `development/modules/M01_GENESIS/README.md`
- `development/modules/M02_CODE/README.md`
- `development/modules/M03_NETWORK/README.md`
- `development/modules/M04_VIRTUALIZE/README.md`
- `development/modules/M05_VIRTUAL_BOXING/README.md`
- `development/modules/M06_RAID/README.md`
- `development/modules/M07_FLEET/README.md`
- `development/modules/M08_SOVEREIGN/README.md`
- `development/modules/README.md`
- `development/systems/BOOT_NAVIGATION/.gitkeep`
- `development/systems/SHARED_SYSTEMS/.gitkeep`
- `docs/architecture/.gitkeep`
- `docs/cybersecurity/.gitkeep`
- `docs/design/.gitkeep`
- `docs/diagrams/.gitkeep`
- `docs/genesis/11D_ARCHITECTURE.md`
- `docs/genesis/BANDWIDTH.md`
- `docs/genesis/CHIRALITY_BYTE.md`
- `docs/genesis/CHIRALITY_CYCLES.md`
- `docs/genesis/CHIRALITY_FABRIC.md`
- `docs/genesis/DECS.md`
- `docs/genesis/GENESIS_FIELD.md`
- `docs/genesis/GENESIS_LANGUAGE.md`
- `docs/genesis/GHOSTING.md`
- `docs/genesis/GUARDIAN_CDN.md`
- `docs/genesis/PSSP.md`
- `docs/genesis/RAINBOW_ROAD.md`
- `docs/genesis/README.md`
- `docs/genesis/RESOLUTION.md`
- `docs/glossary/.gitkeep`
- `docs/visual_language/.gitkeep`
- `game/gameplay/.gitkeep`
- `game/genesis/.gitkeep`
- `game/levels/.gitkeep`
- `game/networking/.gitkeep`
- `game/persistence/.gitkeep`
- `game/platform/.gitkeep`
- `game/rendering/.gitkeep`
- `game/sandbox/.gitkeep`
- `game/security/.gitkeep`
- `platform/android/.gitkeep`
- `platform/desktop/.gitkeep`
- `platform/ios/.gitkeep`
- `provenance/audits/.gitkeep`
- `provenance/audits/bootstrap-inventory.md`
- `provenance/audits/bootstrap-validation.txt`
- `provenance/checkpoints/.gitkeep`
- `provenance/checkpoints/dev.zip`
- `provenance/decisions/.gitkeep`
- `provenance/decisions/0001-bootstrap.md`
- `provenance/sources/.gitkeep`
- `provenance/sources/bootstrap-request.txt`
- `provenance/sources/dev-import.json`
- `tests/adversarial/.gitkeep`
- `tests/integration/.gitkeep`
- `tests/performance/.gitkeep`
- `tests/regression/.gitkeep`
- `tests/unit/.gitkeep`
- `tools/dev/.gitkeep`
- `tools/exporters/.gitkeep`
- `tools/generators/.gitkeep`
- `tools/validators/validate-bootstrap.mjs`

## Source preservation

All 87 imported constitution files retain the exact source paths below LEVEL_XX and original bytes. See dev-import.json for the complete source mapping and SHA-256 hashes. The entire source archive is preserved in provenance/checkpoints/dev.zip.
