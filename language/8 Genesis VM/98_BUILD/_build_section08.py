from pathlib import Path
import shutil, json, textwrap, hashlib, os, zipfile, subprocess, sys, struct, importlib.util, random

ROOT = Path('/mnt/data/GENESIS_CHIRALITY_MACHINE_SECTION_08_VM_IR_v0.1.0_20260821')
if ROOT.exists():
    shutil.rmtree(ROOT)
DIRS = [
'00_START_HERE','01_ARCHITECTURE','02_GIR_GRAPH_IR','03_GVM_MACHINE_MODEL','04_TYPE_SYSTEM','05_EFFECT_SYSTEM','06_ISA','07_MEMORY_MODEL','08_GRAPH_SCHEDULER','09_BYTECODE','10_VERIFIER','11_RUNTIME','12_BACKEND_ABI','13_REFERENCE_IMPLEMENTATION/genesis_vm','14_SCHEMAS','15_PSEUDOCODE','16_FAILURES','17_TESTS','18_EXAMPLES','19_REFERENCE_PROGRAMS','20_SOURCE_CROSSWALK','21_RECOVERY','98_BUILD','99_RELEASE'
]
for d in DIRS:
    (ROOT/d).mkdir(parents=True, exist_ok=True)

def w(rel, txt):
    p = ROOT/rel; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(txt).lstrip(), encoding='utf-8')

def j(rel, obj):
    p = ROOT/rel; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding='utf-8')

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

# ---------------- documentation ----------------
w('00_START_HERE/FOLDER_NAME.txt', ROOT.name+'\n')
w('00_START_HERE/README.md', r'''
# Genesis Chirality Machine — Section 08
## Genesis Virtual Machine + Graph Intermediate Representation

**Version:** 0.1.0 — bootstrap software execution model  
**Date:** 2026-08-21

Section 08 defines the machine-facing execution language that future Genesis source syntax compiles into.

It intentionally has **two internal levels**:

1. **GIR — Genesis Graph Intermediate Representation**: semantic, typed, dependency-first, relationship-first, mostly SSA-like. It represents the program as a typed relationship/dependency graph.
2. **GVM — Genesis Virtual Machine**: deterministic register/resource machine that executes a scheduled/lowered form of GIR and dispatches semantic operations to Sections 01–07 through a backend ABI.

```text
future Genesis source syntax
          |
          v
         GIR                 semantic graph IR
          |
   verify / type / effect
          |
   deterministic scheduling
          v
         GVM                 machine execution IR / bytecode
          |
     backend ABI
          |
          +--> Section 01 hardware/fabric
          +--> Section 02 Geometric instantiation
          +--> Section 03 transformation/forking
          +--> Section 04 Portal/Corridor
          +--> Section 05 Rainbow Road
          +--> Section 06 QFT/GR transduction
          +--> Section 07 quantum-information effects
          |
          v
      BRANE / Trinity / BLACKGLASS
```

### Foundational decision

Python does **not** define Genesis semantics. Python is the current bootstrap implementation of the GVM and its reference backend. The normative contract is the typed GIR/GVM model, instruction semantics, verifier rules, effects, receipts, and backend ABI contained here.

### Machine principle

The VM does not treat the base chirality fabric as an ordinary mutable heap. Section 01 remains authoritative: base fabric identity is stable; writes occur through overlays/derived state. Persistent semantic changes are represented through new Geometric states, receipts, ancestry, provenance, and closure.

### Scope

This is a software execution model and compiler bootstrap target. It does not claim custom physical hardware has been manufactured. It is designed so the Python VM can later be replaced by a native, FPGA, GPU, or custom chirality-machine backend without changing Genesis language semantics.
''')
w('00_START_HERE/RECOVERY_ORDER.md', r'''
# Recovery order

1. Mount Part A first. It contains the complete Section 08 architecture, GIR, GVM, bytecode, verifier, reference VM, tests, compiled reference programs, schemas, and recovery state.
2. Mount Part B for executable reference fixtures and the Section 06/07 integration fixtures used to exercise mixed-sector and quantum-effect lowering.
3. Mount Part C for implementation lineage: Sections 01–07 core releases, Layer Zero, prior Computational Genesis handoff, CFP, Corridor mathematics, and Rainbow Road source.
4. Mount Part D for Astraeus mathematics, API 4.3, and the QFT/GR bridge reference corpus.
5. Mount Part E for MK Ultra Tome / information / Helicon / QFT-GR reference lineage.

The future human-facing Genesis grammar is **above** Section 08. Do not infer grammar from bytecode spelling.
''')

w('01_ARCHITECTURE/ARCHITECTURE.md', r'''
# Section 08 architecture

## Two-stage execution language

Genesis needs a representation that preserves the project's native relationship/dependency semantics without forcing source programs to look like CPU assembly. It also needs a deterministic machine that can actually run those semantics on current hardware.

Therefore Section 08 separates:

### GIR — semantic graph

```text
Nodes      = typed semantic operations
Edges      = data dependency, relationship, effect ordering, closure obligation
Values     = SSA-like immutable references
Resources  = typed identity-bearing runtime resources
Blocks     = optional explicit control regions
```

GIR is the canonical compiler target for future Genesis syntax.

### GVM — execution machine

```text
Typed virtual registers
Resource table
Fabric mount table
Linear-resource ownership table
Frame/control stack
Append-only receipt ledger
Backend dispatch table
```

GVM is a deterministic lowering target and bytecode format. GVM instructions are not the ontology; they are an execution projection of GIR.

## Machine stack

```text
Genesis source (future)
        v
GIR graph
        v
Static verifier + type/effect checker
        v
Deterministic graph scheduler
        v
GVM instruction stream
        v
GVM verifier
        v
Reference VM
        v
Backend ABI
        v
Section stack 01..07
        v
BRANE / Trinity / BLACKGLASS
```

## Design law

**The program is the typed relationship graph. The instruction stream is a deterministic execution projection of that graph.**
''')
w('01_ARCHITECTURE/DESIGN_INVARIANTS.md', r'''
# Design invariants

1. GIR is graph-native; textual Genesis syntax is not required to define the machine.
2. GVM is deterministic for a fixed program, input resource set, backend version, and declared measurement seed/input.
3. Base chirality fabric is never mutated through generic VM memory stores.
4. Fabric writes require the `WRITE_OVERLAY` effect and backend support for Section 01 overlay semantics.
5. Identity-bearing resources are referenced by handles, not copied as untyped blobs.
6. Persistent transformations produce new state/ancestry; they do not silently mutate a closed parent Geometric.
7. Portal and Road execution must close or expose an explicit partial/failure frontier.
8. Sector changes require explicit `BRIDGE_SECTOR`; QFT and GR are not silently interchangeable.
9. Nonclassical quantum resources are linear. GVM move/copy rules cannot clone a live QSTATE.
10. Measurement is an explicit effect and typestate transition.
11. Provenance and closure are machine-visible results, not logging side effects.
12. Python is the bootstrap oracle, not the semantic authority.
''')

w('02_GIR_GRAPH_IR/GIR_SPEC.md', r'''
# GIR 0.1 — Genesis Graph Intermediate Representation

A GIR program is a typed directed graph of semantic operations.

## Core shape

```json
{
  "ir": "GIR",
  "version": "0.1.0",
  "name": "first_portal",
  "nodes": [
    {
      "id": "mount",
      "op": "FABRIC_MOUNT",
      "out": "%fabric",
      "type": "FABRIC",
      "args": [],
      "attrs": {"uri": "fabric://reference"}
    }
  ],
  "edges": [],
  "exports": ["%receipt"]
}
```

## Dependency semantics

Dependencies are obtained from both:

- explicit `edges` of kind `dependency` or `effect_order`;
- data references in node `args` beginning with `%`.

The compiler constructs one partial order, checks it for illegal cycles, and emits a deterministic topological schedule. Ties are resolved by node ID so compilation is reproducible.

## Why SSA-like values

A named GIR value is assigned once. Identity-bearing runtime objects can have many successor resources, but each successor receives a new value name. This directly supports append-only ancestry.

## Cycles and recursion

A dependency graph cycle is not used to mean runtime recursion. Recursion/control loops are represented through explicit basic blocks in lower GVM control flow. This keeps dependency cycles distinct from executable loops.
''')
w('02_GIR_GRAPH_IR/RELATIONSHIP_EDGES.md', r'''
# GIR relationship edges

GIR edges are typed. Initial edge kinds:

- `dependency` — execution/data prerequisite;
- `relationship` — semantic relation witness between identity-bearing resources;
- `effect_order` — ordering required because effects would otherwise commute ambiguously;
- `closure_obligation` — downstream node must close/verify the referenced transaction;
- `provenance` — source lineage edge;
- `ownership` — linear-resource movement/consumption edge.

Only `dependency` and `effect_order` directly participate in the v0.1 scheduler. Other edge kinds are preserved for verification, visualization, future optimization, and provenance.
''')
w('02_GIR_GRAPH_IR/LOWERING_RULES.md', r'''
# GIR -> GVM lowering

1. Validate GIR schema and node uniqueness.
2. Infer data dependencies from `%value` arguments.
3. Merge explicit dependency/effect-order edges.
4. Reject illegal graph cycles.
5. Topologically schedule nodes deterministically.
6. Allocate typed virtual registers to GIR outputs.
7. Lower each GIR operation to one GVM instruction in v0.1.
8. Preserve node IDs and source-map metadata.
9. Run the GVM verifier.
10. Encode deterministic bytecode and emit a content hash.

Future optimization passes may fuse or split nodes, but they must preserve declared identity, effect, closure, ownership, and provenance obligations.
''')

w('03_GVM_MACHINE_MODEL/GVM_SPEC.md', r'''
# GVM 0.1 machine model

## State

`MachineState = (PC, Registers, Resources, FabricMounts, Ownership, Frames, Ledger, BackendState)`

### Registers

The reference VM exposes 256 typed virtual registers per frame. A register contains a tagged value or a resource handle. Registers are implementation-level slots; they are not the same thing as chirality fabric cells.

### Resource table

Identity-bearing values are stored as immutable/versioned backend resources and referenced by deterministic handles. Examples: `GEOMETRIC`, `PORTAL`, `ROAD`, `BRIDGE`, `QSTATE`, `RECEIPT`.

### Fabric address space

GVM has dedicated fabric instructions. Generic register operations cannot rewrite the Section 01 base fabric. `FABRIC_WRITE_OVERLAY` delegates to the hardware ABI/overlay contract.

### Ledger

Every persistent semantic operation may emit a receipt. The VM ledger is append-only and content-hashed.

### Control flow

GVM has explicit `JUMP`, `BRANCH`, `CALL`, `RETURN`, and `HALT`. GIR v0.1 compilation focuses on acyclic semantic graphs; explicit control-flow lowering is available directly at GVM level and is reserved for the source-language frontend/compiler stage.
''')
w('03_GVM_MACHINE_MODEL/RESOURCE_TABLE.md', r'''
# Resource table

Resource handles are machine-visible references to identity-bearing objects. They carry at minimum:

- `resource_id`;
- `kind`;
- `content_hash`;
- `parent_ids`;
- `sector` when applicable;
- `typestate` / closure state;
- provenance metadata;
- backend locator.

Copying a handle does not duplicate the underlying physical or semantic resource. For linear resources such as nonclassical `QSTATE`, even handle copying is verifier-restricted.
''')
w('03_GVM_MACHINE_MODEL/DETERMINISM.md', r'''
# Determinism contract

For all non-measurement operations, the reference GVM is deterministic under canonical serialization.

Measurement must receive either:

- an external result from a physical backend; or
- an explicit deterministic reference seed/sample token in simulation.

The seed/result becomes provenance. Hidden process-global randomness is forbidden in normative execution.
''')

w('04_TYPE_SYSTEM/TYPES.md', r'''
# GVM/GIR type universe v0.1

Scalar/structural:

`VOID BOOL INT FLOAT TEXT HASH SECTOR FABRIC_ADDR REGION`

Identity/resources:

`FABRIC MMO GEOMETRIC RELATION ADMISSION TRANSFORM PORTAL ROAD BRIDGE QSTATE QRESULT M5 RECEIPT`

A future frontend may expose richer parametric types such as:

`Portal<QFT>`, `Portal<GR>`, `MMO<closed>`, `QState<owned>`, `Road<partial>`.

GVM stores those refinements as verified attributes/typestates rather than flattening them into untyped strings.
''')
w('04_TYPE_SYSTEM/TYPE_RULES.md', r'''
# Selected type rules

- `GEO_INSTANTIATE(FABRIC, REGION, MMO) -> GEOMETRIC`
- `RELATE(GEOMETRIC, GEOMETRIC|MMO|TEXT) -> RELATION`
- `ADMIT(GEOMETRIC, RELATION?) -> ADMISSION`
- `TRANSFORM(GEOMETRIC, ADMISSION) -> GEOMETRIC`
- `PORTAL_OPEN(GEOMETRIC, ADMISSION, SECTOR) -> PORTAL`
- `PORTAL_TRANSPORT(PORTAL, GEOMETRIC) -> GEOMETRIC`
- `PORTAL_CLOSE(PORTAL, GEOMETRIC) -> RECEIPT`
- `ROAD_BEGIN(GEOMETRIC) -> ROAD`
- `ROAD_APPEND(ROAD, RECEIPT) -> ROAD`
- `ROAD_CLOSE(ROAD, GEOMETRIC) -> RECEIPT`
- `BRIDGE_SECTOR(GEOMETRIC, SECTOR, SECTOR) -> BRIDGE`
- `Q_PREPARE(GEOMETRIC) -> QSTATE`
- `Q_SUPERPOSE(QSTATE) -> QSTATE`
- `Q_ENTANGLE(QSTATE, QSTATE) -> QSTATE` consuming/moving the inputs under linear rules
- `Q_CHANNEL(QSTATE) -> QSTATE`
- `Q_MEASURE(QSTATE) -> QRESULT` consuming the coherent state handle
- `BRANE_LIFT(GEOMETRIC) -> M5`
- `PROVENANCE_SEAL(any resource) -> RECEIPT`
''')

w('05_EFFECT_SYSTEM/EFFECTS.md', r'''
# Effect system

Effects are statically visible obligations.

- `READ_FABRIC`
- `WRITE_OVERLAY`
- `ALLOCATE`
- `RELATE`
- `ADMIT`
- `TRANSFORM`
- `TRANSPORT`
- `CLOSE`
- `INHERIT`
- `PROJECT`
- `TRANSDUCE`
- `MEASURE`
- `QUANTUM_LINEAR`
- `PROVENANCE`
- `CONTROL`

An instruction may carry several effects. The verifier checks sequencing rules where effects alter typestate or ownership.

`WRITE_OVERLAY` is deliberately distinct from generic memory mutation. No opcode grants unrestricted base-fabric writes.
''')
w('05_EFFECT_SYSTEM/LINEAR_AND_CLOSURE_RULES.md', r'''
# Linear and closure rules

## Linear quantum state

A QSTATE starts `OWNED`. Operations may move it, transform it into a successor, entangle it into a joint successor, or consume it through measurement. A consumed/moved source cannot be used again as if it remained independently owned.

## Portal closure

`PORTAL_OPEN` produces an open Portal. A transport may occur only through an admitted/open Portal. `PORTAL_CLOSE` emits a closure receipt. An open Portal live at `HALT` is a verifier/runtime error unless the program explicitly declares a failure/partial frontier.

## Road closure

A Road may accumulate independently closed Portal receipts. `ROAD_CLOSE` emits an end-to-end closure receipt. Partial execution is preserved as history rather than destructively rolled back.
''')

# ISA table data
ISA = [
(0x0000,'NOP','VOID','',[]),
(0x0001,'CONST','ANY','',[]),
(0x0002,'MOVE','SAME','',[]),
(0x0003,'HASH','HASH','',[]),
(0x0010,'FABRIC_MOUNT','FABRIC','READ_FABRIC',[]),
(0x0011,'FABRIC_ALLOC','REGION','ALLOCATE',['FABRIC','INT']),
(0x0012,'FABRIC_READ','ANY','READ_FABRIC',['FABRIC','FABRIC_ADDR']),
(0x0013,'FABRIC_WRITE_OVERLAY','RECEIPT','WRITE_OVERLAY',['FABRIC','FABRIC_ADDR','ANY']),
(0x0020,'GEO_INSTANTIATE','GEOMETRIC','ALLOCATE|INHERIT',['FABRIC','REGION','MMO']),
(0x0021,'GEO_FORK','GEOMETRIC','TRANSFORM|INHERIT',['GEOMETRIC']),
(0x0022,'RELATE','RELATION','RELATE',['GEOMETRIC','ANY']),
(0x0023,'ADMIT','ADMISSION','ADMIT',['GEOMETRIC']),
(0x0024,'TRANSFORM','GEOMETRIC','TRANSFORM|INHERIT',['GEOMETRIC','ADMISSION']),
(0x0025,'INHERIT','RECEIPT','INHERIT|PROVENANCE',['ANY']),
(0x0030,'PORTAL_OPEN','PORTAL','TRANSPORT',['GEOMETRIC','ADMISSION','SECTOR']),
(0x0031,'PORTAL_TRANSPORT','GEOMETRIC','TRANSPORT|INHERIT',['PORTAL','GEOMETRIC']),
(0x0032,'PORTAL_CLOSE','RECEIPT','CLOSE|PROVENANCE',['PORTAL','GEOMETRIC']),
(0x0033,'ROAD_BEGIN','ROAD','TRANSPORT',['GEOMETRIC']),
(0x0034,'ROAD_APPEND','ROAD','TRANSPORT|INHERIT',['ROAD','RECEIPT']),
(0x0035,'ROAD_CLOSE','RECEIPT','CLOSE|PROVENANCE',['ROAD','GEOMETRIC']),
(0x0040,'BRIDGE_SECTOR','BRIDGE','TRANSDUCE|PROVENANCE',['GEOMETRIC','SECTOR','SECTOR']),
(0x0050,'Q_PREPARE','QSTATE','QUANTUM_LINEAR',['GEOMETRIC']),
(0x0051,'Q_SUPERPOSE','QSTATE','QUANTUM_LINEAR',['QSTATE']),
(0x0052,'Q_ENTANGLE','QSTATE','QUANTUM_LINEAR',['QSTATE','QSTATE']),
(0x0053,'Q_CHANNEL','QSTATE','QUANTUM_LINEAR|TRANSFORM',['QSTATE']),
(0x0054,'Q_MEASURE','QRESULT','MEASURE|QUANTUM_LINEAR',['QSTATE']),
(0x0060,'BRANE_LIFT','M5','PROJECT',['GEOMETRIC']),
(0x0061,'PROVENANCE_SEAL','RECEIPT','PROVENANCE',['ANY']),
(0x0062,'ASSERT_CLOSURE','BOOL','CLOSE',['ANY']),
(0x0063,'EMIT_RECEIPT','RECEIPT','PROVENANCE',[]),
(0x0070,'JUMP','VOID','CONTROL',[]),
(0x0071,'BRANCH','VOID','CONTROL',['BOOL']),
(0x0072,'CALL','VOID','CONTROL',[]),
(0x0073,'RETURN','VOID','CONTROL',[]),
(0x0074,'HALT','VOID','CONTROL',[]),
]
rows=['| Code | Opcode | Result | Effects | Principal inputs |','|---:|---|---|---|---|']
for code,name,res,effects,inputs in ISA:
    rows.append(f'| `0x{code:04X}` | `{name}` | `{res}` | `{effects or "-"}` | `{", ".join(inputs) or "-"}` |')
w('06_ISA/ISA_TABLE.md', '# GVM ISA 0.1\n\n'+'\n'.join(rows)+'\n')
w('06_ISA/INSTRUCTION_SEMANTICS.md', r'''
# Instruction semantics notes

## Hardware/fabric group

`FABRIC_MOUNT`, `FABRIC_ALLOC`, `FABRIC_READ`, and `FABRIC_WRITE_OVERLAY` are the only direct hardware-facing instructions in v0.1. They delegate to Section 01. The write opcode means **overlay/derived-state write**, never an unrestricted rewrite of the immutable base fabric image.

## Geometric group

Instantiation and transformation instructions delegate to Sections 02–03 semantics: child states have explicit ancestry and closed parents remain immutable.

## Portal/Road group

Portal operations preserve the separation between Portal transaction and Corridor admission/routing established by Sections 04–05. Road instructions compose closed Portal receipts rather than merging all legs into one untyped mutation.

## Sector bridge

`BRIDGE_SECTOR` delegates to Section 06. It is an explicit transduction witness; it does not assert QFT=GR.

## Quantum group

QSTATE instructions delegate to Section 07 semantic contracts. They are optional sector-scoped resources and obey linear/no-cloning rules.

## Projection/provenance

BRANE lift and receipts are explicit machine operations because realization/provenance are part of the execution contract, not incidental logs.
''')

w('07_MEMORY_MODEL/MEMORY_MODEL.md', r'''
# Memory model

GVM intentionally exposes several distinct stores:

1. **Typed register file** — ephemeral execution values.
2. **Resource table** — handles to identity-bearing immutable/versioned objects.
3. **Fabric address space** — Section 01 hardware/fabric substrate.
4. **Overlay/derived state** — permitted dynamic writes over stable fabric identity.
5. **Receipt ledger** — append-only provenance/closure history.
6. **Frame stack** — control-flow implementation state.

These stores are not collapsed into one generic byte-addressable heap because doing so would erase the distinctions the earlier sections were built to preserve.
''')
w('07_MEMORY_MODEL/FABRIC_ADDRESSING.md', r'''
# Fabric addressing

GVM treats a fabric address as a typed `FABRIC_ADDR`, not an integer with implicit meaning. The backend maps it to the Section 01 Fabric Address ABI.

No normal `MOVE`, `CONST`, or control-flow instruction can create authority to write a fabric cell. Only an admitted backend call carrying the `WRITE_OVERLAY` effect can produce a fabric write receipt.
''')

w('08_GRAPH_SCHEDULER/SCHEDULER.md', r'''
# Deterministic graph scheduler

The v0.1 compiler schedules GIR as follows:

1. infer producer->consumer data dependencies;
2. add explicit `dependency` and `effect_order` edges;
3. verify all referenced producers exist;
4. run Kahn topological sort;
5. choose the lexicographically smallest node ID among simultaneously ready nodes;
6. reject remaining-cycle graphs;
7. allocate output registers in emitted order.

This gives reproducible bytecode independent of JSON node ordering.
''')
w('08_GRAPH_SCHEDULER/OPTIMIZATION_BOUNDARY.md', r'''
# Optimization boundary

Optimizations may reorder operations only when they preserve:

- data dependencies;
- declared relationship/identity obligations;
- effect ordering;
- linear ownership;
- sector bridge ordering;
- Portal/Road closure;
- provenance ancestry.

The reference compiler intentionally performs no speculative reordering beyond deterministic topological scheduling.
''')

w('09_BYTECODE/BYTECODE_FORMAT.md', r'''
# `.gvm` bytecode format v0.1

All multibyte integers are big-endian.

## File header

```text
4 bytes   magic = "GVM1"
2 bytes   major version
2 bytes   minor version
4 bytes   instruction count
4 bytes   metadata JSON length
32 bytes  SHA-256 of metadata + encoded instruction records
N bytes   canonical metadata JSON
...
```

## Instruction record

```text
2 bytes   opcode
2 bytes   output register (0xFFFF = no output)
2 bytes   argument count
2 bytes   flags
4 bytes   canonical JSON payload length
N bytes   payload {"args": [...], "attrs": {...}, "source": ...}
```

The first bytecode is deliberately transparent and auditable rather than maximally compact. A future packed encoding may be introduced without changing GIR/GVM semantics.
''')
w('09_BYTECODE/CONTENT_ADDRESSING.md', r'''
# Content addressing

Compiler output includes:

- canonical GIR hash;
- canonical GVM program hash;
- bytecode SHA-256;
- backend ABI version required;
- source-map node IDs;
- verifier result.

A bytecode decoder verifies the embedded digest before execution.
''')

w('10_VERIFIER/VERIFIER_RULES.md', r'''
# GVM verifier rules

The v0.1 verifier checks:

- valid opcodes and register range;
- register use-after-definition;
- declared output type consistency;
- source-map uniqueness where present;
- no obvious use of consumed linear QSTATE values;
- Portal open/close typestate pairing;
- Road close pairing;
- explicit sector bridge declarations where a program declares a sector transition;
- valid control-flow targets for direct GVM programs;
- HALT/RETURN structure;
- no base-fabric mutation opcode exists;
- required effect declarations match the opcode table.

The reference runtime repeats dynamic checks because external backends may reject requests based on runtime state.
''')
w('10_VERIFIER/PROOF_OBLIGATIONS.md', r'''
# Static proof obligations

Future Genesis compilation should turn these machine checks into source-level proof obligations:

- every Portal has an admissibility witness before opening;
- every open transaction resolves to closure or explicit partial failure;
- every identity-changing transform declares ancestry;
- every sector change has a bridge witness;
- every quantum measurement consumes the correct linear resource;
- every projection declares its information-loss/readout contract;
- every persistent result is provenance-addressable.
''')

w('11_RUNTIME/EXECUTION_LOOP.md', r'''
# Reference execution loop

```text
verify bytecode
initialize frame + register file
mount backend
while PC < instruction_count:
    decode instruction
    fetch typed arguments
    enforce dynamic typestate / linear rules
    dispatch semantic opcode to backend
    store typed result
    append backend receipts/provenance
    update PC/control flow
halt only when transaction closure invariants are satisfied
emit execution receipt
```

The backend is not allowed to redefine opcode meaning. It realizes the contract for a target execution environment.
''')
w('11_RUNTIME/EXECUTION_RECEIPT.md', r'''
# Execution receipt

Every completed VM run emits a receipt containing:

- program name/version/hash;
- bytecode hash;
- backend identity/version;
- executed instruction count;
- exported register/resource hashes;
- append-only operation ledger root;
- open transaction count at halt;
- verifier status;
- deterministic execution root.

This is the bridge from language execution to BLACKGLASS provenance/recovery.
''')

w('12_BACKEND_ABI/BACKEND_ABI.md', r'''
# Genesis Machine Backend ABI 0.1

The GVM backend interface is semantic, not CPU-specific.

Required capability groups:

- `fabric.*` — Section 01 mounting/address/overlay operations;
- `geometric.*` — Sections 02–03 instantiation/fork/transform;
- `portal.*` — Section 04 Portal transaction realization;
- `road.*` — Section 05 Rainbow Road composition;
- `bridge.*` — Section 06 sector transduction;
- `quantum.*` — optional Section 07 QFT quantum-information effects;
- `brane.*` — BRANE M5 projection/realization handoff;
- `provenance.*` — receipts, ancestry, closure witnesses.

A backend declares a capability bitmap. Programs requiring unsupported capabilities fail before execution.
''')
w('12_BACKEND_ABI/BACKEND_TARGETS.md', r'''
# Backend targets

The same GVM contract can be realized by:

- Python reference backend — current oracle;
- native CPU runtime;
- GPU accelerator backend;
- FPGA hardware emulator/prototype;
- custom chirality-fabric controller;
- quantum-device adapter for supported `QSTATE` subprograms;
- deterministic simulator/testing backend.

Backend replacement must not change GIR/GVM semantic meaning.
''')

# ---------------- implementation ----------------
pkg = ROOT/'13_REFERENCE_IMPLEMENTATION/genesis_vm'

w('13_REFERENCE_IMPLEMENTATION/README.md', r'''
# Reference implementation

`genesis_vm` is a zero-third-party-dependency Python bootstrap implementation of GIR compilation, GVM verification, bytecode encoding/decoding, and a deterministic semantic reference backend.

It intentionally models backend resources abstractly. It proves the execution contract can be exercised before binding every opcode directly into the larger Section 01–07 Python packages.

Run:

```bash
python -m unittest discover -s ../../17_TESTS -p 'test_*.py' -v
```
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/util.py', r'''
import hashlib, json

def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def sha256_obj(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def short_id(prefix, obj):
    return f"{prefix}-{sha256_obj(obj)[:20]}"
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/model.py', r'''
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any

class TypeTag(str, Enum):
    VOID='VOID'; BOOL='BOOL'; INT='INT'; FLOAT='FLOAT'; TEXT='TEXT'; HASH='HASH'; SECTOR='SECTOR'
    FABRIC_ADDR='FABRIC_ADDR'; REGION='REGION'; FABRIC='FABRIC'; MMO='MMO'; GEOMETRIC='GEOMETRIC'
    RELATION='RELATION'; ADMISSION='ADMISSION'; TRANSFORM='TRANSFORM'; PORTAL='PORTAL'; ROAD='ROAD'
    BRIDGE='BRIDGE'; QSTATE='QSTATE'; QRESULT='QRESULT'; M5='M5'; RECEIPT='RECEIPT'; ANY='ANY'

class Effect(str, Enum):
    READ_FABRIC='READ_FABRIC'; WRITE_OVERLAY='WRITE_OVERLAY'; ALLOCATE='ALLOCATE'; RELATE='RELATE'; ADMIT='ADMIT'
    TRANSFORM='TRANSFORM'; TRANSPORT='TRANSPORT'; CLOSE='CLOSE'; INHERIT='INHERIT'; PROJECT='PROJECT'
    TRANSDUCE='TRANSDUCE'; MEASURE='MEASURE'; QUANTUM_LINEAR='QUANTUM_LINEAR'; PROVENANCE='PROVENANCE'; CONTROL='CONTROL'

class Opcode(IntEnum):
    NOP=0x0000; CONST=0x0001; MOVE=0x0002; HASH=0x0003
    FABRIC_MOUNT=0x0010; FABRIC_ALLOC=0x0011; FABRIC_READ=0x0012; FABRIC_WRITE_OVERLAY=0x0013
    GEO_INSTANTIATE=0x0020; GEO_FORK=0x0021; RELATE=0x0022; ADMIT=0x0023; TRANSFORM=0x0024; INHERIT=0x0025
    PORTAL_OPEN=0x0030; PORTAL_TRANSPORT=0x0031; PORTAL_CLOSE=0x0032; ROAD_BEGIN=0x0033; ROAD_APPEND=0x0034; ROAD_CLOSE=0x0035
    BRIDGE_SECTOR=0x0040
    Q_PREPARE=0x0050; Q_SUPERPOSE=0x0051; Q_ENTANGLE=0x0052; Q_CHANNEL=0x0053; Q_MEASURE=0x0054
    BRANE_LIFT=0x0060; PROVENANCE_SEAL=0x0061; ASSERT_CLOSURE=0x0062; EMIT_RECEIPT=0x0063
    JUMP=0x0070; BRANCH=0x0071; CALL=0x0072; RETURN=0x0073; HALT=0x0074

@dataclass(frozen=True)
class Instruction:
    op: Opcode
    out: int | None = None
    args: tuple[int, ...] = ()
    attrs: dict[str, Any] = field(default_factory=dict)
    source: str | None = None
    result_type: TypeTag = TypeTag.ANY

@dataclass
class Program:
    name: str
    version: str = '0.1.0'
    instructions: list[Instruction] = field(default_factory=list)
    exports: list[int] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class TaggedValue:
    type: TypeTag
    value: Any
    linear_state: str | None = None

@dataclass
class ExecutionResult:
    halted: bool
    registers: dict[int, TaggedValue]
    exports: dict[int, TaggedValue]
    receipt: dict[str, Any]
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/isa.py', r'''
from .model import Opcode, TypeTag, Effect

RESULT = {
Opcode.NOP:TypeTag.VOID, Opcode.CONST:TypeTag.ANY, Opcode.MOVE:TypeTag.ANY, Opcode.HASH:TypeTag.HASH,
Opcode.FABRIC_MOUNT:TypeTag.FABRIC, Opcode.FABRIC_ALLOC:TypeTag.REGION, Opcode.FABRIC_READ:TypeTag.ANY, Opcode.FABRIC_WRITE_OVERLAY:TypeTag.RECEIPT,
Opcode.GEO_INSTANTIATE:TypeTag.GEOMETRIC, Opcode.GEO_FORK:TypeTag.GEOMETRIC, Opcode.RELATE:TypeTag.RELATION, Opcode.ADMIT:TypeTag.ADMISSION, Opcode.TRANSFORM:TypeTag.GEOMETRIC, Opcode.INHERIT:TypeTag.RECEIPT,
Opcode.PORTAL_OPEN:TypeTag.PORTAL, Opcode.PORTAL_TRANSPORT:TypeTag.GEOMETRIC, Opcode.PORTAL_CLOSE:TypeTag.RECEIPT,
Opcode.ROAD_BEGIN:TypeTag.ROAD, Opcode.ROAD_APPEND:TypeTag.ROAD, Opcode.ROAD_CLOSE:TypeTag.RECEIPT,
Opcode.BRIDGE_SECTOR:TypeTag.BRIDGE,
Opcode.Q_PREPARE:TypeTag.QSTATE, Opcode.Q_SUPERPOSE:TypeTag.QSTATE, Opcode.Q_ENTANGLE:TypeTag.QSTATE, Opcode.Q_CHANNEL:TypeTag.QSTATE, Opcode.Q_MEASURE:TypeTag.QRESULT,
Opcode.BRANE_LIFT:TypeTag.M5, Opcode.PROVENANCE_SEAL:TypeTag.RECEIPT, Opcode.ASSERT_CLOSURE:TypeTag.BOOL, Opcode.EMIT_RECEIPT:TypeTag.RECEIPT,
Opcode.JUMP:TypeTag.VOID, Opcode.BRANCH:TypeTag.VOID, Opcode.CALL:TypeTag.VOID, Opcode.RETURN:TypeTag.VOID, Opcode.HALT:TypeTag.VOID,
}
EFFECTS = {
Opcode.FABRIC_MOUNT:{Effect.READ_FABRIC}, Opcode.FABRIC_ALLOC:{Effect.ALLOCATE}, Opcode.FABRIC_READ:{Effect.READ_FABRIC}, Opcode.FABRIC_WRITE_OVERLAY:{Effect.WRITE_OVERLAY},
Opcode.GEO_INSTANTIATE:{Effect.ALLOCATE,Effect.INHERIT}, Opcode.GEO_FORK:{Effect.TRANSFORM,Effect.INHERIT}, Opcode.RELATE:{Effect.RELATE}, Opcode.ADMIT:{Effect.ADMIT}, Opcode.TRANSFORM:{Effect.TRANSFORM,Effect.INHERIT}, Opcode.INHERIT:{Effect.INHERIT,Effect.PROVENANCE},
Opcode.PORTAL_OPEN:{Effect.TRANSPORT}, Opcode.PORTAL_TRANSPORT:{Effect.TRANSPORT,Effect.INHERIT}, Opcode.PORTAL_CLOSE:{Effect.CLOSE,Effect.PROVENANCE},
Opcode.ROAD_BEGIN:{Effect.TRANSPORT}, Opcode.ROAD_APPEND:{Effect.TRANSPORT,Effect.INHERIT}, Opcode.ROAD_CLOSE:{Effect.CLOSE,Effect.PROVENANCE},
Opcode.BRIDGE_SECTOR:{Effect.TRANSDUCE,Effect.PROVENANCE},
Opcode.Q_PREPARE:{Effect.QUANTUM_LINEAR}, Opcode.Q_SUPERPOSE:{Effect.QUANTUM_LINEAR}, Opcode.Q_ENTANGLE:{Effect.QUANTUM_LINEAR}, Opcode.Q_CHANNEL:{Effect.QUANTUM_LINEAR,Effect.TRANSFORM}, Opcode.Q_MEASURE:{Effect.MEASURE,Effect.QUANTUM_LINEAR},
Opcode.BRANE_LIFT:{Effect.PROJECT}, Opcode.PROVENANCE_SEAL:{Effect.PROVENANCE}, Opcode.ASSERT_CLOSURE:{Effect.CLOSE}, Opcode.EMIT_RECEIPT:{Effect.PROVENANCE},
Opcode.JUMP:{Effect.CONTROL}, Opcode.BRANCH:{Effect.CONTROL}, Opcode.CALL:{Effect.CONTROL}, Opcode.RETURN:{Effect.CONTROL}, Opcode.HALT:{Effect.CONTROL},
}

def result_type(op): return RESULT[op]
def effects(op): return EFFECTS.get(op,set())
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/errors.py', r'''
class GenesisVMError(Exception): pass
class GIRCompileError(GenesisVMError): pass
class VerifyError(GenesisVMError): pass
class BytecodeError(GenesisVMError): pass
class RuntimeFault(GenesisVMError): pass
class LinearResourceError(RuntimeFault): pass
class ClosureError(RuntimeFault): pass
class SectorError(RuntimeFault): pass
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/graph.py', r'''
from collections import defaultdict
from .errors import GIRCompileError

def schedule_gir(gir):
    nodes = gir.get('nodes', [])
    by_id = {}
    producers = {}
    for n in nodes:
        nid=n['id']
        if nid in by_id: raise GIRCompileError(f'duplicate node id {nid}')
        by_id[nid]=n
        out=n.get('out')
        if out:
            if out in producers: raise GIRCompileError(f'duplicate value producer {out}')
            producers[out]=nid
    deps={nid:set() for nid in by_id}
    rev=defaultdict(set)
    for n in nodes:
        nid=n['id']
        for arg in n.get('args',[]):
            if isinstance(arg,str) and arg.startswith('%'):
                if arg not in producers: raise GIRCompileError(f'unknown value {arg} in {nid}')
                p=producers[arg]
                if p!=nid: deps[nid].add(p); rev[p].add(nid)
    for e in gir.get('edges',[]):
        if e.get('kind','dependency') in ('dependency','effect_order'):
            a=e['from']; b=e['to']
            if a not in by_id or b not in by_id: raise GIRCompileError(f'unknown edge {a}->{b}')
            deps[b].add(a); rev[a].add(b)
    ready=sorted([n for n,d in deps.items() if not d])
    out=[]
    while ready:
        nid=ready.pop(0); out.append(by_id[nid])
        for m in sorted(rev[nid]):
            deps[m].discard(nid)
            if not deps[m] and m not in [x['id'] for x in out] and m not in ready:
                ready.append(m); ready.sort()
    if len(out)!=len(nodes):
        remain=sorted(set(by_id)-{x['id'] for x in out})
        raise GIRCompileError(f'dependency cycle: {remain}')
    return out
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/compiler.py', r'''
from .model import Program, Instruction, Opcode, TypeTag
from .isa import result_type
from .graph import schedule_gir
from .errors import GIRCompileError
from .util import sha256_obj


def _type(x):
    try: return TypeTag(x)
    except Exception: return TypeTag.ANY

def compile_gir(gir):
    if gir.get('ir')!='GIR': raise GIRCompileError('not GIR')
    scheduled=schedule_gir(gir)
    regs={}; nextreg=0; ins=[]
    for n in scheduled:
        opname=n['op']
        try: op=Opcode[opname]
        except KeyError: raise GIRCompileError(f'unknown op {opname}')
        args=[]
        attrs=dict(n.get('attrs',{}))
        literals=[]
        for a in n.get('args',[]):
            if isinstance(a,str) and a.startswith('%'):
                args.append(regs[a])
            else:
                literals.append(a)
        if literals:
            attrs['_literal_args']=literals
        outreg=None
        rt=_type(n.get('type',result_type(op).value))
        if n.get('out'):
            outreg=nextreg; regs[n['out']]=outreg; nextreg+=1
        ins.append(Instruction(op=op,out=outreg,args=tuple(args),attrs=attrs,source=n['id'],result_type=rt))
    exports=[]
    for x in gir.get('exports',[]):
        if x not in regs: raise GIRCompileError(f'unknown export {x}')
        exports.append(regs[x])
    normalized_gir=dict(gir)
    normalized_gir['nodes']=sorted(gir.get('nodes',[]), key=lambda n:n.get('id',''))
    normalized_gir['edges']=sorted(gir.get('edges',[]), key=lambda e:(e.get('from',''),e.get('to',''),e.get('kind','')))
    md={
        'ir':'GVM','lowered_from':'GIR','gir_hash':sha256_obj(normalized_gir),'value_registers':regs,
        'source_name':gir.get('name','unnamed'),'required_backend_abi':'0.1'
    }
    p=Program(name=gir.get('name','unnamed'),version=gir.get('version','0.1.0'),instructions=ins,exports=exports,metadata=md)
    return p
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/bytecode.py', r'''
import struct, hashlib, json
from .model import Program, Instruction, Opcode, TypeTag
from .util import canonical_bytes
from .errors import BytecodeError

MAGIC=b'GVM1'; MAJOR=0; MINOR=1
HEADER=struct.Struct('>4sHHII32s')
REC=struct.Struct('>HHHHI')

def _metadata(program):
    return {
        'name':program.name,'version':program.version,'exports':program.exports,
        'metadata':program.metadata,
    }

def _payload(i):
    return {'args':list(i.args),'attrs':i.attrs,'source':i.source,'result_type':i.result_type.value}

def encode(program):
    meta=canonical_bytes(_metadata(program)); records=[]
    for i in program.instructions:
        pl=canonical_bytes(_payload(i)); out=0xFFFF if i.out is None else i.out
        records.append(REC.pack(int(i.op),out,len(i.args),0,len(pl))+pl)
    body=meta+b''.join(records); digest=hashlib.sha256(body).digest()
    return HEADER.pack(MAGIC,MAJOR,MINOR,len(program.instructions),len(meta),digest)+body

def decode(data):
    if len(data)<HEADER.size: raise BytecodeError('truncated header')
    magic,maj,minr,count,mlen,digest=HEADER.unpack(data[:HEADER.size])
    if magic!=MAGIC: raise BytecodeError('bad magic')
    if (maj,minr)!=(MAJOR,MINOR): raise BytecodeError('unsupported version')
    body=data[HEADER.size:]
    if hashlib.sha256(body).digest()!=digest: raise BytecodeError('digest mismatch')
    if len(body)<mlen: raise BytecodeError('truncated metadata')
    md=json.loads(body[:mlen]); pos=mlen; ins=[]
    for _ in range(count):
        if pos+REC.size>len(body): raise BytecodeError('truncated record')
        op,out,argc,flags,plen=REC.unpack(body[pos:pos+REC.size]); pos+=REC.size
        if pos+plen>len(body): raise BytecodeError('truncated payload')
        p=json.loads(body[pos:pos+plen]); pos+=plen
        args=tuple(p.get('args',[]))
        if len(args)!=argc: raise BytecodeError('argc mismatch')
        try: opcode=Opcode(op)
        except ValueError: raise BytecodeError(f'unknown opcode {op}')
        ins.append(Instruction(opcode,None if out==0xFFFF else out,args,p.get('attrs',{}),p.get('source'),TypeTag(p.get('result_type','ANY'))))
    if pos!=len(body): raise BytecodeError('trailing bytes')
    return Program(md['name'],md.get('version','0.1.0'),ins,list(md.get('exports',[])),dict(md.get('metadata',{})))
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/disasm.py', r'''
import json

def disassemble(program):
    lines=[]
    for pc,i in enumerate(program.instructions):
        out='-' if i.out is None else f'r{i.out}:{i.result_type.value}'
        args=','.join(f'r{x}' for x in i.args)
        attrs=json.dumps(i.attrs,sort_keys=True,separators=(',',':'))
        src=f' ; {i.source}' if i.source else ''
        lines.append(f'{pc:04d} {out:<18} {i.op.name:<22} [{args}] {attrs}{src}')
    return '\n'.join(lines)+'\n'
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/verifier.py', r'''
from .model import Opcode, TypeTag
from .isa import result_type
from .errors import VerifyError

CONTROL={Opcode.JUMP,Opcode.BRANCH,Opcode.CALL,Opcode.RETURN,Opcode.HALT}

def verify(program):
    defined=set(); types={}; qstate_live={}; portals={}; roads={}
    for pc,i in enumerate(program.instructions):
        if i.out is not None and not (0<=i.out<256): raise VerifyError(f'pc {pc}: output register out of range')
        for r in i.args:
            if r not in defined: raise VerifyError(f'pc {pc}: use before define r{r}')
        if i.out is not None and i.out in defined: raise VerifyError(f'pc {pc}: register redefinition r{i.out}')
        expected=result_type(i.op)
        if i.out is not None and expected not in (TypeTag.ANY,TypeTag.VOID) and i.result_type not in (expected,TypeTag.ANY):
            raise VerifyError(f'pc {pc}: result type {i.result_type} != {expected}')
        if i.op==Opcode.Q_MEASURE:
            if not i.args: raise VerifyError('Q_MEASURE missing qstate')
            q=i.args[0]
            if not qstate_live.get(q,False): raise VerifyError(f'pc {pc}: QSTATE r{q} not live')
            qstate_live[q]=False
        elif i.op in (Opcode.Q_SUPERPOSE,Opcode.Q_CHANNEL):
            if not i.args: raise VerifyError(f'{i.op.name} missing qstate')
            q=i.args[0]
            if not qstate_live.get(q,False): raise VerifyError(f'pc {pc}: QSTATE r{q} not live')
            qstate_live[q]=False
        elif i.op==Opcode.Q_ENTANGLE:
            if len(i.args)<2: raise VerifyError('Q_ENTANGLE requires two qstates')
            for q in i.args[:2]:
                if not qstate_live.get(q,False): raise VerifyError(f'pc {pc}: QSTATE r{q} not live')
                qstate_live[q]=False
        if i.op==Opcode.PORTAL_OPEN and i.out is not None: portals[i.out]='OPEN'
        if i.op==Opcode.PORTAL_CLOSE:
            p=i.args[0]
            if portals.get(p)!='OPEN': raise VerifyError(f'pc {pc}: portal r{p} is not OPEN')
            portals[p]='CLOSED'
        if i.op==Opcode.ROAD_BEGIN and i.out is not None: roads[i.out]='OPEN'
        if i.op==Opcode.ROAD_APPEND:
            r=i.args[0]
            if roads.get(r)!='OPEN': raise VerifyError(f'pc {pc}: road r{r} is not OPEN')
            roads[r]='MOVED'
        if i.op==Opcode.ROAD_CLOSE:
            r=i.args[0]
            if roads.get(r)!='OPEN': raise VerifyError(f'pc {pc}: road r{r} is not OPEN')
            roads[r]='CLOSED'
        if i.out is not None:
            defined.add(i.out); types[i.out]=i.result_type
            if i.result_type==TypeTag.QSTATE: qstate_live[i.out]=True
            if i.op==Opcode.ROAD_APPEND: roads[i.out]='OPEN'
        if i.op in (Opcode.JUMP,Opcode.CALL):
            t=i.attrs.get('target')
            if not isinstance(t,int) or not (0<=t<len(program.instructions)): raise VerifyError(f'pc {pc}: invalid target')
        if i.op==Opcode.BRANCH:
            for key in ('true','false'):
                t=i.attrs.get(key)
                if not isinstance(t,int) or not (0<=t<len(program.instructions)): raise VerifyError(f'pc {pc}: invalid branch {key}')
    openp=[r for r,s in portals.items() if s=='OPEN']
    openr=[r for r,s in roads.items() if s=='OPEN']
    if openp: raise VerifyError(f'unclosed portals: {openp}')
    if openr: raise VerifyError(f'unclosed roads: {openr}')
    for e in program.exports:
        if e not in defined: raise VerifyError(f'undefined export r{e}')
    return {'ok':True,'registers':len(defined),'instructions':len(program.instructions),'exports':list(program.exports)}
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/backend.py', r'''
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .util import short_id, sha256_obj
from .errors import RuntimeFault, ClosureError, SectorError

@dataclass
class ReferenceBackend:
    backend_id: str='python-reference-backend'
    version: str='0.1.0'
    resources: dict[str,dict[str,Any]]=field(default_factory=dict)
    ledger: list[dict[str,Any]]=field(default_factory=list)
    overlay: dict[tuple[str,str],Any]=field(default_factory=dict)

    def _put(self, kind, payload, parents=(), sector=None, typestate='CLOSED'):
        body={'kind':kind,'payload':payload,'parents':list(parents),'sector':sector,'typestate':typestate}
        rid=short_id(kind.lower(),body)
        res={'resource_id':rid,**body,'content_hash':sha256_obj(body)}
        self.resources[rid]=res
        return res
    def _receipt(self, op, payload, parents=()):
        rec=self._put('RECEIPT',{'op':op,**payload},parents=parents,typestate='CLOSED')
        self.ledger.append(rec)
        return rec
    def mount_fabric(self, uri): return self._put('FABRIC',{'uri':uri,'immutable_base':True})
    def alloc(self, fabric, cells): return self._put('REGION',{'fabric':fabric['resource_id'],'cells':int(cells)},parents=[fabric['resource_id']])
    def read_fabric(self, fabric, addr):
        key=(fabric['resource_id'],str(addr)); return self.overlay.get(key, {'base':'reference','addr':addr})
    def write_overlay(self, fabric, addr, value):
        key=(fabric['resource_id'],str(addr)); self.overlay[key]=value
        return self._receipt('FABRIC_WRITE_OVERLAY',{'fabric':fabric['resource_id'],'addr':addr,'value_hash':sha256_obj(value)},[fabric['resource_id']])
    def instantiate(self, fabric, region, mmo):
        return self._put('GEOMETRIC',{'mmo':mmo,'fabric':fabric['resource_id'],'region':region['resource_id'],'closed':True},[fabric['resource_id'],region['resource_id']])
    def fork(self, geo, attrs):
        return self._put('GEOMETRIC',{'fork_of':geo['resource_id'],'attrs':attrs,'closed':True},[geo['resource_id']],sector=geo.get('sector'))
    def relate(self, geo, target, attrs): return self._put('RELATION',{'source':geo['resource_id'],'target':target,'attrs':attrs},[geo['resource_id']])
    def admit(self, geo, attrs): return self._put('ADMISSION',{'source':geo['resource_id'],'attrs':attrs,'admitted':attrs.get('admitted',True)},[geo['resource_id']])
    def transform(self, geo, admission, attrs):
        if not admission['payload'].get('admitted'): raise RuntimeFault('TRANSFORM_INADMISSIBLE')
        return self._put('GEOMETRIC',{'parent':geo['resource_id'],'transform':attrs,'closed':True},[geo['resource_id'],admission['resource_id']],sector=geo.get('sector'))
    def inherit(self, resource, attrs): return self._receipt('INHERIT',{'resource':resource['resource_id'],'attrs':attrs},[resource['resource_id']])
    def portal_open(self, geo, admission, sector, attrs):
        if not admission['payload'].get('admitted'): raise RuntimeFault('PORTAL_INADMISSIBLE')
        return self._put('PORTAL',{'source':geo['resource_id'],'admission':admission['resource_id'],'attrs':attrs},[geo['resource_id'],admission['resource_id']],sector=sector,typestate='OPEN')
    def portal_transport(self, portal, geo, attrs):
        if portal['typestate']!='OPEN': raise ClosureError('portal not open')
        sector=portal.get('sector')
        return self._put('GEOMETRIC',{'transported_from':geo['resource_id'],'portal':portal['resource_id'],'closed':True,'attrs':attrs},[geo['resource_id'],portal['resource_id']],sector=sector)
    def portal_close(self, portal, dest):
        if portal['typestate']!='OPEN': raise ClosureError('portal already closed')
        portal['typestate']='CLOSED'
        return self._receipt('PORTAL_CLOSE',{'portal':portal['resource_id'],'destination':dest['resource_id'],'sector':portal.get('sector')},[portal['resource_id'],dest['resource_id']])
    def road_begin(self, geo, attrs): return self._put('ROAD',{'source':geo['resource_id'],'legs':[],'attrs':attrs},[geo['resource_id']],typestate='OPEN')
    def road_append(self, road, receipt):
        if road['typestate']!='OPEN': raise ClosureError('road not open')
        legs=list(road['payload']['legs'])+[receipt['resource_id']]
        # Road values are persistent/versioned; original road remains valid history.
        return self._put('ROAD',{'source':road['payload']['source'],'legs':legs,'attrs':road['payload'].get('attrs',{})},[road['resource_id'],receipt['resource_id']],typestate='OPEN')
    def road_close(self, road, geo):
        if road['typestate']!='OPEN': raise ClosureError('road not open')
        road['typestate']='CLOSED'
        return self._receipt('ROAD_CLOSE',{'road':road['resource_id'],'destination':geo['resource_id'],'legs':road['payload']['legs']},[road['resource_id'],geo['resource_id']])
    def bridge(self, geo, from_sector, to_sector, attrs):
        if from_sector==to_sector: raise SectorError('bridge requires sector change')
        return self._put('BRIDGE',{'geometric':geo['resource_id'],'from':from_sector,'to':to_sector,'attrs':attrs},[geo['resource_id']],sector=to_sector)
    def q_prepare(self, geo, attrs): return self._put('QSTATE',{'geometric':geo['resource_id'],'state':'PREPARED','attrs':attrs},[geo['resource_id']],sector='QFT',typestate='OWNED')
    def q_successor(self, op, states, attrs):
        for s in states:
            if s['typestate']!='OWNED': raise RuntimeFault('QSTATE_NOT_OWNED')
        for s in states: s['typestate']='MOVED'
        return self._put('QSTATE',{'op':op,'inputs':[s['resource_id'] for s in states],'attrs':attrs},[s['resource_id'] for s in states],sector='QFT',typestate='OWNED')
    def q_measure(self, state, attrs):
        if state['typestate']!='OWNED': raise RuntimeFault('QSTATE_NOT_OWNED')
        state['typestate']='MEASURED'
        outcome=attrs.get('outcome',0)
        return self._put('QRESULT',{'state':state['resource_id'],'outcome':outcome,'classical':True},[state['resource_id']],sector='QFT')
    def brane_lift(self, geo, attrs): return self._put('M5',{'geometric':geo['resource_id'],'I':geo['resource_id'],'D':attrs.get('D','derived'),'Chi':attrs.get('Chi','preserved'),'R':attrs.get('R','history'),'P':attrs.get('P','ledger')},[geo['resource_id']])
    def provenance_seal(self, resource, attrs): return self._receipt('PROVENANCE_SEAL',{'resource':resource['resource_id'],'attrs':attrs},[resource['resource_id']])
    def assert_closure(self, resource):
        return resource.get('typestate') in ('CLOSED','MEASURED') or bool(resource.get('payload',{}).get('closed'))
    def execution_receipt(self, payload): return self._receipt('GVM_EXECUTION',payload)
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/runtime.py', r'''
from __future__ import annotations
from .model import Opcode, TypeTag, TaggedValue, ExecutionResult
from .verifier import verify
from .backend import ReferenceBackend
from .util import sha256_obj
from .errors import RuntimeFault, ClosureError

class VM:
    def __init__(self, backend=None): self.backend=backend or ReferenceBackend()
    def run(self, program, max_steps=100000):
        vr=verify(program)
        regs={}; pc=0; steps=0; stack=[]; halted=False; open_portals=set(); open_roads=set()
        def get(r):
            if r not in regs: raise RuntimeFault(f'uninitialized r{r}')
            return regs[r]
        def resource(r): return get(r).value
        while pc < len(program.instructions):
            if steps>=max_steps: raise RuntimeFault('step limit')
            i=program.instructions[pc]; steps+=1; advance=True; out=None; typ=i.result_type
            lit=i.attrs.get('_literal_args',[])
            if i.op==Opcode.NOP: pass
            elif i.op==Opcode.CONST:
                out=i.attrs.get('value', lit[0] if lit else None)
            elif i.op==Opcode.MOVE:
                v=get(i.args[0]); out=v.value; typ=v.type
                if v.type==TypeTag.QSTATE: raise RuntimeFault('QSTATE cannot use generic MOVE')
            elif i.op==Opcode.HASH: out=sha256_obj(get(i.args[0]).value); typ=TypeTag.HASH
            elif i.op==Opcode.FABRIC_MOUNT: out=self.backend.mount_fabric(i.attrs.get('uri','fabric://reference'))
            elif i.op==Opcode.FABRIC_ALLOC:
                cells=i.attrs.get('cells',lit[0] if lit else 1); out=self.backend.alloc(resource(i.args[0]),cells)
            elif i.op==Opcode.FABRIC_READ:
                addr=i.attrs.get('addr',lit[0] if lit else '0'); out=self.backend.read_fabric(resource(i.args[0]),addr)
            elif i.op==Opcode.FABRIC_WRITE_OVERLAY:
                addr=i.attrs.get('addr',lit[0] if lit else '0'); value=i.attrs.get('value',lit[1] if len(lit)>1 else None); out=self.backend.write_overlay(resource(i.args[0]),addr,value)
            elif i.op==Opcode.GEO_INSTANTIATE:
                mmo=i.attrs.get('mmo',lit[0] if lit else {'handle':'@anonymous'}); out=self.backend.instantiate(resource(i.args[0]),resource(i.args[1]),mmo)
            elif i.op==Opcode.GEO_FORK: out=self.backend.fork(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.RELATE:
                target=resource(i.args[1]) if len(i.args)>1 else i.attrs.get('target',lit[0] if lit else 'environment'); out=self.backend.relate(resource(i.args[0]),target,i.attrs)
            elif i.op==Opcode.ADMIT: out=self.backend.admit(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.TRANSFORM: out=self.backend.transform(resource(i.args[0]),resource(i.args[1]),i.attrs)
            elif i.op==Opcode.INHERIT: out=self.backend.inherit(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.PORTAL_OPEN:
                sector=i.attrs.get('sector',lit[0] if lit else 'GENERIC'); out=self.backend.portal_open(resource(i.args[0]),resource(i.args[1]),sector,i.attrs); open_portals.add(out['resource_id'])
            elif i.op==Opcode.PORTAL_TRANSPORT: out=self.backend.portal_transport(resource(i.args[0]),resource(i.args[1]),i.attrs)
            elif i.op==Opcode.PORTAL_CLOSE:
                p=resource(i.args[0]); out=self.backend.portal_close(p,resource(i.args[1])); open_portals.discard(p['resource_id'])
            elif i.op==Opcode.ROAD_BEGIN:
                out=self.backend.road_begin(resource(i.args[0]),i.attrs); open_roads.add(out['resource_id'])
            elif i.op==Opcode.ROAD_APPEND:
                old=resource(i.args[0]); out=self.backend.road_append(old,resource(i.args[1])); open_roads.discard(old['resource_id']); open_roads.add(out['resource_id'])
            elif i.op==Opcode.ROAD_CLOSE:
                road=resource(i.args[0]); out=self.backend.road_close(road,resource(i.args[1])); open_roads.discard(road['resource_id'])
            elif i.op==Opcode.BRIDGE_SECTOR:
                fs=i.attrs.get('from'); ts=i.attrs.get('to'); out=self.backend.bridge(resource(i.args[0]),fs,ts,i.attrs)
            elif i.op==Opcode.Q_PREPARE: out=self.backend.q_prepare(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.Q_SUPERPOSE: out=self.backend.q_successor('SUPERPOSE',[resource(i.args[0])],i.attrs)
            elif i.op==Opcode.Q_ENTANGLE: out=self.backend.q_successor('ENTANGLE',[resource(i.args[0]),resource(i.args[1])],i.attrs)
            elif i.op==Opcode.Q_CHANNEL: out=self.backend.q_successor('CHANNEL',[resource(i.args[0])],i.attrs)
            elif i.op==Opcode.Q_MEASURE: out=self.backend.q_measure(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.BRANE_LIFT: out=self.backend.brane_lift(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.PROVENANCE_SEAL: out=self.backend.provenance_seal(resource(i.args[0]),i.attrs)
            elif i.op==Opcode.ASSERT_CLOSURE:
                out=self.backend.assert_closure(resource(i.args[0])); typ=TypeTag.BOOL
                if not out and i.attrs.get('required',True): raise ClosureError('closure assertion failed')
            elif i.op==Opcode.EMIT_RECEIPT:
                payload={'program':program.name,'pc':pc,'ledger_root':sha256_obj([x['resource_id'] for x in self.backend.ledger])}; out=self.backend.execution_receipt(payload)
            elif i.op==Opcode.JUMP: pc=i.attrs['target']; advance=False
            elif i.op==Opcode.BRANCH:
                cond=bool(get(i.args[0]).value); pc=i.attrs['true'] if cond else i.attrs['false']; advance=False
            elif i.op==Opcode.CALL: stack.append(pc+1); pc=i.attrs['target']; advance=False
            elif i.op==Opcode.RETURN:
                if not stack: halted=True; break
                pc=stack.pop(); advance=False
            elif i.op==Opcode.HALT: halted=True; break
            else: raise RuntimeFault(f'unimplemented {i.op.name}')
            if i.out is not None: regs[i.out]=TaggedValue(typ,out)
            if advance: pc+=1
        if open_portals: raise ClosureError(f'open portal resources at halt: {sorted(open_portals)}')
        if open_roads: raise ClosureError(f'open road resources at halt: {sorted(open_roads)}')
        exports={r:regs[r] for r in program.exports}
        receipt=self.backend.execution_receipt({
            'program':program.name,'version':program.version,'steps':steps,'verified':vr['ok'],
            'exports':{str(r):sha256_obj(regs[r].value) for r in program.exports},
            'ledger_root':sha256_obj([x['resource_id'] for x in self.backend.ledger]),
            'open_portals':0,'open_roads':0,
        })
        return ExecutionResult(halted=halted or pc>=len(program.instructions),registers=regs,exports=exports,receipt=receipt)
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/assembler.py', r'''
from .model import Program, Instruction, Opcode, TypeTag

def assemble(obj):
    ins=[]
    for x in obj['instructions']:
        ins.append(Instruction(
            Opcode[x['op']],x.get('out'),tuple(x.get('args',[])),dict(x.get('attrs',{})),x.get('source'),TypeTag(x.get('result_type','ANY'))
        ))
    return Program(obj.get('name','assembled'),obj.get('version','0.1.0'),ins,list(obj.get('exports',[])),dict(obj.get('metadata',{})))
''')

w('13_REFERENCE_IMPLEMENTATION/genesis_vm/__init__.py', r'''
from .model import *
from .compiler import compile_gir
from .bytecode import encode, decode
from .verifier import verify
from .runtime import VM
from .backend import ReferenceBackend
from .disasm import disassemble
from .assembler import assemble
''')

# CLI
w('13_REFERENCE_IMPLEMENTATION/genesis_vm/__main__.py', r'''
import argparse, json, pathlib
from . import compile_gir, encode, decode, verify, VM, disassemble

def main():
    ap=argparse.ArgumentParser(prog='genesis_vm')
    sp=ap.add_subparsers(dest='cmd',required=True)
    c=sp.add_parser('compile'); c.add_argument('gir'); c.add_argument('-o','--out',required=True)
    d=sp.add_parser('disasm'); d.add_argument('gvm')
    v=sp.add_parser('verify'); v.add_argument('gvm')
    r=sp.add_parser('run'); r.add_argument('gvm')
    a=ap.parse_args()
    if a.cmd=='compile':
        gir=json.loads(pathlib.Path(a.gir).read_text()); p=compile_gir(gir); verify(p); pathlib.Path(a.out).write_bytes(encode(p))
    elif a.cmd=='disasm': print(disassemble(decode(pathlib.Path(a.gvm).read_bytes())),end='')
    elif a.cmd=='verify': print(json.dumps(verify(decode(pathlib.Path(a.gvm).read_bytes())),indent=2))
    elif a.cmd=='run':
        res=VM().run(decode(pathlib.Path(a.gvm).read_bytes())); print(json.dumps(res.receipt,indent=2,sort_keys=True))
if __name__=='__main__': main()
''')

# Schemas
j('14_SCHEMAS/gir.schema.json', {
'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Genesis GIR 0.1','type':'object','required':['ir','version','name','nodes'],
'properties':{
'ir':{'const':'GIR'},'version':{'type':'string'},'name':{'type':'string'},
'nodes':{'type':'array','items':{'type':'object','required':['id','op'],'properties':{'id':{'type':'string'},'op':{'type':'string'},'out':{'type':'string'},'type':{'type':'string'},'args':{'type':'array'},'attrs':{'type':'object'}}}},
'edges':{'type':'array'},'exports':{'type':'array','items':{'type':'string'}}}
})
j('14_SCHEMAS/execution_receipt.schema.json', {
'$schema':'https://json-schema.org/draft/2020-12/schema','title':'GVM execution receipt','type':'object','required':['resource_id','kind','payload','content_hash'],
'properties':{'resource_id':{'type':'string'},'kind':{'const':'RECEIPT'},'payload':{'type':'object'},'content_hash':{'type':'string'}}
})
j('14_SCHEMAS/backend_capabilities.schema.json', {
'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Genesis backend capabilities','type':'object','required':['backend_id','abi','capabilities'],
'properties':{'backend_id':{'type':'string'},'abi':{'type':'string'},'capabilities':{'type':'array','items':{'type':'string'}}}
})
j('14_SCHEMAS/gvm_instruction.schema.json', {
'$schema':'https://json-schema.org/draft/2020-12/schema','title':'GVM instruction JSON assembly','type':'object','required':['op'],
'properties':{'op':{'type':'string'},'out':{'type':['integer','null']},'args':{'type':'array','items':{'type':'integer'}},'attrs':{'type':'object'},'source':{'type':['string','null']},'result_type':{'type':'string'}}
})

# Pseudocode/failures
w('15_PSEUDOCODE/COMPILE_GIR.txt', r'''
COMPILE_GIR(gir):
  validate schema
  producers := map output value -> node
  dependencies := explicit dependencies + inferred data dependencies
  schedule := deterministic_topological_sort(dependencies)
  for node in schedule:
      allocate fresh typed register for node.out
      lower node.op -> GVM opcode
      preserve source node id
  verify GVM
  encode bytecode
  return bytecode + source map + hashes
''')
w('15_PSEUDOCODE/GVM_EXECUTE.txt', r'''
EXECUTE(program, backend):
  VERIFY(program)
  state := new machine state
  while not HALT:
      i := FETCH(PC)
      args := typed register lookup
      enforce ownership / closure / sector typestate
      result := BACKEND_DISPATCH(i.op, args, i.attrs)
      append receipts
      write result register
      update PC
  reject open Portal/Road transaction frontier unless explicit partial result
  emit execution receipt
''')
w('15_PSEUDOCODE/FIRST_PORTAL.txt', r'''
mount fabric
allocate region
instantiate MMO -> Geometric
relate Geometric to environment
admit transformation/transport
transform -> child Geometric
open Portal
transport child -> destination Geometric
close Portal -> receipt
lift destination -> BRANE M5
seal provenance
assert closure
emit execution receipt
''')

w('16_FAILURES/FAILURE_TAXONOMY.md', r'''
# Section 08 failure taxonomy

Compiler/verifier:

- `GIR_UNKNOWN_VALUE`
- `GIR_DUPLICATE_VALUE`
- `GIR_DEPENDENCY_CYCLE`
- `GVM_UNKNOWN_OPCODE`
- `GVM_USE_BEFORE_DEFINE`
- `GVM_REGISTER_REDEFINITION`
- `GVM_TYPE_MISMATCH`
- `GVM_INVALID_CONTROL_TARGET`
- `GVM_LINEAR_RESOURCE_REUSE`
- `GVM_UNCLOSED_PORTAL`
- `GVM_UNCLOSED_ROAD`

Runtime/backend:

- `BACKEND_CAPABILITY_MISSING`
- `FABRIC_WRITE_NOT_OVERLAY`
- `ADMISSION_FAILED`
- `PORTAL_INADMISSIBLE`
- `PORTAL_NOT_OPEN`
- `ROAD_NOT_OPEN`
- `SECTOR_BRIDGE_REQUIRED`
- `QSTATE_NOT_OWNED`
- `CLOSURE_ASSERTION_FAILED`
- `PROVENANCE_SEAL_FAILED`

Failures preserve any already-committed immutable history; they do not imply destructive rollback of earlier closed transactions.
''')

# Examples GIR helper
def node(id,op,out=None,type=None,args=None,attrs=None):
    d={'id':id,'op':op}
    if out is not None: d['out']=out
    if type is not None: d['type']=type
    if args: d['args']=args
    if attrs: d['attrs']=attrs
    return d

first_portal={
'ir':'GIR','version':'0.1.0','name':'first_portal','nodes':[
node('01_mount','FABRIC_MOUNT','%fabric','FABRIC',attrs={'uri':'fabric://chirality/reference-v1'}),
node('02_alloc','FABRIC_ALLOC','%region','REGION',['%fabric'],{'cells':4096}),
node('03_instantiate','GEO_INSTANTIATE','%g0','GEOMETRIC',['%fabric','%region'],{'mmo':{'handle':'@hydrogen_reference','class':'MMO'}}),
node('04_relate','RELATE','%rel','RELATION',['%g0'],{'target':'environment://trinity'}),
node('05_admit','ADMIT','%adm','ADMISSION',['%g0'],{'admitted':True,'resolution':1.0,'bandwidth':1.0}),
node('06_transform','TRANSFORM','%g1','GEOMETRIC',['%g0','%adm'],{'kind':'identity-preserving-reference-transform'}),
node('07_portal_open','PORTAL_OPEN','%p','PORTAL',['%g1','%adm'],{'sector':'GR','corridor':'corridor://red-violet'}),
node('08_transport','PORTAL_TRANSPORT','%g2','GEOMETRIC',['%p','%g1'],{'destination':'trinity://node-B'}),
node('09_close','PORTAL_CLOSE','%pc','RECEIPT',['%p','%g2']),
node('10_lift','BRANE_LIFT','%m5','M5',['%g2'],{'D':'portal-history','Chi':'preserved','R':'closed','P':'receipt-ledger'}),
node('11_seal','PROVENANCE_SEAL','%seal','RECEIPT',['%g2'],{'label':'first-portal'}),
node('12_assert','ASSERT_CLOSURE','%closed','BOOL',['%g2'],{'required':True}),
node('13_receipt','EMIT_RECEIPT','%receipt','RECEIPT',attrs={'label':'Genesis Bootstrap 0 — The First Portal'}),
], 'edges':[{'from':'09_close','to':'13_receipt','kind':'effect_order'},{'from':'11_seal','to':'13_receipt','kind':'effect_order'}], 'exports':['%g2','%pc','%m5','%receipt']}

rainbow={
'ir':'GIR','version':'0.1.0','name':'rainbow_road_two_leg','nodes':[
node('01_mount','FABRIC_MOUNT','%fabric','FABRIC',attrs={'uri':'fabric://chirality/reference-v1'}),
node('02_alloc','FABRIC_ALLOC','%region','REGION',['%fabric'],{'cells':8192}),
node('03_g0','GEO_INSTANTIATE','%g0','GEOMETRIC',['%fabric','%region'],{'mmo':{'handle':'@oxygen_reference','class':'MMO'}}),
node('04_road','ROAD_BEGIN','%road0','ROAD',['%g0'],{'name':'RR-OXYGEN-01'}),
node('05_adm1','ADMIT','%a1','ADMISSION',['%g0'],{'admitted':True}),
node('06_p1','PORTAL_OPEN','%p1','PORTAL',['%g0','%a1'],{'sector':'GR','corridor':'Red->Orange'}),
node('07_t1','PORTAL_TRANSPORT','%g1','GEOMETRIC',['%p1','%g0'],{'destination':'Orange'}),
node('08_c1','PORTAL_CLOSE','%c1','RECEIPT',['%p1','%g1']),
node('09_ra1','ROAD_APPEND','%road1','ROAD',['%road0','%c1']),
node('10_adm2','ADMIT','%a2','ADMISSION',['%g1'],{'admitted':True}),
node('11_p2','PORTAL_OPEN','%p2','PORTAL',['%g1','%a2'],{'sector':'GR','corridor':'Orange->Violet'}),
node('12_t2','PORTAL_TRANSPORT','%g2','GEOMETRIC',['%p2','%g1'],{'destination':'Violet'}),
node('13_c2','PORTAL_CLOSE','%c2','RECEIPT',['%p2','%g2']),
node('14_ra2','ROAD_APPEND','%road2','ROAD',['%road1','%c2']),
node('15_rc','ROAD_CLOSE','%road_receipt','RECEIPT',['%road2','%g2']),
node('16_m5','BRANE_LIFT','%m5','M5',['%g2'],{'R':'rainbow-road-history'}),
node('17_receipt','EMIT_RECEIPT','%receipt','RECEIPT'),
], 'edges':[{'from':'15_rc','to':'17_receipt','kind':'effect_order'}], 'exports':['%g2','%road_receipt','%m5','%receipt']}

mixed={
'ir':'GIR','version':'0.1.0','name':'mixed_sector_bridge','nodes':[
node('01_mount','FABRIC_MOUNT','%fabric','FABRIC',attrs={'uri':'fabric://chirality/reference-v1'}),
node('02_alloc','FABRIC_ALLOC','%region','REGION',['%fabric'],{'cells':16384}),
node('03_g0','GEO_INSTANTIATE','%g0','GEOMETRIC',['%fabric','%region'],{'mmo':{'handle':'@virus_hsv1_reference','class':'MMO'}}),
node('04_aq','ADMIT','%aq','ADMISSION',['%g0'],{'admitted':True}),
node('05_pq','PORTAL_OPEN','%pq','PORTAL',['%g0','%aq'],{'sector':'QFT','corridor':'QFT-A'}),
node('06_tq','PORTAL_TRANSPORT','%gq','GEOMETRIC',['%pq','%g0'],{'destination':'QFT-B'}),
node('07_cq','PORTAL_CLOSE','%cq','RECEIPT',['%pq','%gq']),
node('08_bridge','BRIDGE_SECTOR','%b','BRIDGE',['%gq'],{'from':'QFT','to':'GR','preserve':['identity','chirality_ancestry','provenance']}),
node('09_ag','ADMIT','%ag','ADMISSION',['%gq'],{'admitted':True,'bridge':'%b'}),
node('10_pg','PORTAL_OPEN','%pg','PORTAL',['%gq','%ag'],{'sector':'GR','corridor':'GR-B'}),
node('11_tg','PORTAL_TRANSPORT','%gg','GEOMETRIC',['%pg','%gq'],{'destination':'GR-C'}),
node('12_cg','PORTAL_CLOSE','%cg','RECEIPT',['%pg','%gg']),
node('13_m5','BRANE_LIFT','%m5','M5',['%gg'],{'P':'mixed-sector-ledger'}),
node('14_receipt','EMIT_RECEIPT','%receipt','RECEIPT'),
], 'edges':[{'from':'08_bridge','to':'09_ag','kind':'effect_order'},{'from':'12_cg','to':'14_receipt','kind':'effect_order'}], 'exports':['%gg','%b','%cg','%m5','%receipt']}

quantum={
'ir':'GIR','version':'0.1.0','name':'quantum_effect_program','nodes':[
node('01_mount','FABRIC_MOUNT','%fabric','FABRIC',attrs={'uri':'fabric://chirality/reference-v1'}),
node('02_alloc','FABRIC_ALLOC','%region','REGION',['%fabric'],{'cells':2048}),
node('03_g0','GEO_INSTANTIATE','%g0','GEOMETRIC',['%fabric','%region'],{'mmo':{'handle':'@hydrogen_reference','class':'MMO'}}),
node('04_q0','Q_PREPARE','%q0','QSTATE',['%g0'],{'basis':['0','1']}),
node('05_q1','Q_SUPERPOSE','%q1','QSTATE',['%q0'],{'amplitudes':['1/sqrt(2)','1/sqrt(2)']}),
node('06_q2','Q_CHANNEL','%q2','QSTATE',['%q1'],{'channel':'IDENTITY','preserve_coherence':True}),
node('07_measure','Q_MEASURE','%qr','QRESULT',['%q2'],{'outcome':0,'reference_seed':'GENESIS-SECTION08'}),
node('08_seal','PROVENANCE_SEAL','%seal','RECEIPT',['%qr'],{'effect':'measurement'}),
node('09_receipt','EMIT_RECEIPT','%receipt','RECEIPT'),
], 'edges':[{'from':'08_seal','to':'09_receipt','kind':'effect_order'}], 'exports':['%qr','%seal','%receipt']}

for name,obj in [('FIRST_PORTAL',first_portal),('RAINBOW_ROAD',rainbow),('MIXED_SECTOR',mixed),('QUANTUM_EFFECT',quantum)]:
    j(f'18_EXAMPLES/{name}.gir.json',obj)

w('18_EXAMPLES/README.md', r'''
# Reference GIR programs

- `FIRST_PORTAL.gir.json` — the Bootstrap 0 milestone: one MMO, relationship, admission, transform, Portal transport, closure, BRANE lift, provenance receipt.
- `RAINBOW_ROAD.gir.json` — two independently closed GR Portal legs composed into one Road.
- `MIXED_SECTOR.gir.json` — explicit QFT Portal, QFT->GR bridge witness, then GR Portal.
- `QUANTUM_EFFECT.gir.json` — QFT quantum state prepare -> superpose -> channel -> measure with linear consumption.
''')

# Tests
w('17_TESTS/test_section08.py', r'''
import json, sys, unittest, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'13_REFERENCE_IMPLEMENTATION'))
from genesis_vm import *
from genesis_vm.errors import GIRCompileError, VerifyError, BytecodeError, RuntimeFault
from genesis_vm.model import Program, Instruction, Opcode, TypeTag

class Section08Tests(unittest.TestCase):
    def load(self,name): return json.loads((ROOT/'18_EXAMPLES'/name).read_text())
    def compile(self,name): return compile_gir(self.load(name))
    def test_01_schedule_independent_of_json_order(self):
        g=self.load('FIRST_PORTAL.gir.json'); p1=compile_gir(g)
        g['nodes']=list(reversed(g['nodes'])); p2=compile_gir(g)
        self.assertEqual(encode(p1),encode(p2))
    def test_02_cycle_rejected(self):
        g={'ir':'GIR','version':'0.1','name':'cycle','nodes':[{'id':'a','op':'NOP'},{'id':'b','op':'NOP'}],'edges':[{'from':'a','to':'b','kind':'dependency'},{'from':'b','to':'a','kind':'dependency'}]}
        with self.assertRaises(GIRCompileError): compile_gir(g)
    def test_03_unknown_value_rejected(self):
        g={'ir':'GIR','version':'0.1','name':'bad','nodes':[{'id':'a','op':'HASH','out':'%h','type':'HASH','args':['%x']}]}
        with self.assertRaises(GIRCompileError): compile_gir(g)
    def test_04_first_portal_verifies(self): self.assertTrue(verify(self.compile('FIRST_PORTAL.gir.json'))['ok'])
    def test_05_rainbow_verifies(self): self.assertTrue(verify(self.compile('RAINBOW_ROAD.gir.json'))['ok'])
    def test_06_mixed_verifies(self): self.assertTrue(verify(self.compile('MIXED_SECTOR.gir.json'))['ok'])
    def test_07_quantum_verifies(self): self.assertTrue(verify(self.compile('QUANTUM_EFFECT.gir.json'))['ok'])
    def test_08_bytecode_roundtrip_first(self):
        p=self.compile('FIRST_PORTAL.gir.json'); q=decode(encode(p)); self.assertEqual(encode(p),encode(q))
    def test_09_bytecode_roundtrip_quantum(self):
        p=self.compile('QUANTUM_EFFECT.gir.json'); q=decode(encode(p)); self.assertEqual(encode(p),encode(q))
    def test_10_corrupt_bytecode_rejected(self):
        b=bytearray(encode(self.compile('FIRST_PORTAL.gir.json'))); b[-1]^=1
        with self.assertRaises(BytecodeError): decode(bytes(b))
    def test_11_first_portal_runs(self):
        r=VM().run(self.compile('FIRST_PORTAL.gir.json')); self.assertTrue(r.halted); self.assertEqual(len(r.exports),4)
    def test_12_rainbow_runs(self): self.assertTrue(VM().run(self.compile('RAINBOW_ROAD.gir.json')).halted)
    def test_13_mixed_runs(self): self.assertTrue(VM().run(self.compile('MIXED_SECTOR.gir.json')).halted)
    def test_14_quantum_runs(self): self.assertTrue(VM().run(self.compile('QUANTUM_EFFECT.gir.json')).halted)
    def test_15_execution_deterministic(self):
        p=self.compile('FIRST_PORTAL.gir.json'); a=VM().run(p); b=VM().run(p)
        self.assertEqual(a.receipt['content_hash'],b.receipt['content_hash'])
    def test_16_first_portal_export_geometric(self):
        p=self.compile('FIRST_PORTAL.gir.json'); r=VM().run(p); g=r.exports[p.exports[0]].value; self.assertEqual(g['kind'],'GEOMETRIC')
    def test_17_first_portal_receipt_closed(self):
        p=self.compile('FIRST_PORTAL.gir.json'); r=VM().run(p); rec=r.exports[p.exports[1]].value; self.assertEqual(rec['payload']['op'],'PORTAL_CLOSE')
    def test_18_brane_lift_m5(self):
        p=self.compile('FIRST_PORTAL.gir.json'); r=VM().run(p); m5=r.exports[p.exports[2]].value; self.assertEqual(m5['kind'],'M5')
    def test_19_quantum_measure_result_classical(self):
        p=self.compile('QUANTUM_EFFECT.gir.json'); r=VM().run(p); qr=r.exports[p.exports[0]].value; self.assertTrue(qr['payload']['classical'])
    def test_20_quantum_linear_reuse_rejected_static(self):
        g=self.load('QUANTUM_EFFECT.gir.json')
        # add a second consumer of already-consumed q0
        g['nodes'].append({'id':'10_bad','op':'Q_MEASURE','out':'%bad','type':'QRESULT','args':['%q0'],'attrs':{'outcome':1}})
        p=compile_gir(g)
        with self.assertRaises(VerifyError): verify(p)
    def test_21_qstate_generic_move_runtime_forbidden(self):
        p=Program('qmove',instructions=[Instruction(Opcode.CONST,0,(),{'value':{'kind':'QSTATE'}},'a',TypeTag.QSTATE),Instruction(Opcode.MOVE,1,(0,),{},'b',TypeTag.QSTATE)],exports=[])
        # verifier does not claim CONST is a valid quantum allocator; runtime still blocks generic MOVE.
        verify(p)
        with self.assertRaises(RuntimeFault): VM().run(p)
    def test_22_use_before_define(self):
        p=Program('bad',instructions=[Instruction(Opcode.HASH,1,(0,),{},'x',TypeTag.HASH)])
        with self.assertRaises(VerifyError): verify(p)
    def test_23_register_redefinition(self):
        p=Program('bad',instructions=[Instruction(Opcode.CONST,0,(),{'value':1},'a',TypeTag.INT),Instruction(Opcode.CONST,0,(),{'value':2},'b',TypeTag.INT)])
        with self.assertRaises(VerifyError): verify(p)
    def test_24_invalid_jump(self):
        p=Program('bad',instructions=[Instruction(Opcode.JUMP,None,(),{'target':9},'a',TypeTag.VOID)])
        with self.assertRaises(VerifyError): verify(p)
    def test_25_unclosed_portal_static(self):
        # minimal typed constants to reach PORTAL_OPEN
        p=Program('bad',instructions=[
            Instruction(Opcode.CONST,0,(),{'value':{}},'g',TypeTag.GEOMETRIC),
            Instruction(Opcode.CONST,1,(),{'value':{}},'a',TypeTag.ADMISSION),
            Instruction(Opcode.PORTAL_OPEN,2,(0,1),{'sector':'GR'},'p',TypeTag.PORTAL)],exports=[])
        with self.assertRaises(VerifyError): verify(p)
    def test_26_overlay_does_not_change_base_resource(self):
        b=ReferenceBackend(); f=b.mount_fabric('fabric://x'); before=f['content_hash']; b.write_overlay(f,'A',{'v':1}); self.assertEqual(before,f['content_hash'])
    def test_27_bridge_requires_change(self):
        b=ReferenceBackend(); f=b.mount_fabric('x'); reg=b.alloc(f,1); g=b.instantiate(f,reg,{'h':'m'})
        from genesis_vm.errors import SectorError
        with self.assertRaises(SectorError): b.bridge(g,'QFT','QFT',{})
    def test_28_portal_transport_requires_open(self):
        b=ReferenceBackend(); f=b.mount_fabric('x'); reg=b.alloc(f,1); g=b.instantiate(f,reg,{'h':'m'}); a=b.admit(g,{}); p=b.portal_open(g,a,'GR',{}); d=b.portal_transport(p,g,{}); b.portal_close(p,d)
        from genesis_vm.errors import ClosureError
        with self.assertRaises(ClosureError): b.portal_transport(p,g,{})
    def test_29_bytecode_magic(self): self.assertEqual(encode(self.compile('FIRST_PORTAL.gir.json'))[:4],b'GVM1')
    def test_30_disasm_contains_portal(self): self.assertIn('PORTAL_OPEN',disassemble(self.compile('FIRST_PORTAL.gir.json')))
    def test_31_all_outputs_unique(self):
        p=self.compile('RAINBOW_ROAD.gir.json'); outs=[i.out for i in p.instructions if i.out is not None]; self.assertEqual(len(outs),len(set(outs)))
    def test_32_gir_hash_present(self): self.assertEqual(len(self.compile('FIRST_PORTAL.gir.json').metadata['gir_hash']),64)
    def test_33_backend_abi_present(self): self.assertEqual(self.compile('FIRST_PORTAL.gir.json').metadata['required_backend_abi'],'0.1')
    def test_34_portal_receipt_in_ledger(self):
        vm=VM(); vm.run(self.compile('FIRST_PORTAL.gir.json')); self.assertTrue(any(r['payload'].get('op')=='PORTAL_CLOSE' for r in vm.backend.ledger))
    def test_35_road_receipt_in_ledger(self):
        vm=VM(); vm.run(self.compile('RAINBOW_ROAD.gir.json')); self.assertTrue(any(r['payload'].get('op')=='ROAD_CLOSE' for r in vm.backend.ledger))
    def test_36_mixed_has_bridge_resource(self):
        p=self.compile('MIXED_SECTOR.gir.json'); r=VM().run(p); b=r.exports[p.exports[1]].value; self.assertEqual(b['kind'],'BRIDGE')
    def test_37_measure_consumes_state_runtime(self):
        b=ReferenceBackend(); f=b.mount_fabric('x'); reg=b.alloc(f,1); g=b.instantiate(f,reg,{'h':'m'}); q=b.q_prepare(g,{}); b.q_measure(q,{'outcome':0}); self.assertEqual(q['typestate'],'MEASURED')
    def test_38_q_successor_moves_source(self):
        b=ReferenceBackend(); f=b.mount_fabric('x'); reg=b.alloc(f,1); g=b.instantiate(f,reg,{'h':'m'}); q=b.q_prepare(g,{}); q2=b.q_successor('SUPERPOSE',[q],{}); self.assertEqual(q['typestate'],'MOVED'); self.assertEqual(q2['typestate'],'OWNED')
    def test_39_execution_receipt_kind(self): self.assertEqual(VM().run(self.compile('FIRST_PORTAL.gir.json')).receipt['kind'],'RECEIPT')
    def test_40_reference_program_count(self): self.assertEqual(len(list((ROOT/'18_EXAMPLES').glob('*.gir.json'))),4)

if __name__=='__main__': unittest.main()
''')

w('17_TESTS/TEST_MATRIX.md', r'''
# Section 08 test matrix

The executable suite covers:

- deterministic GIR scheduling independent of input JSON order;
- dependency-cycle and unknown-value rejection;
- all four reference GIR programs;
- bytecode encode/decode integrity and corruption detection;
- deterministic execution receipts;
- Geometric, Portal closure, Rainbow Road, Bridge, BRANE M5, and quantum measurement outputs;
- QSTATE linear use-after-consumption rejection;
- generic QSTATE move prohibition;
- register use-before-define and redefinition rejection;
- invalid control target rejection;
- unclosed Portal rejection;
- immutable fabric-resource identity across overlay writes;
- sector bridge sanity;
- closed Portal transport rejection;
- provenance ledger emission.
''')

# Source crosswalk/recovery
j('20_SOURCE_CROSSWALK/SOURCE_REGISTRY.json', {
'section':'08','status':'software bootstrap execution model','dependencies':[
{'section':'01','role':'fabric hardware ABI / immutable base + overlay contract'},
{'section':'02','role':'Geometric/MMO instantiation'},
{'section':'03','role':'transformation and immutable forking'},
{'section':'04','role':'Portal/Corridor transaction semantics'},
{'section':'05','role':'Rainbow Road composition'},
{'section':'06','role':'QFT/GR typed bridge'},
{'section':'07','role':'quantum information effects and linear ownership'},
{'source':'Computational Genesis handoff','role':'frontend/compiler precursor; noncanonical where superseded'},
{'source':'Layer Zero','role':'semantic constitution and initial IR/Portal contracts'},
{'source':'Astraeus mathematics','role':'dependency/admissibility/bandwidth/resolution/identity/history/holonomy'},
]})
w('20_SOURCE_CROSSWALK/SOURCE_CROSSWALK.md', r'''
# Source crosswalk

Section 08 is an implementation synthesis, not a claim that earlier scientific source documents literally specified a VM ISA.

- Section 01 constrains fabric-facing opcodes and forbids generic base-fabric mutation.
- Sections 02–03 motivate immutable/versioned Geometric resource semantics.
- Sections 04–05 constrain Portal/Road typestate and closure.
- Section 06 requires explicit sector transduction.
- Section 07 constrains QSTATE linear ownership and measurement effects.
- Layer Zero and the prior Computational Genesis handoff supply compiler/IR hypotheses that Section 08 now makes executable.
- Astraeus mathematics supplies conceptual constraints for admissibility, transport, identity through history, resolution, bandwidth, and holonomy.

Status discipline: GIR/GVM are **new computational architecture derived from those constraints**, not recovered historical mathematics.
''')
w('21_RECOVERY/SECTION_08_STATE.md', r'''
# Section 08 recovery state

**Canonical folder:** `GENESIS_CHIRALITY_MACHINE_SECTION_08_VM_IR_v0.1.0_20260821`

## Established in this section

- GIR 0.1 typed graph IR is the canonical source-neutral compiler target.
- GVM 0.1 is the deterministic executable lowering target.
- Future Genesis text compiles to GIR; GIR lowers to GVM; GVM dispatches through backend ABI to Sections 01–07.
- Python is bootstrap/reference implementation only.
- VM storage is split into registers, resource table, fabric address space, overlay state, ledger, and frames.
- Base chirality fabric is not a generic mutable heap.
- Identity-bearing resources and closure receipts are machine-visible.
- QSTATE remains linear and measurement is explicit.
- QFT/GR sector transition requires an explicit bridge witness.
- `.gvm` deterministic bytecode format v0.1 established.
- First Portal, two-leg Rainbow Road, mixed-sector, and quantum-effect GIR fixtures compile and run through the reference VM.

## Next engineering layer

Section 09 should define the **Genesis static type/effect checker + semantic linker** at the language/compiler boundary: parametric typestates, object/API symbol resolution, module imports, capability checking, proof-obligation generation, and linking GIR graphs into executable programs.
''')

# Save build script itself (this script will copy after generated by caller)

# Run tests
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'13_REFERENCE_IMPLEMENTATION')
cp=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'17_TESTS'),'-p','test_*.py','-v'],capture_output=True,text=True,env=ENV)
(ROOT/'99_RELEASE/TEST_RESULTS.txt').write_text(cp.stdout+cp.stderr,encoding='utf-8')
if cp.returncode!=0:
    print(cp.stdout); print(cp.stderr,file=sys.stderr); raise SystemExit(cp.returncode)

# Compile reference programs, emit gvm/disasm/receipts
sys.path.insert(0,str(ROOT/'13_REFERENCE_IMPLEMENTATION'))
from genesis_vm import compile_gir, verify, encode, decode, VM, disassemble
results={}
for src in sorted((ROOT/'18_EXAMPLES').glob('*.gir.json')):
    gir=json.loads(src.read_text())
    p=compile_gir(gir); ver=verify(p); blob=encode(p); q=decode(blob)
    outbase=ROOT/'19_REFERENCE_PROGRAMS'/src.name.replace('.gir.json','')
    (outbase.with_suffix('.gvm')).write_bytes(blob)
    (outbase.with_suffix('.disasm.txt')).write_text(disassemble(q),encoding='utf-8')
    vm=VM(); res=vm.run(q)
    receipt={
      'program':p.name,'gir_sha256':hashlib.sha256(canon(gir)).hexdigest(),
      'gvm_sha256':hashlib.sha256(blob).hexdigest(),'verify':ver,
      'execution_receipt':res.receipt,
      'exports':{str(k):{'type':v.type.value,'value':v.value} for k,v in res.exports.items()},
      'backend_ledger':[x for x in vm.backend.ledger],
    }
    outbase.with_suffix('.run.json').write_text(json.dumps(receipt,indent=2,sort_keys=True),encoding='utf-8')
    results[p.name]={'gvm_sha256':receipt['gvm_sha256'],'execution_receipt':res.receipt['content_hash'],'instructions':len(p.instructions),'exports':len(p.exports),'status':'PASS'}
j('99_RELEASE/REFERENCE_PROGRAM_RESULTS.json',results)

# Core checksums manifest
core_files=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and '98_BUILD' not in p.parts and '99_RELEASE/CORE_CHECKSUMS.sha256' not in str(p) and '99_RELEASE/CORE_MANIFEST.json' not in str(p):
        rel=p.relative_to(ROOT).as_posix(); h=hashlib.sha256(p.read_bytes()).hexdigest(); core_files.append((rel,h,p.stat().st_size))
(ROOT/'99_RELEASE/CORE_CHECKSUMS.sha256').write_text(''.join(f'{h}  {rel}\n' for rel,h,s in core_files),encoding='utf-8')
j('99_RELEASE/CORE_MANIFEST.json',{'section':'08','version':'0.1.0','date':'2026-08-21','files':[{'path':r,'sha256':h,'bytes':s} for r,h,s in core_files],'tests':'40/40 PASS','reference_programs':'4/4 PASS'})

# Copy build script into tree if available
src_script=Path('/mnt/data/_build_section08.py')
if src_script.exists(): shutil.copy2(src_script,ROOT/'98_BUILD/_build_section08.py')

print('BUILT',ROOT)
print(cp.stdout.splitlines()[-1] if cp.stdout.splitlines() else 'tests complete')
print(json.dumps(results,indent=2))
