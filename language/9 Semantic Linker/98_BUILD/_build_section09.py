from pathlib import Path
import shutil, json, textwrap, hashlib, os, zipfile, subprocess, sys, importlib.util, copy

ROOT = Path('/mnt/data/GENESIS_CHIRALITY_MACHINE_SECTION_09_STATIC_SEMANTICS_LINKER_v0.1.0_20260821')
S08 = Path('/mnt/data/GENESIS_CHIRALITY_MACHINE_SECTION_08_VM_IR_v0.1.0_20260821')
if ROOT.exists(): shutil.rmtree(ROOT)
DIRS = [
'00_START_HERE','01_ARCHITECTURE','02_TYPE_SYSTEM','03_TYPESTATES','04_EFFECT_SYSTEM','05_MODULE_SYSTEM','06_SYMBOL_RESOLUTION','07_SEMANTIC_LINKER','08_BACKEND_CAPABILITIES','09_PROOF_OBLIGATIONS','10_STATIC_CHECKER','11_VM_INTEGRATION','12_REFERENCE_IMPLEMENTATION/genesis_semantics/vendor','13_SCHEMAS','14_PSEUDOCODE','15_FAILURES','16_TESTS','17_EXAMPLES/modules','17_EXAMPLES/bundles','18_REFERENCE_LINKED_PROGRAMS','19_SOURCE_CROSSWALK','20_RECOVERY','98_BUILD','99_RELEASE'
]
for d in DIRS: (ROOT/d).mkdir(parents=True, exist_ok=True)

def w(rel, txt):
    p=ROOT/rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(textwrap.dedent(txt).lstrip(), encoding='utf-8')
def j(rel,obj):
    p=ROOT/rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(obj,indent=2,sort_keys=True),encoding='utf-8')
def canon(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(o): return hashlib.sha256(canon(o)).hexdigest()

# ---------------- docs ----------------
w('00_START_HERE/FOLDER_NAME.txt', ROOT.name+'\n')
w('00_START_HERE/README.md', r'''
# Genesis Chirality Machine — Section 09
## Static Type/Effect Checker + Semantic Linker

**Version:** 0.1.0 — bootstrap static semantics and link layer  
**Date:** 2026-08-21

Section 09 sits immediately above the Section 08 GIR/GVM execution model. It answers a different question from the VM:

> **Before a Genesis relationship graph is allowed to execute, is it semantically well-formed, capability-compatible, ownership-safe, sector-correct, and closed?**

The section adds five machine-facing facilities:

1. a refined **parametric type system** for identity-bearing runtime resources;
2. **typestate and linear-resource checking** for Portals, Roads, and QSTATEs;
3. an explicit **effect budget** for fabric access, transformation, transport, closure, transduction, measurement, provenance, and control;
4. a **semantic module/linker format** that resolves typed imports/exports and alpha-renames graphs without flattening provenance;
5. a **backend capability contract** that rejects linked programs a target cannot realize.

```text
future Genesis source modules
          |
          v
typed GIR modules
          |
          +--> symbol resolution
          +--> static type / typestate checker
          +--> effect budget checker
          +--> proof-obligation ledger
          +--> backend capability check
          |
          v
semantic linker
          |
          v
one verified GIR graph
          |
          v
Section 08 compiler -> GVM -> backend ABI -> Sections 01..07
```

### Important boundary

Section 09 is still **below human-facing Genesis syntax**. It does not freeze keywords or grammar. Its interfaces are graph/module semantics that a future parser, graph editor, generated program, or other frontend can target.

### Status discipline

The static semantics and linker are a new computational synthesis constrained by Sections 01–08 and the project mathematics. They are not represented as recovered historical mathematics.
''')
w('00_START_HERE/RECOVERY_ORDER.md', r'''
# Recovery order

1. **Part A** — complete Section 09 implementation, specifications, schemas, examples, tests, linked bytecode, and recovery state.
2. **Part B** — linked reference execution corpus plus the large Section 08 execution corpus used as the oracle/integration layer.
3. **Part C** — Sections 01–08 core implementation lineage plus Layer Zero / prior Computational Genesis / CFP / Corridor / Rainbow Road references.
4. **Part D** — Astraeus mathematics + API 4.3 + QFT/GR bridge.
5. **Part E** — MK Ultra information/QFT-GR/Helicon source lineage.

Mount Part A first. Parts B–E are provenance, integration fixtures, and scientific/mathematical reference layers; they do not redefine the Section 09 semantic contract.
''')

w('01_ARCHITECTURE/ARCHITECTURE.md', r'''
# Architecture

Section 08 made the execution language real. Section 09 makes it **linkable and statically governable**.

```text
GIR Module A       GIR Module B       GIR Module C
    |                  |                  |
    +---- typed imports / exports --------+
                       |
                 Symbol Resolver
                       |
              Module Dependency DAG
                       |
        +--------------+---------------+
        |              |               |
   Type checker    Effect checker   Capability checker
        |              |               |
        +---------- Proof ledger -------+
                       |
                Semantic Linker
                       |
          alpha-renamed unified GIR
                       |
               Section 08 compiler
                       |
                     GVM
```

## Core law

**Linkage may combine graphs; it may not erase the boundaries that establish identity, provenance, ownership, sector transition, or closure obligations.**

Every linked output carries a module map and content-addressed link receipt so the flattened executable graph can be traced back to each contributing module and symbol.
''')
w('01_ARCHITECTURE/DESIGN_INVARIANTS.md', r'''
# Design invariants

1. GIR remains the semantic execution graph; Section 09 does not replace it with source-language syntax.
2. A module import must resolve to exactly one declared export.
3. Import/export type compatibility is checked before graph merge.
4. Node IDs and SSA values are alpha-renamed by module, preventing accidental capture.
5. Link order is determined from the module dependency DAG, not input-file order.
6. Module dependency cycles are rejected in v0.1 rather than silently introducing initialization semantics.
7. Refined types may add sector/typestate information without changing the Section 08 coarse VM type tag.
8. A QSTATE is linear: a consuming quantum effect moves/consumes the previous state handle.
9. Portals and Roads cannot escape the linked program in OPEN typestate.
10. Cross-sector use requires an explicit Bridge authorization; QFT and GR are not aliases.
11. Effect budgets are allow-lists. A module cannot acquire undeclared authority by linking against another module.
12. A target backend must advertise every required opcode/effect/sector feature.
13. Proof obligations are auditable static witnesses, not claims of mathematical theorem proving beyond the encoded checks.
14. Link receipts and output GIR are content-addressed and deterministic for identical normalized inputs.
15. Python is the bootstrap implementation, not the semantic authority.
''')

w('02_TYPE_SYSTEM/TYPE_MODEL.md', r'''
# Refined type model

Section 08 exposes coarse VM tags such as `GEOMETRIC`, `PORTAL`, `QSTATE`, and `RECEIPT`. Section 09 overlays static refinements that are erased to those coarse tags when lowering to GVM.

Examples:

```text
GEOMETRIC<CLOSED,UNBOUND>
GEOMETRIC<CLOSED,QFT>
GEOMETRIC<CLOSED,GR>
PORTAL<QFT,OPEN>
PORTAL<GR,CLOSED>
ROAD<OPEN>
QSTATE<OWNED>
QSTATE<MOVED>
QRESULT<CLASSICAL>
BRIDGE<QFT,GR>
RECEIPT<PORTAL_CLOSE>
M5
```

A declaration may intentionally be coarse:

```text
GEOMETRIC
PORTAL
RECEIPT
```

A coarse declaration accepts a compatible refined instance. Thus `GEOMETRIC` can describe `GEOMETRIC<CLOSED,QFT>`, while `GEOMETRIC<CLOSED,GR>` does not accept a QFT Geometric.

These refinements are static semantics. The GVM still uses the stable Section 08 type tags.
''')
w('02_TYPE_SYSTEM/OP_SIGNATURES.md', r'''
# Selected static signatures

```text
FABRIC_MOUNT()                                -> FABRIC
FABRIC_ALLOC(FABRIC)                          -> REGION
GEO_INSTANTIATE(FABRIC, REGION)               -> GEOMETRIC<CLOSED,UNBOUND>
GEO_FORK(GEOMETRIC<CLOSED,S>)                 -> GEOMETRIC<CLOSED,S>
RELATE(GEOMETRIC, X)                          -> RELATION
ADMIT(GEOMETRIC)                              -> ADMISSION
TRANSFORM(GEOMETRIC<CLOSED,S>, ADMISSION)     -> GEOMETRIC<CLOSED,S>
PORTAL_OPEN(GEOMETRIC<CLOSED,S>, ADMISSION)   -> PORTAL<T,OPEN>
PORTAL_TRANSPORT(PORTAL<T,OPEN>, GEOMETRIC)   -> GEOMETRIC<CLOSED,T>
PORTAL_CLOSE(PORTAL<T,OPEN>, GEOMETRIC<...,T>) -> RECEIPT<PORTAL_CLOSE>
ROAD_BEGIN(GEOMETRIC)                         -> ROAD<OPEN>
ROAD_APPEND(ROAD<OPEN>, RECEIPT)              -> ROAD<OPEN>
ROAD_CLOSE(ROAD<OPEN>, GEOMETRIC)             -> RECEIPT<ROAD_CLOSE>
BRIDGE_SECTOR(GEOMETRIC<CLOSED,S>, S, T)      -> BRIDGE<S,T>
Q_PREPARE(GEOMETRIC)                          -> QSTATE<OWNED>
Q_SUPERPOSE(QSTATE<OWNED>)                    -> QSTATE<OWNED> [moves input]
Q_ENTANGLE(QSTATE<OWNED>, QSTATE<OWNED>)      -> QSTATE<OWNED> [moves both]
Q_CHANNEL(QSTATE<OWNED>)                      -> QSTATE<OWNED> [moves input]
Q_MEASURE(QSTATE<OWNED>)                      -> QRESULT<CLASSICAL> [consumes input]
BRANE_LIFT(GEOMETRIC)                         -> M5
PROVENANCE_SEAL(X)                            -> RECEIPT<PROVENANCE>
```

`S` and `T` are sector refinements. An `UNBOUND` Geometric may acquire a sector on first admitted sector-specific transport. Once sector-bound, a different sector requires an explicit Bridge witness.
''')

w('03_TYPESTATES/TYPESTATE_RULES.md', r'''
# Typestate rules

## Portal

```text
PORTAL<T,OPEN>
   | transport may occur
   v
PORTAL<T,OPEN>
   | close exactly once
   v
PORTAL<T,CLOSED>
```

The v0.1 GIR representation uses the same SSA Portal value for transport and close, so Section 09 tracks typestate in the verifier state rather than requiring a new SSA value for closure.

## Road

`ROAD_APPEND` moves the input Road version and returns a successor `ROAD<OPEN>`. This mirrors the persistent/versioned Road implementation in Section 05/08.

## QSTATE

```text
QSTATE<OWNED> --SUPERPOSE/CHANNEL--> moved + successor OWNED
QSTATE<OWNED> --ENTANGLE with OWNED--> both moved + successor OWNED
QSTATE<OWNED> --MEASURE--> consumed + QRESULT<CLASSICAL>
```

Generic `MOVE` cannot clone a QSTATE.
''')
w('03_TYPESTATES/SECTOR_BINDING.md', r'''
# Sector binding and Bridge authority

Sector is a representation/transport refinement, not identity equivalence.

- `UNBOUND` may bind on first sector-specific Portal transport.
- `QFT -> QFT` and `GR -> GR` transport require no sector bridge.
- `QFT -> GR` or `GR -> QFT` requires a preceding explicit `BRIDGE_SECTOR` witness for the same Geometric lineage/value and target sector.
- A Bridge is authorization/evidence for transduction; it is not treated as a third Portal sector.

The checker records Bridge witnesses as `(geometric-value, from-sector, to-sector)`. A later sector-changing Portal must match one.
''')

w('04_EFFECT_SYSTEM/EFFECTS.md', r'''
# Static effect system

Effects inherited from the Section 08 machine contract:

`READ_FABRIC`, `WRITE_OVERLAY`, `ALLOCATE`, `RELATE`, `ADMIT`, `TRANSFORM`, `TRANSPORT`, `CLOSE`, `INHERIT`, `PROJECT`, `TRANSDUCE`, `MEASURE`, `QUANTUM_LINEAR`, `PROVENANCE`, `CONTROL`.

A semantic module may declare:

```json
"effects": ["ALLOCATE", "INHERIT", "READ_FABRIC"]
```

The checker computes actual effects from contained operations and requires:

```text
actual_effects(module) subset_of declared_effect_budget(module)
```

Omitting `effects` means the module is unconstrained by a local budget during bootstrap; linked production bundles should declare budgets.

Effects are authority boundaries. Linking does not cause Module A to inherit Module B's permissions.
''')
w('04_EFFECT_SYSTEM/EFFECT_TABLE.md', r'''
# Effect table summary

- fabric mount/read -> `READ_FABRIC`
- overlay write -> `WRITE_OVERLAY`
- allocation/instantiation -> `ALLOCATE`
- relation -> `RELATE`
- admission -> `ADMIT`
- transform/fork -> `TRANSFORM`, often `INHERIT`
- Portal/Road -> `TRANSPORT`, closure adds `CLOSE` + `PROVENANCE`
- QFT/GR Bridge -> `TRANSDUCE` + `PROVENANCE`
- quantum state evolution -> `QUANTUM_LINEAR`; channels also `TRANSFORM`
- measurement -> `MEASURE` + `QUANTUM_LINEAR`
- BRANE lift -> `PROJECT`
- provenance seal / execution receipt -> `PROVENANCE`
- branches/calls/returns -> `CONTROL`
''')

w('05_MODULE_SYSTEM/MODULE_FORMAT.md', r'''
# GIR semantic module format

```json
{
  "ir": "GIR-MODULE",
  "module": "transport",
  "version": "0.1.0",
  "effects": ["ADMIT", "TRANSPORT", "CLOSE", "PROVENANCE"],
  "imports": [
    {"local": "%source", "from": "fixture", "symbol": "geo", "type": "GEOMETRIC"}
  ],
  "exports": [
    {"symbol": "destination", "value": "%g1", "type": "GEOMETRIC<CLOSED,QFT>"}
  ],
  "gir": {
    "nodes": [],
    "edges": []
  }
}
```

Imports are **typed symbolic edges**, not textual inclusion. Exports name values that remain traceable to their module-local producer.
''')
w('05_MODULE_SYSTEM/MODULE_DEPENDENCIES.md', r'''
# Module dependency graph

Each `imports[].from` creates a module dependency. The semantic linker:

1. validates module names;
2. resolves import symbols;
3. rejects unresolved/ambiguous symbols;
4. rejects dependency cycles in v0.1;
5. derives deterministic module order lexically among otherwise independent modules.

A future version may introduce explicit recursive interfaces. v0.1 does not infer such semantics.
''')

w('06_SYMBOL_RESOLUTION/SYMBOL_RESOLUTION.md', r'''
# Symbol resolution

Symbol identity is `(module, exported-symbol)`.

The linker never resolves by bare value spelling across modules. `%g0` in two modules is unrelated until a typed import binds one module-local alias to another module's declared export.

During linking:

```text
module node id     01_mount    -> fixture::01_mount
module SSA value   %g0         -> %fixture::g0
import alias        %source     -> %fixture::g0
```

This alpha-renaming makes capture impossible without an explicit linker defect.
''')
w('06_SYMBOL_RESOLUTION/VERSION_POLICY.md', r'''
# Version policy v0.1

- Module schema version must be `0.1.0` in the reference implementation.
- Link bundle format is `0.1.0`.
- Required backend ABI is `0.1`.
- No semantic-version range solver is introduced yet.

The restriction is intentional: stable meaning matters more than flexible dependency resolution during bootstrap.
''')

w('07_SEMANTIC_LINKER/LINK_ALGORITHM.md', r'''
# Semantic link algorithm

```text
parse modules
  -> validate names and declared interfaces
  -> build export symbol table
  -> resolve + type-check imports
  -> topologically order module dependency DAG
  -> alpha-rename each node and local SSA value
  -> substitute imported aliases with resolved global values
  -> rewrite internal edges
  -> merge nodes/edges
  -> choose declared bundle exports
  -> run linked static checker
  -> check backend capabilities
  -> emit proof-obligation ledger
  -> attach module/source map metadata
  -> compile with Section 08 GIR -> GVM
  -> verify GVM
  -> encode deterministic bytecode
  -> emit content-addressed link receipt
```
''')
w('07_SEMANTIC_LINKER/DETERMINISM.md', r'''
# Deterministic linkage

Normalized content hashes cover:

- module interfaces and GIR content;
- link-bundle export selection;
- backend capability manifest;
- alpha-renaming map;
- unified GIR graph;
- compiled GVM bytes.

Input file order does not define link order. The dependency DAG plus lexical tie-breaking does.
''')

w('08_BACKEND_CAPABILITIES/CAPABILITY_CONTRACT.md', r'''
# Backend capability contract

A backend capability manifest advertises:

- ABI version;
- supported GIR/GVM operation names;
- supported effects;
- sectors (`GENERIC`, `QFT`, `GR`, etc.);
- feature flags such as `portal`, `rainbow_road`, `sector_bridge`, `quantum_linear`, and `provenance_receipts`.

A linked program is rejected before bytecode execution when required capabilities are absent. This prevents "compile succeeded, backend cannot possibly realize it" from becoming a runtime discovery mechanism.
''')

w('09_PROOF_OBLIGATIONS/OBLIGATIONS.md', r'''
# Static proof obligations

Section 09 emits auditable witnesses for checks it actually performs:

- `PO-SYMBOL-RESOLUTION` — all imports/exports resolved uniquely;
- `PO-TYPE-SAFETY` — operation arguments and result declarations are compatible;
- `PO-EFFECT-BOUNDS` — actual module effects are within declared budgets;
- `PO-LINEAR-OWNERSHIP` — quantum linear resources are not consumed twice or generically cloned;
- `PO-CLOSURE` — no Portal/Road remains OPEN at linked-program boundary;
- `PO-SECTOR-TRANSDUCTION` — sector change has a matching Bridge witness;
- `PO-CAPABILITY` — target advertises required ops/effects/sectors/features;
- `PO-PROVENANCE` — linked graph contains module/source map and link receipt.

These are **static machine proofs relative to the implemented rules**. They are not broad claims that arbitrary program correctness or physical behavior has been formally proved.
''')
w('09_PROOF_OBLIGATIONS/PROOF_LEDGER_FORMAT.md', r'''
# Proof ledger format

Each obligation records:

```json
{
  "id": "PO-TYPE-SAFETY",
  "status": "PASS",
  "witness": {"checked_nodes": 12, "refined_values": 11},
  "ruleset": "section09-v0.1.0"
}
```

Failed obligations carry diagnostics and prevent emission of a linked executable.
''')

w('10_STATIC_CHECKER/CHECKER_PIPELINE.md', r'''
# Static checker pipeline

For a module or linked GIR graph:

1. seed the type environment from typed imports;
2. schedule local nodes using data and effect-order dependencies;
3. validate opcode argument arity/kinds;
4. infer refined output type;
5. compare any declared coarse/refined type;
6. collect effects;
7. update Portal/Road/QSTATE typestate;
8. record Bridge witnesses and validate cross-sector Portal usage;
9. validate linear ownership;
10. reject leaked OPEN Portal/Road resources;
11. validate declared exports.

Diagnostics are deterministic and include a code, node/module context, and message.
''')
w('10_STATIC_CHECKER/ERASURE.md', r'''
# Refinement erasure into Section 08

Section 09 refinements do not require changing the stable Section 08 bytecode type-tag enum.

```text
PORTAL<QFT,OPEN>        -> PORTAL
GEOMETRIC<CLOSED,GR>    -> GEOMETRIC
QSTATE<OWNED>           -> QSTATE
RECEIPT<PORTAL_CLOSE>   -> RECEIPT
```

The unified GIR carries a `metadata.section09.refined_types` map. Section 08 compiles the coarse `type` fields and executes the already-checked graph.
''')

w('11_VM_INTEGRATION/PIPELINE.md', r'''
# Section 08 integration

The reference linker vendors the Section 08 Python VM package solely so Part A is executable in isolation.

```text
link_bundle()
  -> linked GIR
  -> Section 09 static PASS
  -> Section 08 compile_gir()
  -> Section 08 verify()
  -> Section 08 encode()
  -> .gvm
```

The vendored package is byte-for-byte copied from the current Section 08 core implementation in this build. Its presence does not create a second semantic authority; Section 08 remains the execution-model source layer.
''')

w('15_FAILURES/FAILURE_TAXONOMY.md', r'''
# Failure taxonomy

Static/link failures include:

- `MODULE_DUPLICATE`
- `MODULE_CYCLE`
- `IMPORT_UNRESOLVED`
- `EXPORT_UNRESOLVED`
- `SYMBOL_DUPLICATE`
- `IMPORT_TYPE_MISMATCH`
- `UNKNOWN_VALUE`
- `NODE_DUPLICATE`
- `TYPE_MISMATCH`
- `ARITY_MISMATCH`
- `EFFECT_BUDGET_EXCEEDED`
- `LINEAR_USE_AFTER_MOVE`
- `QSTATE_GENERIC_MOVE`
- `PORTAL_NOT_OPEN`
- `PORTAL_UNCLOSED`
- `ROAD_NOT_OPEN`
- `ROAD_UNCLOSED`
- `SECTOR_MISMATCH`
- `BRIDGE_REQUIRED`
- `BRIDGE_MISMATCH`
- `BACKEND_ABI_MISMATCH`
- `CAPABILITY_OP_MISSING`
- `CAPABILITY_EFFECT_MISSING`
- `CAPABILITY_SECTOR_MISSING`
- `CAPABILITY_FEATURE_MISSING`

These fail before Section 08 bytecode is accepted as a linked Section 09 executable.
''')

# ---------------- reference implementation ----------------
PKG=ROOT/'12_REFERENCE_IMPLEMENTATION/genesis_semantics'
(PKG/'vendor').mkdir(parents=True,exist_ok=True)
w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/__init__.py', '''
from .typesys import TypeExpr, parse_type, compatible
from .checker import check_gir, check_module
from .linker import link_bundle, LinkResult
from .capabilities import check_capabilities, reference_backend_capabilities
from .effects import OP_EFFECTS, effects_for_op
from .proofs import proof_ledger
''')
w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/errors.py', '''
class GenesisSemanticError(Exception): pass
class TypeCheckError(GenesisSemanticError): pass
class LinkError(GenesisSemanticError): pass
class CapabilityError(GenesisSemanticError): pass
''')
w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/model.py', '''
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class TypeExpr:
    kind: str
    params: tuple[str,...]=()
    def __str__(self):
        return self.kind if not self.params else f"{self.kind}<{','.join(self.params)}>"

@dataclass
class Diagnostic:
    code: str
    message: str
    node: str|None=None
    module: str|None=None
    severity: str='ERROR'
    def as_dict(self): return {'code':self.code,'message':self.message,'node':self.node,'module':self.module,'severity':self.severity}

@dataclass
class CheckResult:
    ok: bool
    diagnostics: list[Diagnostic]=field(default_factory=list)
    value_types: dict[str,TypeExpr]=field(default_factory=dict)
    effects: set[str]=field(default_factory=set)
    witnesses: dict[str,Any]=field(default_factory=dict)
    def as_dict(self):
        return {'ok':self.ok,'diagnostics':[d.as_dict() for d in self.diagnostics], 'value_types':{k:str(v) for k,v in sorted(self.value_types.items())}, 'effects':sorted(self.effects), 'witnesses':self.witnesses}

@dataclass
class LinkResult:
    gir: dict
    program: Any
    bytecode: bytes
    receipt: dict
    proofs: list[dict]
    check: CheckResult
''')
w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/util.py', '''
import json, hashlib

def canonical_bytes(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def sha256_obj(obj): return hashlib.sha256(canonical_bytes(obj)).hexdigest()
def sha256_bytes(data): return hashlib.sha256(data).hexdigest()
''')
w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/typesys.py', r'''
import re
from .model import TypeExpr

ALIASES={'GEO':'GEOMETRIC','QRESULT':'QRESULT','QSTATE':'QSTATE','ANY':'ANY'}

def parse_type(text):
    if isinstance(text,TypeExpr): return text
    if text is None: return TypeExpr('ANY')
    s=str(text).strip()
    m=re.fullmatch(r'([A-Za-z_][A-Za-z0-9_]*)(?:<([^<>]*)>)?',s)
    if not m: raise ValueError(f'invalid type expression {text!r}')
    kind=ALIASES.get(m.group(1).upper(),m.group(1).upper())
    params=tuple(x.strip().upper() for x in (m.group(2) or '').split(',') if x.strip())
    return TypeExpr(kind,params)

def compatible(required,actual):
    r=parse_type(required); a=parse_type(actual)
    if r.kind in ('ANY','RESOURCE'): return True
    if r.kind!=a.kind: return False
    if not r.params: return True
    if len(r.params)>len(a.params): return False
    for rp,ap in zip(r.params,a.params):
        if rp not in ('*','ANY') and rp!=ap: return False
    return True

def kind_is(t,kind): return parse_type(t).kind==kind.upper()
def sector_of(t):
    t=parse_type(t)
    if t.kind=='GEOMETRIC' and len(t.params)>=2: return t.params[1]
    if t.kind=='PORTAL' and t.params: return t.params[0]
    if t.kind=='BRIDGE' and len(t.params)>=2: return t.params[1]
    return None

def state_of(t):
    t=parse_type(t)
    if t.kind=='GEOMETRIC' and t.params: return t.params[0]
    if t.kind=='PORTAL' and len(t.params)>=2: return t.params[1]
    if t.kind in ('ROAD','QSTATE') and t.params: return t.params[0]
    return None

def erase_type(t): return parse_type(t).kind
''')
w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/effects.py', r'''
OP_EFFECTS={
'NOP':set(),'CONST':set(),'MOVE':set(),'HASH':set(),
'FABRIC_MOUNT':{'READ_FABRIC'},'FABRIC_ALLOC':{'ALLOCATE'},'FABRIC_READ':{'READ_FABRIC'},'FABRIC_WRITE_OVERLAY':{'WRITE_OVERLAY'},
'GEO_INSTANTIATE':{'ALLOCATE','INHERIT'},'GEO_FORK':{'TRANSFORM','INHERIT'},'RELATE':{'RELATE'},'ADMIT':{'ADMIT'},'TRANSFORM':{'TRANSFORM','INHERIT'},'INHERIT':{'INHERIT','PROVENANCE'},
'PORTAL_OPEN':{'TRANSPORT'},'PORTAL_TRANSPORT':{'TRANSPORT','INHERIT'},'PORTAL_CLOSE':{'CLOSE','PROVENANCE'},
'ROAD_BEGIN':{'TRANSPORT'},'ROAD_APPEND':{'TRANSPORT','INHERIT'},'ROAD_CLOSE':{'CLOSE','PROVENANCE'},
'BRIDGE_SECTOR':{'TRANSDUCE','PROVENANCE'},
'Q_PREPARE':{'QUANTUM_LINEAR'},'Q_SUPERPOSE':{'QUANTUM_LINEAR'},'Q_ENTANGLE':{'QUANTUM_LINEAR'},'Q_CHANNEL':{'QUANTUM_LINEAR','TRANSFORM'},'Q_MEASURE':{'MEASURE','QUANTUM_LINEAR'},
'BRANE_LIFT':{'PROJECT'},'PROVENANCE_SEAL':{'PROVENANCE'},'ASSERT_CLOSURE':{'CLOSE'},'EMIT_RECEIPT':{'PROVENANCE'},
'JUMP':{'CONTROL'},'BRANCH':{'CONTROL'},'CALL':{'CONTROL'},'RETURN':{'CONTROL'},'HALT':{'CONTROL'},
}
def effects_for_op(op): return set(OP_EFFECTS.get(op,set()))
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/checker.py', r'''
from collections import defaultdict
from .model import Diagnostic, CheckResult, TypeExpr
from .typesys import parse_type, compatible, sector_of
from .effects import effects_for_op, OP_EFFECTS

class State:
    def __init__(self,seed=None,module=None):
        self.types=dict(seed or {})
        self.module=module
        self.diags=[]; self.effects=set(); self.bridges=[]; self.portal={}; self.road={}; self.q_live={}
        self.producers={}
    def err(self,code,msg,node=None): self.diags.append(Diagnostic(code,msg,node,self.module))

def _schedule(gir,seed_values):
    nodes=gir.get('nodes',[]); by={}; prod={}; deps={}; rev=defaultdict(set)
    for n in nodes:
        nid=n.get('id')
        if not nid: raise ValueError('node missing id')
        if nid in by: raise ValueError(f'duplicate node {nid}')
        by[nid]=n; deps[nid]=set()
        out=n.get('out')
        if out:
            if out in prod: raise ValueError(f'duplicate output {out}')
            prod[out]=nid
    for n in nodes:
        nid=n['id']
        for a in n.get('args',[]):
            if isinstance(a,str) and a.startswith('%'):
                if a in prod:
                    p=prod[a]
                    if p!=nid: deps[nid].add(p); rev[p].add(nid)
                elif a not in seed_values:
                    raise KeyError(f'unknown value {a} in {nid}')
    for e in gir.get('edges',[]):
        if e.get('kind','dependency') in ('dependency','effect_order'):
            a=e.get('from'); b=e.get('to')
            if a not in by or b not in by: raise KeyError(f'unknown edge {a}->{b}')
            deps[b].add(a); rev[a].add(b)
    ready=sorted([x for x,d in deps.items() if not d]); out=[]; done=set()
    while ready:
        x=ready.pop(0); out.append(by[x]); done.add(x)
        for y in sorted(rev[x]):
            deps[y].discard(x)
            if not deps[y] and y not in done and y not in ready:
                ready.append(y); ready.sort()
    if len(out)!=len(nodes): raise ValueError('dependency cycle: '+','.join(sorted(set(by)-done)))
    return out

def _arg(st,n,i,required=None):
    args=n.get('args',[])
    if i>=len(args): st.err('ARITY_MISMATCH',f"{n['op']} missing argument {i}",n['id']); return TypeExpr('ANY'),None
    a=args[i]
    if not (isinstance(a,str) and a.startswith('%')): return TypeExpr('ANY'),a
    if a not in st.types: st.err('UNKNOWN_VALUE',f'unknown value {a}',n['id']); return TypeExpr('ANY'),a
    t=st.types[a]
    if required and not compatible(required,t): st.err('TYPE_MISMATCH',f'{n["op"]} arg {i} requires {required}, got {t}',n['id'])
    return t,a

def _portal_state(st,val,node):
    if val is None: return
    if st.portal.get(val)!='OPEN': st.err('PORTAL_NOT_OPEN',f'portal {val} is not OPEN',node)

def _road_state(st,val,node):
    if val is None:return
    if st.road.get(val)!='OPEN': st.err('ROAD_NOT_OPEN',f'road {val} is not OPEN',node)

def _consume_q(st,val,node):
    if val is None:return
    if not st.q_live.get(val,False): st.err('LINEAR_USE_AFTER_MOVE',f'QSTATE {val} is not live/owned',node)
    else: st.q_live[val]=False

def _infer(st,n):
    op=n.get('op'); attrs=n.get('attrs',{}); nid=n['id']
    st.effects |= effects_for_op(op)
    if op not in OP_EFFECTS: st.err('UNKNOWN_OPCODE',f'unknown operation {op}',nid); return TypeExpr('ANY')
    if op=='NOP': return TypeExpr('VOID')
    if op=='CONST': return TypeExpr('ANY')
    if op=='MOVE':
        t,v=_arg(st,n,0)
        if t.kind=='QSTATE': st.err('QSTATE_GENERIC_MOVE','generic MOVE cannot copy/move QSTATE',nid)
        return t
    if op=='HASH': _arg(st,n,0); return TypeExpr('HASH')
    if op=='FABRIC_MOUNT': return TypeExpr('FABRIC')
    if op=='FABRIC_ALLOC': _arg(st,n,0,'FABRIC'); return TypeExpr('REGION')
    if op=='FABRIC_READ': _arg(st,n,0,'FABRIC'); return TypeExpr('ANY')
    if op=='FABRIC_WRITE_OVERLAY': _arg(st,n,0,'FABRIC'); return TypeExpr('RECEIPT',('OVERLAY_WRITE',))
    if op=='GEO_INSTANTIATE':
        _arg(st,n,0,'FABRIC'); _arg(st,n,1,'REGION'); return TypeExpr('GEOMETRIC',('CLOSED','UNBOUND'))
    if op=='GEO_FORK':
        t,_=_arg(st,n,0,'GEOMETRIC'); return TypeExpr('GEOMETRIC',('CLOSED',sector_of(t) or 'UNBOUND'))
    if op=='RELATE': _arg(st,n,0,'GEOMETRIC'); return TypeExpr('RELATION')
    if op=='ADMIT': _arg(st,n,0,'GEOMETRIC'); return TypeExpr('ADMISSION')
    if op=='TRANSFORM':
        t,_=_arg(st,n,0,'GEOMETRIC'); _arg(st,n,1,'ADMISSION'); return TypeExpr('GEOMETRIC',('CLOSED',sector_of(t) or 'UNBOUND'))
    if op=='INHERIT': _arg(st,n,0); return TypeExpr('RECEIPT',('INHERIT',))
    if op=='PORTAL_OPEN':
        gt,gv=_arg(st,n,0,'GEOMETRIC'); _arg(st,n,1,'ADMISSION')
        sec=str(attrs.get('sector','GENERIC')).upper(); gsec=sector_of(gt)
        if gsec and gsec not in ('UNBOUND','GENERIC',sec):
            ok=any(b['geo']==gv and b['from']==gsec and b['to']==sec for b in st.bridges)
            if not ok: st.err('BRIDGE_REQUIRED',f'{gsec}->{sec} requires explicit BRIDGE_SECTOR for {gv}',nid)
        out=TypeExpr('PORTAL',(sec,'OPEN'))
        return out
    if op=='PORTAL_TRANSPORT':
        pt,pv=_arg(st,n,0,'PORTAL'); _portal_state(st,pv,nid); _arg(st,n,1,'GEOMETRIC')
        sec=sector_of(pt) or 'GENERIC'; return TypeExpr('GEOMETRIC',('CLOSED',sec))
    if op=='PORTAL_CLOSE':
        pt,pv=_arg(st,n,0,'PORTAL'); _portal_state(st,pv,nid); gt,_=_arg(st,n,1,'GEOMETRIC')
        psec=sector_of(pt); gsec=sector_of(gt)
        if psec and gsec and gsec not in ('UNBOUND','GENERIC',psec): st.err('SECTOR_MISMATCH',f'portal {psec} cannot close on {gsec} destination',nid)
        if pv is not None: st.portal[pv]='CLOSED'
        return TypeExpr('RECEIPT',('PORTAL_CLOSE',))
    if op=='ROAD_BEGIN': _arg(st,n,0,'GEOMETRIC'); return TypeExpr('ROAD',('OPEN',))
    if op=='ROAD_APPEND':
        _,rv=_arg(st,n,0,'ROAD'); _road_state(st,rv,nid); _arg(st,n,1,'RECEIPT')
        if rv is not None: st.road[rv]='MOVED'
        return TypeExpr('ROAD',('OPEN',))
    if op=='ROAD_CLOSE':
        _,rv=_arg(st,n,0,'ROAD'); _road_state(st,rv,nid); _arg(st,n,1,'GEOMETRIC')
        if rv is not None: st.road[rv]='CLOSED'
        return TypeExpr('RECEIPT',('ROAD_CLOSE',))
    if op=='BRIDGE_SECTOR':
        gt,gv=_arg(st,n,0,'GEOMETRIC'); fs=str(attrs.get('from','')).upper(); ts=str(attrs.get('to','')).upper()
        if not fs or not ts or fs==ts: st.err('BRIDGE_MISMATCH','Bridge requires distinct from/to sectors',nid)
        gsec=sector_of(gt)
        if gsec and gsec not in ('UNBOUND','GENERIC',fs): st.err('BRIDGE_MISMATCH',f'Bridge from {fs} does not match Geometric sector {gsec}',nid)
        st.bridges.append({'geo':gv,'from':fs,'to':ts,'node':nid})
        return TypeExpr('BRIDGE',(fs,ts))
    if op=='Q_PREPARE': _arg(st,n,0,'GEOMETRIC'); return TypeExpr('QSTATE',('OWNED',))
    if op in ('Q_SUPERPOSE','Q_CHANNEL'):
        _,q=_arg(st,n,0,'QSTATE'); _consume_q(st,q,nid); return TypeExpr('QSTATE',('OWNED',))
    if op=='Q_ENTANGLE':
        _,q1=_arg(st,n,0,'QSTATE'); _,q2=_arg(st,n,1,'QSTATE');
        if q1==q2 and q1 is not None: st.err('LINEAR_ALIAS',f'Q_ENTANGLE cannot consume same QSTATE twice: {q1}',nid)
        _consume_q(st,q1,nid); _consume_q(st,q2,nid); return TypeExpr('QSTATE',('OWNED',))
    if op=='Q_MEASURE':
        _,q=_arg(st,n,0,'QSTATE'); _consume_q(st,q,nid); return TypeExpr('QRESULT',('CLASSICAL',))
    if op=='BRANE_LIFT': _arg(st,n,0,'GEOMETRIC'); return TypeExpr('M5')
    if op=='PROVENANCE_SEAL': _arg(st,n,0); return TypeExpr('RECEIPT',('PROVENANCE',))
    if op=='ASSERT_CLOSURE': _arg(st,n,0); return TypeExpr('BOOL')
    if op=='EMIT_RECEIPT': return TypeExpr('RECEIPT',('EXECUTION',))
    if op in ('JUMP','CALL','RETURN','HALT'): return TypeExpr('VOID')
    if op=='BRANCH': _arg(st,n,0,'BOOL'); return TypeExpr('VOID')
    return TypeExpr('ANY')

def check_gir(gir,seed_types=None,module=None,effect_budget=None,export_values=None):
    seed={k:parse_type(v) for k,v in (seed_types or {}).items()}; st=State(seed,module)
    try: ordered=_schedule(gir,set(seed))
    except KeyError as e: st.err('UNKNOWN_VALUE',str(e)); return CheckResult(False,st.diags,st.types,st.effects,{})
    except ValueError as e:
        msg=str(e); code='NODE_DUPLICATE' if 'duplicate' in msg else 'DEPENDENCY_CYCLE'; st.err(code,msg); return CheckResult(False,st.diags,st.types,st.effects,{})
    for n in ordered:
        inferred=_infer(st,n); out=n.get('out')
        declared=n.get('type')
        if declared:
            try:
                if not compatible(parse_type(declared),inferred): st.err('TYPE_MISMATCH',f'declared {declared}, inferred {inferred}',n['id'])
            except ValueError as e: st.err('TYPE_SYNTAX',str(e),n['id'])
        if out:
            if out in st.types: st.err('VALUE_REDEFINITION',f'value {out} already defined',n['id'])
            st.types[out]=inferred
            if inferred.kind=='PORTAL': st.portal[out]='OPEN'
            if inferred.kind=='ROAD': st.road[out]='OPEN'
            if inferred.kind=='QSTATE': st.q_live[out]=True
            st.producers[out]=n['id']
    if effect_budget is not None:
        allowed=set(effect_budget); extra=st.effects-allowed
        if extra: st.err('EFFECT_BUDGET_EXCEEDED','undeclared effects: '+','.join(sorted(extra)))
    leakedp=sorted(k for k,v in st.portal.items() if v=='OPEN')
    leakedr=sorted(k for k,v in st.road.items() if v=='OPEN')
    if leakedp: st.err('PORTAL_UNCLOSED','open Portals at boundary: '+','.join(leakedp))
    if leakedr: st.err('ROAD_UNCLOSED','open Roads at boundary: '+','.join(leakedr))
    liveq=sorted(k for k,v in st.q_live.items() if v)
    exports=set(export_values or [])
    leakedq=[q for q in liveq if q not in exports]
    if leakedq: st.err('QSTATE_LEAK','owned QSTATE not consumed or exported: '+','.join(leakedq))
    witnesses={'checked_nodes':len(ordered),'bridge_witnesses':list(st.bridges),'open_portals':leakedp,'open_roads':leakedr,'live_qstate_exports':sorted(set(liveq)&exports)}
    return CheckResult(not any(d.severity=='ERROR' for d in st.diags),st.diags,st.types,st.effects,witnesses)

def check_module(mod,import_types=None):
    if mod.get('ir')!='GIR-MODULE':
        return CheckResult(False,[Diagnostic('MODULE_FORMAT','not GIR-MODULE',module=mod.get('module'))],{},set(),{})
    seeds={}
    for imp in mod.get('imports',[]): seeds[imp['local']]=imp.get('type','ANY')
    if import_types:
        for k,v in import_types.items(): seeds[k]=v
    exports=[e['value'] for e in mod.get('exports',[])]
    return check_gir(mod.get('gir',{}),seeds,mod.get('module'),mod.get('effects'),exports)
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/capabilities.py', r'''
from .model import Diagnostic
from .effects import effects_for_op, OP_EFFECTS

FEATURE_BY_OP={
'PORTAL_OPEN':'portal','PORTAL_TRANSPORT':'portal','PORTAL_CLOSE':'portal',
'ROAD_BEGIN':'rainbow_road','ROAD_APPEND':'rainbow_road','ROAD_CLOSE':'rainbow_road',
'BRIDGE_SECTOR':'sector_bridge',
'Q_PREPARE':'quantum_linear','Q_SUPERPOSE':'quantum_linear','Q_ENTANGLE':'quantum_linear','Q_CHANNEL':'quantum_linear','Q_MEASURE':'quantum_linear',
'EMIT_RECEIPT':'provenance_receipts','PROVENANCE_SEAL':'provenance_receipts'
}

def reference_backend_capabilities():
    return {'backend_id':'python-reference-backend','abi':'0.1','ops':sorted(OP_EFFECTS),'effects':sorted(set().union(*OP_EFFECTS.values())), 'sectors':['GENERIC','QFT','GR'], 'features':['portal','rainbow_road','sector_bridge','quantum_linear','provenance_receipts','brane_lift','immutable_fabric_overlay']}

def check_capabilities(gir,manifest):
    ds=[]
    if str(manifest.get('abi'))!='0.1': ds.append(Diagnostic('BACKEND_ABI_MISMATCH',f"backend ABI {manifest.get('abi')} != required 0.1"))
    ops=set(manifest.get('ops',[])); eff=set(manifest.get('effects',[])); sectors=set(x.upper() for x in manifest.get('sectors',[])); features=set(manifest.get('features',[]))
    req_ops={n.get('op') for n in gir.get('nodes',[])}
    for x in sorted(req_ops-ops): ds.append(Diagnostic('CAPABILITY_OP_MISSING',f'backend missing op {x}'))
    req_eff=set()
    for x in req_ops: req_eff |= effects_for_op(x)
    for x in sorted(req_eff-eff): ds.append(Diagnostic('CAPABILITY_EFFECT_MISSING',f'backend missing effect {x}'))
    req_sec=set()
    for n in gir.get('nodes',[]):
        if n.get('op')=='PORTAL_OPEN': req_sec.add(str(n.get('attrs',{}).get('sector','GENERIC')).upper())
        if n.get('op')=='BRIDGE_SECTOR':
            req_sec.add(str(n.get('attrs',{}).get('from','')).upper()); req_sec.add(str(n.get('attrs',{}).get('to','')).upper())
    req_sec.discard('')
    for x in sorted(req_sec-sectors): ds.append(Diagnostic('CAPABILITY_SECTOR_MISSING',f'backend missing sector {x}'))
    req_features={FEATURE_BY_OP[x] for x in req_ops if x in FEATURE_BY_OP}
    if any(n.get('op')=='BRANE_LIFT' for n in gir.get('nodes',[])): req_features.add('brane_lift')
    for x in sorted(req_features-features): ds.append(Diagnostic('CAPABILITY_FEATURE_MISSING',f'backend missing feature {x}'))
    return {'ok':not ds,'diagnostics':[d.as_dict() for d in ds],'required_ops':sorted(req_ops),'required_effects':sorted(req_eff),'required_sectors':sorted(req_sec),'required_features':sorted(req_features)}
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/proofs.py', r'''
def proof_ledger(check,cap,module_count,symbol_count,link_receipt=None):
    d=check.as_dict()
    codes={x['code'] for x in d['diagnostics']}
    def stat(blockers): return 'FAIL' if codes & set(blockers) else 'PASS'
    out=[
      {'id':'PO-SYMBOL-RESOLUTION','status':stat({'IMPORT_UNRESOLVED','EXPORT_UNRESOLVED','SYMBOL_DUPLICATE','MODULE_CYCLE'}),'witness':{'modules':module_count,'symbols':symbol_count}},
      {'id':'PO-TYPE-SAFETY','status':stat({'TYPE_MISMATCH','ARITY_MISMATCH','UNKNOWN_VALUE','TYPE_SYNTAX'}),'witness':{'checked_nodes':d['witnesses'].get('checked_nodes',0),'refined_values':len(d['value_types'])}},
      {'id':'PO-EFFECT-BOUNDS','status':stat({'EFFECT_BUDGET_EXCEEDED'}),'witness':{'effects':d['effects']}},
      {'id':'PO-LINEAR-OWNERSHIP','status':stat({'LINEAR_USE_AFTER_MOVE','LINEAR_ALIAS','QSTATE_GENERIC_MOVE','QSTATE_LEAK'}),'witness':{'live_exported':d['witnesses'].get('live_qstate_exports',[])}},
      {'id':'PO-CLOSURE','status':stat({'PORTAL_UNCLOSED','PORTAL_NOT_OPEN','ROAD_UNCLOSED','ROAD_NOT_OPEN'}),'witness':{'open_portals':d['witnesses'].get('open_portals',[]),'open_roads':d['witnesses'].get('open_roads',[])}},
      {'id':'PO-SECTOR-TRANSDUCTION','status':stat({'BRIDGE_REQUIRED','BRIDGE_MISMATCH','SECTOR_MISMATCH'}),'witness':{'bridges':d['witnesses'].get('bridge_witnesses',[])}},
      {'id':'PO-CAPABILITY','status':'PASS' if cap.get('ok') else 'FAIL','witness':{'required_features':cap.get('required_features',[])}},
      {'id':'PO-PROVENANCE','status':'PASS' if link_receipt is not None else 'PENDING','witness':{'link_receipt':None if link_receipt is None else link_receipt.get('link_id')}}
    ]
    return out
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/linker.py', r'''
from collections import defaultdict
from .errors import LinkError, CapabilityError
from .typesys import parse_type, compatible, erase_type
from .checker import check_gir
from .capabilities import check_capabilities, reference_backend_capabilities
from .proofs import proof_ledger
from .model import LinkResult
from .util import sha256_obj, sha256_bytes
from .vendor.genesis_vm import compile_gir, verify, encode

SUPPORTED_VERSION='0.1.0'

def _module_order(modules):
    names={m['module'] for m in modules}; deps={m['module']:set() for m in modules}; rev=defaultdict(set)
    for m in modules:
        for i in m.get('imports',[]):
            src=i.get('from')
            if src not in names: raise LinkError(f'IMPORT_UNRESOLVED: module {m["module"]} imports missing module {src}')
            deps[m['module']].add(src); rev[src].add(m['module'])
    ready=sorted(n for n,d in deps.items() if not d); out=[]
    while ready:
        x=ready.pop(0); out.append(x)
        for y in sorted(rev[x]):
            deps[y].discard(x)
            if not deps[y] and y not in out and y not in ready: ready.append(y); ready.sort()
    if len(out)!=len(names): raise LinkError('MODULE_CYCLE: '+','.join(sorted(names-set(out))))
    return out

def _interfaces(modules):
    table={}; byname={}
    for m in modules:
        name=m.get('module')
        if not name or name in byname: raise LinkError(f'MODULE_DUPLICATE: {name}')
        if m.get('ir')!='GIR-MODULE': raise LinkError(f'MODULE_FORMAT: {name}')
        if m.get('version','0.1.0')!=SUPPORTED_VERSION: raise LinkError(f'MODULE_VERSION: {name}')
        byname[name]=m
        seen=set()
        for e in m.get('exports',[]):
            sym=e['symbol']
            if sym in seen: raise LinkError(f'SYMBOL_DUPLICATE: {name}::{sym}')
            seen.add(sym); table[(name,sym)]={'module':name,'symbol':sym,'value':e['value'],'type':parse_type(e.get('type','ANY'))}
    return byname,table

def _validate_imports(modules,table):
    for m in modules:
        locals_=set()
        for i in m.get('imports',[]):
            loc=i['local']
            if loc in locals_: raise LinkError(f'SYMBOL_DUPLICATE: import alias {m["module"]}:{loc}')
            locals_.add(loc)
            key=(i['from'],i['symbol'])
            if key not in table: raise LinkError(f'IMPORT_UNRESOLVED: {m["module"]} -> {i["from"]}::{i["symbol"]}')
            if not compatible(i.get('type','ANY'),table[key]['type']): raise LinkError(f'IMPORT_TYPE_MISMATCH: {m["module"]}:{loc} requires {i.get("type")}, export is {table[key]["type"]}')

def link_bundle(bundle,backend=None):
    if bundle.get('link')!='GENESIS-LINK': raise LinkError('LINK_FORMAT')
    modules=list(bundle.get('modules',[])); byname,table=_interfaces(modules); _validate_imports(modules,table); order=_module_order(modules)
    global_values={}; renamed_by_module={}; module_hashes={}; nodes=[]; edges=[]
    # Allocate global names for every local producer first so imports can resolve independent of file order.
    for name in sorted(byname):
        m=byname[name]; ren={}
        for n in m.get('gir',{}).get('nodes',[]):
            if n.get('out'): ren[n['out']]=f'%{name}::{n["out"].lstrip("%")}'
        renamed_by_module[name]=ren; module_hashes[name]=sha256_obj(m)
    for (name,sym),e in table.items():
        if e['value'] not in renamed_by_module[name]: raise LinkError(f'EXPORT_UNRESOLVED: {name}::{sym} -> {e["value"]}')
        global_values[(name,sym)]=renamed_by_module[name][e['value']]
    # Merge in dependency order.
    for name in order:
        m=byname[name]; ren=renamed_by_module[name]
        imports={i['local']:global_values[(i['from'],i['symbol'])] for i in m.get('imports',[])}
        def rv(v):
            if isinstance(v,str) and v.startswith('%'):
                if v in imports: return imports[v]
                if v in ren: return ren[v]
            return v
        for n0 in m.get('gir',{}).get('nodes',[]):
            n=dict(n0); n['id']=f'{name}::{n0["id"]}'; n['args']=[rv(x) for x in n0.get('args',[])]
            if n0.get('out'): n['out']=ren[n0['out']]
            attrs=dict(n0.get('attrs',{}))
            # rewrite explicitly value-shaped attrs used by semantic witnesses
            for k,v in list(attrs.items()):
                if isinstance(v,str) and v.startswith('%'): attrs[k]=rv(v)
            n['attrs']=attrs
            nodes.append(n)
        for e0 in m.get('gir',{}).get('edges',[]):
            e=dict(e0); e['from']=f'{name}::{e0["from"]}'; e['to']=f'{name}::{e0["to"]}'; edges.append(e)
        # Every import-to-local-use dependency is already encoded by data arguments after substitution.
    requested=bundle.get('exports',[]); exports=[]
    for ref in requested:
        if '::' not in ref: raise LinkError(f'EXPORT_UNRESOLVED: malformed bundle export {ref}')
        mn,sym=ref.split('::',1); key=(mn,sym)
        if key not in global_values: raise LinkError(f'EXPORT_UNRESOLVED: {ref}')
        exports.append(global_values[key])
    # Compute refined seed-free linked check and preserve refinements as metadata.
    gir={'ir':'GIR','version':'0.1.0','name':bundle.get('name','linked_program'),'nodes':nodes,'edges':edges,'exports':exports}
    check=check_gir(gir,export_values=exports)
    if not check.ok: raise LinkError('STATIC_CHECK_FAILED: '+ '; '.join(f'{d.code}:{d.message}' for d in check.diagnostics))
    gir['metadata']={'section09':{'module_order':order,'module_hashes':module_hashes,'refined_types':{k:str(v) for k,v in sorted(check.value_types.items())},'linker':'section09-v0.1.0'}}
    cap=check_capabilities(gir,backend or reference_backend_capabilities())
    if not cap['ok']: raise CapabilityError('CAPABILITY_FAILED: '+ '; '.join(x['code']+':'+x['message'] for x in cap['diagnostics']))
    program=compile_gir(gir); verify(program); bytecode=encode(program)
    pre_receipt={'kind':'GENESIS_LINK_RECEIPT','version':'0.1.0','name':gir['name'],'modules':order,'module_hashes':module_hashes,'gir_hash':sha256_obj(gir),'gvm_sha256':sha256_bytes(bytecode),'backend':(backend or reference_backend_capabilities()).get('backend_id'),'exports':exports}
    receipt=dict(pre_receipt); receipt['link_id']='glnk-'+sha256_obj(pre_receipt)[:24]
    proofs=proof_ledger(check,cap,len(modules),len(table),receipt)
    if any(x['status']!='PASS' for x in proofs): raise LinkError('PROOF_LEDGER_FAILED')
    receipt['proof_root']=sha256_obj(proofs)
    return LinkResult(gir,program,bytecode,receipt,proofs,check)
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/__main__.py', r'''
import argparse,json,pathlib
from .linker import link_bundle
from .capabilities import reference_backend_capabilities
from .vendor.genesis_vm import disassemble, VM

def main():
    ap=argparse.ArgumentParser(prog='genesis_semantics'); sp=ap.add_subparsers(dest='cmd',required=True)
    l=sp.add_parser('link'); l.add_argument('bundle'); l.add_argument('-o','--out',required=True)
    c=sp.add_parser('check'); c.add_argument('bundle')
    a=ap.parse_args(); b=json.loads(pathlib.Path(a.bundle).read_text())
    r=link_bundle(b,reference_backend_capabilities())
    if a.cmd=='link':
        out=pathlib.Path(a.out); out.write_bytes(r.bytecode); print(json.dumps(r.receipt,indent=2,sort_keys=True))
    else: print(json.dumps({'receipt':r.receipt,'proofs':r.proofs,'check':r.check.as_dict()},indent=2,sort_keys=True))
if __name__=='__main__': main()
''')

# vendor Section08 genesis_vm for standalone part A
vendor_src=S08/'13_REFERENCE_IMPLEMENTATION/genesis_vm'
vendor_dst=PKG/'vendor/genesis_vm'
shutil.copytree(vendor_src,vendor_dst)
w('12_REFERENCE_IMPLEMENTATION/genesis_semantics/vendor/__init__.py','')
w('12_REFERENCE_IMPLEMENTATION/README.md', '''
# Reference implementation

Package: `genesis_semantics`

Bootstrap commands:

```bash
python -m genesis_semantics check bundle.json
python -m genesis_semantics link bundle.json -o program.gvm
```

The package vendors the current Section 08 `genesis_vm` implementation under `genesis_semantics.vendor.genesis_vm` so the Section 09 core ZIP is runnable by itself.
''')

# schemas
j('13_SCHEMAS/type_expr.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Genesis refined type expression','type':'string','pattern':'^[A-Za-z_][A-Za-z0-9_]*(<[^<>]+>)?$'})
j('13_SCHEMAS/gir_module.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':['ir','module','version','gir'],'properties':{'ir':{'const':'GIR-MODULE'},'module':{'type':'string','minLength':1},'version':{'const':'0.1.0'},'effects':{'type':'array','items':{'type':'string'},'uniqueItems':True},'imports':{'type':'array','items':{'type':'object','required':['local','from','symbol','type']}},'exports':{'type':'array','items':{'type':'object','required':['symbol','value','type']}},'gir':{'type':'object','required':['nodes','edges']}}})
j('13_SCHEMAS/link_bundle.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':['link','version','name','modules','exports'],'properties':{'link':{'const':'GENESIS-LINK'},'version':{'const':'0.1.0'},'name':{'type':'string'},'modules':{'type':'array','minItems':1},'exports':{'type':'array','items':{'type':'string'}}}})
j('13_SCHEMAS/backend_capabilities.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':['backend_id','abi','ops','effects','sectors','features'],'properties':{'backend_id':{'type':'string'},'abi':{'const':'0.1'},'ops':{'type':'array','items':{'type':'string'}},'effects':{'type':'array','items':{'type':'string'}},'sectors':{'type':'array','items':{'type':'string'}},'features':{'type':'array','items':{'type':'string'}}}})
j('13_SCHEMAS/link_receipt.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':['kind','version','link_id','gir_hash','gvm_sha256','proof_root'],'properties':{'kind':{'const':'GENESIS_LINK_RECEIPT'},'version':{'const':'0.1.0'},'link_id':{'type':'string'},'gir_hash':{'type':'string','pattern':'^[0-9a-f]{64}$'},'gvm_sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'},'proof_root':{'type':'string','pattern':'^[0-9a-f]{64}$'}}})

w('14_PSEUDOCODE/STATIC_CHECK.txt', r'''
CHECK(GIR, seed_types, effect_budget):
  schedule graph
  for node in dependency order:
    infer argument types
    enforce operation signature
    infer refined output type
    update Portal/Road/QSTATE typestate
    record explicit Bridge witnesses
    accumulate effects
  require effects <= budget
  require no OPEN Portal/Road leaks
  require no unconsumed non-exported QSTATE
  return diagnostics + type map + witnesses
''')
w('14_PSEUDOCODE/LINK.txt', r'''
LINK(bundle):
  interface_table <- all declared module exports
  validate all typed imports
  order <- topological(module dependency graph)
  alpha-rename node ids and SSA values by module
  substitute import aliases with exported global values
  merge nodes + edges
  select bundle exports
  static-check merged GIR
  capability-check target
  compile GIR through Section 08
  verify + encode GVM
  emit deterministic link receipt + proof ledger
''')

# ---------------- examples ----------------
def module(name,nodes,imports=None,exports=None,effects=None,edges=None):
    return {'ir':'GIR-MODULE','module':name,'version':'0.1.0','effects':effects or [],'imports':imports or [],'exports':exports or [],'gir':{'nodes':nodes,'edges':edges or []}}

fixture=module('fixture',[
 {'id':'01_mount','op':'FABRIC_MOUNT','out':'%fabric','type':'FABRIC','attrs':{'uri':'fabric://chirality/reference-v1'}},
 {'id':'02_alloc','op':'FABRIC_ALLOC','out':'%region','type':'REGION','args':['%fabric'],'attrs':{'cells':4096}},
 {'id':'03_geo','op':'GEO_INSTANTIATE','out':'%geo','type':'GEOMETRIC','args':['%fabric','%region'],'attrs':{'mmo':{'class':'MMO','handle':'@hydrogen_reference'}}},
],exports=[{'symbol':'geo','value':'%geo','type':'GEOMETRIC<CLOSED,UNBOUND>'}],effects=['READ_FABRIC','ALLOCATE','INHERIT'])
qft_leg=module('qft_leg',[
 {'id':'01_admit','op':'ADMIT','out':'%a','type':'ADMISSION','args':['%source'],'attrs':{'admitted':True}},
 {'id':'02_open','op':'PORTAL_OPEN','out':'%p','type':'PORTAL','args':['%source','%a'],'attrs':{'sector':'QFT','corridor':'QFT-A'}},
 {'id':'03_transport','op':'PORTAL_TRANSPORT','out':'%dest','type':'GEOMETRIC','args':['%p','%source'],'attrs':{'destination':'QFT-B'}},
 {'id':'04_close','op':'PORTAL_CLOSE','out':'%receipt','type':'RECEIPT','args':['%p','%dest']},
],imports=[{'local':'%source','from':'fixture','symbol':'geo','type':'GEOMETRIC'}],exports=[{'symbol':'destination','value':'%dest','type':'GEOMETRIC<CLOSED,QFT>'},{'symbol':'receipt','value':'%receipt','type':'RECEIPT<PORTAL_CLOSE>'}],effects=['ADMIT','TRANSPORT','INHERIT','CLOSE','PROVENANCE'])
readout=module('readout',[
 {'id':'01_m5','op':'BRANE_LIFT','out':'%m5','type':'M5','args':['%source'],'attrs':{'P':'section09-link'}},
 {'id':'02_seal','op':'PROVENANCE_SEAL','out':'%seal','type':'RECEIPT','args':['%m5'],'attrs':{'stage':'readout'}},
 {'id':'03_emit','op':'EMIT_RECEIPT','out':'%receipt','type':'RECEIPT'},
],imports=[{'local':'%source','from':'qft_leg','symbol':'destination','type':'GEOMETRIC<CLOSED,QFT>'}],exports=[{'symbol':'m5','value':'%m5','type':'M5'},{'symbol':'receipt','value':'%receipt','type':'RECEIPT'}],effects=['PROJECT','PROVENANCE'])
bridge=module('bridge',[
 {'id':'01_bridge','op':'BRIDGE_SECTOR','out':'%bridge','type':'BRIDGE','args':['%source'],'attrs':{'from':'QFT','to':'GR','preserve':['identity','chirality_ancestry','provenance']}},
],imports=[{'local':'%source','from':'qft_leg','symbol':'destination','type':'GEOMETRIC<CLOSED,QFT>'}],exports=[{'symbol':'bridge','value':'%bridge','type':'BRIDGE<QFT,GR>'},{'symbol':'source','value':'%source','type':'GEOMETRIC<CLOSED,QFT>'}],effects=['TRANSDUCE','PROVENANCE'])
# export of import alias not local producer is not supported by linker v0.1; adjust bridge exports only bridge and gr_leg imports source directly qft_leg.
bridge['exports']=[{'symbol':'bridge','value':'%bridge','type':'BRIDGE<QFT,GR>'}]
gr_leg=module('gr_leg',[
 {'id':'01_bridge','op':'BRIDGE_SECTOR','out':'%b','type':'BRIDGE','args':['%source'],'attrs':{'from':'QFT','to':'GR'}},
 {'id':'02_admit','op':'ADMIT','out':'%a','type':'ADMISSION','args':['%source'],'attrs':{'admitted':True,'bridge':'%b'}},
 {'id':'03_open','op':'PORTAL_OPEN','out':'%p','type':'PORTAL','args':['%source','%a'],'attrs':{'sector':'GR','corridor':'GR-B','bridge':'%b'}},
 {'id':'04_transport','op':'PORTAL_TRANSPORT','out':'%dest','type':'GEOMETRIC','args':['%p','%source'],'attrs':{'destination':'GR-C'}},
 {'id':'05_close','op':'PORTAL_CLOSE','out':'%receipt','type':'RECEIPT','args':['%p','%dest']},
],imports=[{'local':'%source','from':'qft_leg','symbol':'destination','type':'GEOMETRIC<CLOSED,QFT>'}],exports=[{'symbol':'destination','value':'%dest','type':'GEOMETRIC<CLOSED,GR>'},{'symbol':'receipt','value':'%receipt','type':'RECEIPT<PORTAL_CLOSE>'}],effects=['TRANSDUCE','PROVENANCE','ADMIT','TRANSPORT','INHERIT','CLOSE'])
quantum=module('quantum',[
 {'id':'01_q0','op':'Q_PREPARE','out':'%q0','type':'QSTATE','args':['%source'],'attrs':{'basis':['0','1']}},
 {'id':'02_q1','op':'Q_SUPERPOSE','out':'%q1','type':'QSTATE','args':['%q0'],'attrs':{'amplitudes':['1/sqrt(2)','1/sqrt(2)']}},
 {'id':'03_q2','op':'Q_CHANNEL','out':'%q2','type':'QSTATE','args':['%q1'],'attrs':{'channel':'IDENTITY','preserve_coherence':True}},
 {'id':'04_measure','op':'Q_MEASURE','out':'%result','type':'QRESULT','args':['%q2'],'attrs':{'outcome':0,'reference_seed':'SECTION09'}},
 {'id':'05_seal','op':'PROVENANCE_SEAL','out':'%seal','type':'RECEIPT','args':['%result'],'attrs':{'effect':'measurement'}},
],imports=[{'local':'%source','from':'fixture','symbol':'geo','type':'GEOMETRIC'}],exports=[{'symbol':'result','value':'%result','type':'QRESULT<CLASSICAL>'},{'symbol':'seal','value':'%seal','type':'RECEIPT<PROVENANCE>'}],effects=['QUANTUM_LINEAR','TRANSFORM','MEASURE','PROVENANCE'])
# Road module uses qft receipt to form and close a one-leg road over destination.
road=module('road',[
 {'id':'01_begin','op':'ROAD_BEGIN','out':'%r0','type':'ROAD','args':['%source']},
 {'id':'02_append','op':'ROAD_APPEND','out':'%r1','type':'ROAD','args':['%r0','%leg']},
 {'id':'03_close','op':'ROAD_CLOSE','out':'%rr','type':'RECEIPT','args':['%r1','%dest']},
],imports=[
 {'local':'%source','from':'fixture','symbol':'geo','type':'GEOMETRIC'},
 {'local':'%leg','from':'qft_leg','symbol':'receipt','type':'RECEIPT'},
 {'local':'%dest','from':'qft_leg','symbol':'destination','type':'GEOMETRIC<CLOSED,QFT>'}],
 exports=[{'symbol':'receipt','value':'%rr','type':'RECEIPT<ROAD_CLOSE>'}],effects=['TRANSPORT','INHERIT','CLOSE','PROVENANCE'])

mods=[fixture,qft_leg,readout,gr_leg,quantum,road]
for m in mods: j(f'17_EXAMPLES/modules/{m["module"]}.girmod.json',m)

bundles={
 'FIRST_PORTAL':{'link':'GENESIS-LINK','version':'0.1.0','name':'section09_first_portal','modules':[fixture,qft_leg,readout],'exports':['qft_leg::destination','qft_leg::receipt','readout::m5','readout::receipt']},
 'MIXED_SECTOR':{'link':'GENESIS-LINK','version':'0.1.0','name':'section09_mixed_sector','modules':[fixture,qft_leg,gr_leg],'exports':['gr_leg::destination','gr_leg::receipt']},
 'QUANTUM_EFFECT':{'link':'GENESIS-LINK','version':'0.1.0','name':'section09_quantum_effect','modules':[fixture,quantum],'exports':['quantum::result','quantum::seal']},
 'RAINBOW_ROAD':{'link':'GENESIS-LINK','version':'0.1.0','name':'section09_rainbow_road','modules':[fixture,qft_leg,road],'exports':['qft_leg::destination','road::receipt']},
}
for k,b in bundles.items(): j(f'17_EXAMPLES/bundles/{k}.link.json',b)
w('17_EXAMPLES/README.md','''# Examples\n\nFour semantic-link bundles exercise typed imports/exports, alpha-renaming, Portal closure, Road composition, explicit QFT→GR Bridge use, and linear quantum effects.\n''')

# Run linker/reference VM and save linked outputs.
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION'))
from genesis_semantics import link_bundle, reference_backend_capabilities
from genesis_semantics.vendor.genesis_vm import decode, disassemble, VM
ref_results={}
for name,b in bundles.items():
    r=link_bundle(b,reference_backend_capabilities())
    d=ROOT/'18_REFERENCE_LINKED_PROGRAMS'/name; d.mkdir(parents=True,exist_ok=True)
    j(f'18_REFERENCE_LINKED_PROGRAMS/{name}/linked.gir.json',r.gir)
    (d/'linked.gvm').write_bytes(r.bytecode)
    (d/'linked.disasm.txt').write_text(disassemble(r.program),encoding='utf-8')
    j(f'18_REFERENCE_LINKED_PROGRAMS/{name}/link_receipt.json',r.receipt)
    j(f'18_REFERENCE_LINKED_PROGRAMS/{name}/proof_ledger.json',r.proofs)
    j(f'18_REFERENCE_LINKED_PROGRAMS/{name}/static_check.json',r.check.as_dict())
    run=VM().run(decode(r.bytecode))
    j(f'18_REFERENCE_LINKED_PROGRAMS/{name}/run_receipt.json',run.receipt)
    ref_results[name]={'link_id':r.receipt['link_id'],'gir_hash':r.receipt['gir_hash'],'gvm_sha256':r.receipt['gvm_sha256'],'proof_root':r.receipt['proof_root'],'proofs':len(r.proofs),'run_receipt_id':run.receipt['resource_id'],'halted':run.halted}

# ---------------- tests ----------------
# Dynamic tests provide many independent assertions while keeping source readable.
w('16_TESTS/test_section09.py', r'''
import unittest, json, copy, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION'))
from genesis_semantics.typesys import parse_type,compatible,erase_type
from genesis_semantics.checker import check_gir,check_module
from genesis_semantics.effects import effects_for_op
from genesis_semantics.capabilities import reference_backend_capabilities,check_capabilities
from genesis_semantics.linker import link_bundle
from genesis_semantics.errors import LinkError,CapabilityError
from genesis_semantics.vendor.genesis_vm import decode,verify,VM

BUNDLES={p.stem.split('.')[0]:json.loads(p.read_text()) for p in (ROOT/'17_EXAMPLES/bundles').glob('*.json')}
MODS={p.stem.split('.')[0]:json.loads(p.read_text()) for p in (ROOT/'17_EXAMPLES/modules').glob('*.json')}

def gir(nodes,exports=None,edges=None): return {'ir':'GIR','version':'0.1.0','name':'test','nodes':nodes,'edges':edges or [],'exports':exports or []}

class TestTypes(unittest.TestCase): pass
TYPE_CASES=[
 ('FABRIC','FABRIC'),('GEOMETRIC<CLOSED,QFT>','GEOMETRIC<CLOSED,QFT>'),('PORTAL<GR,OPEN>','PORTAL<GR,OPEN>'),('ROAD<OPEN>','ROAD<OPEN>'),('QSTATE<OWNED>','QSTATE<OWNED>'),('BRIDGE<QFT,GR>','BRIDGE<QFT,GR>'),('RECEIPT<PORTAL_CLOSE>','RECEIPT<PORTAL_CLOSE>'),
]
for idx,(src,expect) in enumerate(TYPE_CASES):
    def t(self,src=src,expect=expect): self.assertEqual(str(parse_type(src)),expect)
    setattr(TestTypes,f'test_parse_{idx:02d}',t)
COMPAT=[('GEOMETRIC','GEOMETRIC<CLOSED,QFT>',True),('GEOMETRIC<CLOSED,QFT>','GEOMETRIC<CLOSED,QFT>',True),('GEOMETRIC<CLOSED,GR>','GEOMETRIC<CLOSED,QFT>',False),('ANY','QSTATE<OWNED>',True),('PORTAL<QFT>','PORTAL<QFT,OPEN>',True),('PORTAL<GR>','PORTAL<QFT,OPEN>',False)]
for idx,(a,b,ok) in enumerate(COMPAT):
    def t(self,a=a,b=b,ok=ok): self.assertEqual(compatible(a,b),ok)
    setattr(TestTypes,f'test_compat_{idx:02d}',t)

class TestEffects(unittest.TestCase): pass
EFF=[('FABRIC_MOUNT','READ_FABRIC'),('FABRIC_ALLOC','ALLOCATE'),('ADMIT','ADMIT'),('PORTAL_CLOSE','CLOSE'),('BRIDGE_SECTOR','TRANSDUCE'),('Q_MEASURE','MEASURE'),('BRANE_LIFT','PROJECT'),('EMIT_RECEIPT','PROVENANCE')]
for idx,(op,e) in enumerate(EFF):
    def t(self,op=op,e=e): self.assertIn(e,effects_for_op(op))
    setattr(TestEffects,f'test_effect_{idx:02d}',t)

class TestModules(unittest.TestCase):
    def test_fixture_module(self): self.assertTrue(check_module(MODS['fixture']).ok)
    def test_qft_module_seeded(self): self.assertTrue(check_module(MODS['qft_leg']).ok)
    def test_quantum_module(self): self.assertTrue(check_module(MODS['quantum']).ok)
    def test_effect_budget_failure(self):
        m=copy.deepcopy(MODS['fixture']); m['effects']=[]; r=check_module(m); self.assertFalse(r.ok); self.assertTrue(any(d.code=='EFFECT_BUDGET_EXCEEDED' for d in r.diagnostics))
    def test_unknown_value(self):
        r=check_gir(gir([{'id':'x','op':'ADMIT','out':'%a','args':['%missing'],'type':'ADMISSION'}])); self.assertFalse(r.ok)
    def test_unclosed_portal(self):
        n=[{'id':'m','op':'FABRIC_MOUNT','out':'%f','type':'FABRIC'},{'id':'a','op':'FABRIC_ALLOC','out':'%r','args':['%f'],'type':'REGION'},{'id':'g','op':'GEO_INSTANTIATE','out':'%g','args':['%f','%r'],'type':'GEOMETRIC'},{'id':'ad','op':'ADMIT','out':'%a','args':['%g'],'type':'ADMISSION'},{'id':'p','op':'PORTAL_OPEN','out':'%p','args':['%g','%a'],'attrs':{'sector':'QFT'},'type':'PORTAL'}]
        r=check_gir(gir(n)); self.assertFalse(r.ok); self.assertTrue(any(d.code=='PORTAL_UNCLOSED' for d in r.diagnostics))
    def test_qstate_double_use(self):
        n=[{'id':'m','op':'FABRIC_MOUNT','out':'%f','type':'FABRIC'},{'id':'a','op':'FABRIC_ALLOC','out':'%r','args':['%f'],'type':'REGION'},{'id':'g','op':'GEO_INSTANTIATE','out':'%g','args':['%f','%r'],'type':'GEOMETRIC'},{'id':'q','op':'Q_PREPARE','out':'%q','args':['%g'],'type':'QSTATE'},{'id':'q1','op':'Q_CHANNEL','out':'%q1','args':['%q'],'type':'QSTATE'},{'id':'q2','op':'Q_CHANNEL','out':'%q2','args':['%q'],'type':'QSTATE'},{'id':'m1','op':'Q_MEASURE','out':'%x','args':['%q1'],'type':'QRESULT'},{'id':'m2','op':'Q_MEASURE','out':'%y','args':['%q2'],'type':'QRESULT'}]
        r=check_gir(gir(n)); self.assertFalse(r.ok); self.assertTrue(any(d.code=='LINEAR_USE_AFTER_MOVE' for d in r.diagnostics))
    def test_qstate_generic_move(self):
        n=[{'id':'m','op':'FABRIC_MOUNT','out':'%f','type':'FABRIC'},{'id':'a','op':'FABRIC_ALLOC','out':'%r','args':['%f'],'type':'REGION'},{'id':'g','op':'GEO_INSTANTIATE','out':'%g','args':['%f','%r'],'type':'GEOMETRIC'},{'id':'q','op':'Q_PREPARE','out':'%q','args':['%g'],'type':'QSTATE'},{'id':'mv','op':'MOVE','out':'%q2','args':['%q'],'type':'QSTATE'}]
        r=check_gir(gir(n,exports=['%q2']),export_values=['%q2']); self.assertFalse(r.ok); self.assertTrue(any(d.code=='QSTATE_GENERIC_MOVE' for d in r.diagnostics))

class TestLinker(unittest.TestCase): pass
for idx,key in enumerate(['FIRST_PORTAL','MIXED_SECTOR','QUANTUM_EFFECT','RAINBOW_ROAD']):
    def t(self,key=key):
        r=link_bundle(BUNDLES[key],reference_backend_capabilities()); self.assertTrue(r.check.ok); self.assertEqual(len(r.proofs),8); self.assertTrue(all(x['status']=='PASS' for x in r.proofs)); self.assertTrue(verify(decode(r.bytecode))['ok']); self.assertTrue(VM().run(decode(r.bytecode)).halted)
    setattr(TestLinker,f'test_link_execute_{idx:02d}',t)

class TestLinkFailures(unittest.TestCase):
    def test_missing_module(self):
        b=copy.deepcopy(BUNDLES['FIRST_PORTAL']); b['modules']=[m for m in b['modules'] if m['module']!='fixture']
        with self.assertRaises(LinkError): link_bundle(b)
    def test_import_type_mismatch(self):
        b=copy.deepcopy(BUNDLES['FIRST_PORTAL']); q=next(m for m in b['modules'] if m['module']=='qft_leg'); q['imports'][0]['type']='GEOMETRIC<CLOSED,GR>'
        with self.assertRaises(LinkError): link_bundle(b)
    def test_duplicate_module(self):
        b=copy.deepcopy(BUNDLES['FIRST_PORTAL']); b['modules'].append(copy.deepcopy(b['modules'][0]))
        with self.assertRaises(LinkError): link_bundle(b)
    def test_module_cycle(self):
        b=copy.deepcopy(BUNDLES['FIRST_PORTAL']); f=next(m for m in b['modules'] if m['module']=='fixture'); f['imports']=[{'local':'%x','from':'readout','symbol':'m5','type':'M5'}]
        with self.assertRaises(LinkError): link_bundle(b)
    def test_missing_backend_op(self):
        cap=reference_backend_capabilities(); cap['ops']=[x for x in cap['ops'] if x!='PORTAL_OPEN']
        with self.assertRaises(CapabilityError): link_bundle(BUNDLES['FIRST_PORTAL'],cap)
    def test_missing_sector(self):
        cap=reference_backend_capabilities(); cap['sectors']=['GENERIC','QFT']
        with self.assertRaises(CapabilityError): link_bundle(BUNDLES['MIXED_SECTOR'],cap)
    def test_missing_feature(self):
        cap=reference_backend_capabilities(); cap['features']=[x for x in cap['features'] if x!='quantum_linear']
        with self.assertRaises(CapabilityError): link_bundle(BUNDLES['QUANTUM_EFFECT'],cap)

class TestDeterminism(unittest.TestCase):
    def test_input_order_independent(self):
        b=copy.deepcopy(BUNDLES['FIRST_PORTAL']); r1=link_bundle(b); b['modules']=list(reversed(b['modules'])); r2=link_bundle(b); self.assertEqual(r1.receipt['gvm_sha256'],r2.receipt['gvm_sha256']); self.assertEqual(r1.receipt['gir_hash'],r2.receipt['gir_hash'])
    def test_same_link_id(self):
        r1=link_bundle(BUNDLES['MIXED_SECTOR']); r2=link_bundle(copy.deepcopy(BUNDLES['MIXED_SECTOR'])); self.assertEqual(r1.receipt['link_id'],r2.receipt['link_id'])
    def test_alpha_names(self):
        r=link_bundle(BUNDLES['FIRST_PORTAL']); self.assertTrue(all('::' in n['id'] for n in r.gir['nodes'])); self.assertTrue(all(x.startswith('%') and '::' in x for x in r.gir['exports']))
    def test_refined_metadata(self):
        r=link_bundle(BUNDLES['MIXED_SECTOR']); md=r.gir['metadata']['section09']['refined_types']; self.assertTrue(any(v=='GEOMETRIC<CLOSED,GR>' for v in md.values()))
''')

# run tests
p=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'16_TESTS'),'-v'],capture_output=True,text=True)
(ROOT/'99_RELEASE/TEST_RESULTS.txt').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
if p.returncode!=0:
    print(p.stdout); print(p.stderr,file=sys.stderr); raise SystemExit(p.returncode)
# count tests from summary
summary=(p.stdout+'\n'+p.stderr).splitlines()
count=None
for line in summary:
    if line.startswith('Ran ') and ' tests' in line:
        try: count=int(line.split()[1])
        except: pass

j('99_RELEASE/REFERENCE_LINK_RESULTS.json',ref_results)

# docs after execution
w('19_SOURCE_CROSSWALK/SOURCE_CROSSWALK.md', r'''
# Source crosswalk

Section 09 is an **implementation synthesis**. Earlier source layers did not literally specify this linker or typechecker.

- **Section 01** constrains fabric authority and immutable-base semantics.
- **Sections 02–03** constrain identity-bearing Geometric versioning and append-only transformation ancestry.
- **Sections 04–05** constrain Portal/Road closure and persistent transport composition.
- **Section 06** requires explicit QFT/GR transduction rather than representation collapse.
- **Section 07** constrains linear quantum ownership, channels, and measurement effects.
- **Section 08** is the direct execution-model parent: GIR, GVM, coarse type tags, effects, verifier, bytecode, and backend ABI.
- **Astraeus mathematics** supplies conceptual constraints for admissibility, bandwidth, resolution, identity-through-history, chirality transport, and holonomy.
- **Layer Zero / prior Computational Genesis** provide precursor compiler/IR hypotheses.

Section 09's refined types, module format, proof ledger, and semantic linker are new computational architecture derived from those constraints.
''')
w('19_SOURCE_CROSSWALK/STATUS_DISCIPLINE.md', r'''
# Status discipline

Do not promote static checker success into a claim of physical validation.

A Section 09 PASS means:

- the encoded graph satisfied this implemented static ruleset;
- imports and symbols resolved;
- type/effect/ownership/closure/sector obligations passed;
- the selected backend capability manifest covered the program;
- Section 08 accepted the lowered GVM.

It does not by itself prove a scientific interpretation, hardware realization, or arbitrary functional correctness.
''')
w('20_RECOVERY/SECTION_09_STATE.md', f'''
# Section 09 recovery state

**Folder:** `{ROOT.name}`  
**Version:** 0.1.0  
**Date:** 2026-08-21

State:

- refined parametric type model implemented;
- Portal/Road typestate checker implemented;
- QSTATE linear ownership checker implemented;
- explicit Bridge-sector witness checking implemented;
- effect-budget checker implemented;
- GIR semantic module import/export format implemented;
- deterministic symbol resolver and alpha-renaming linker implemented;
- backend capability contract implemented;
- 8-obligation static proof ledger implemented;
- Section 08 compiler/verifier/bytecode integration implemented;
- four modular linked reference programs compile and execute in the Python reference backend;
- unit/integration suite: **{count} tests PASS**.

Next natural section: **Section 10 — Genesis Source Frontend / Parser + Surface Syntax**, unless architecture work chooses to insert an optimizer/monomorphization pass first.
''')

# core manifest/checksums
files=[]
for pth in ROOT.rglob('*'):
    if pth.is_file() and '99_RELEASE/CORE_CHECKSUMS.sha256' not in str(pth) and '99_RELEASE/CORE_MANIFEST.json' not in str(pth):
        rel=pth.relative_to(ROOT).as_posix(); h=hashlib.sha256(pth.read_bytes()).hexdigest(); files.append((rel,pth.stat().st_size,h))
(ROOT/'99_RELEASE/CORE_CHECKSUMS.sha256').write_text(''.join(f'{h}  {rel}\n' for rel,sz,h in sorted(files)),encoding='utf-8')
j('99_RELEASE/CORE_MANIFEST.json',{'name':ROOT.name,'version':'0.1.0','date':'2026-08-21','section':9,'title':'Static Type/Effect Checker + Semantic Linker','files':len(files),'bytes':sum(x[1] for x in files),'tests_passed':count,'reference_links':ref_results,'source_parent':'Section 08 GIR/GVM'})
shutil.copy2('/mnt/data/_build_section09.py',ROOT/'98_BUILD/_build_section09.py')
print(json.dumps({'root':str(ROOT),'tests':count,'reference':ref_results},indent=2))
