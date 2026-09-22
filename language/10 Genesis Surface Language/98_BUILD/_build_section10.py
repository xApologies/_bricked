from pathlib import Path
import shutil, textwrap, json, hashlib, os, re, subprocess, sys, zipfile, shlex

ROOT=Path('/mnt/data/GENESIS_CHIRALITY_MACHINE_SECTION_10_GENESIS_FRONTEND_v0.1.0_20260821')
S09=Path('/mnt/data/GENESIS_CHIRALITY_MACHINE_SECTION_09_STATIC_SEMANTICS_LINKER_v0.1.0_20260821')
if ROOT.exists(): shutil.rmtree(ROOT)
DIRS=[
'00_START_HERE','01_ARCHITECTURE','02_LANGUAGE_BOUNDARY','03_LEXICAL_MODEL','04_GRAMMAR','05_AST','06_SOURCE_TYPES','07_FRONTEND_EFFECTS','08_LOWERING','09_SOURCE_MAP_PROVENANCE','10_COMPILER_PIPELINE','11_DIAGNOSTICS','12_REFERENCE_IMPLEMENTATION/genesis_frontend/vendor','13_SCHEMAS','14_PSEUDOCODE','15_TESTS','16_EXAMPLES/MODULAR_QFT','17_REFERENCE_BUILDS','18_SOURCE_CROSSWALK','19_RECOVERY','98_BUILD','99_RELEASE'
]
for d in DIRS:(ROOT/d).mkdir(parents=True,exist_ok=True)

def w(rel,s):
 p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(textwrap.dedent(s).lstrip(),encoding='utf-8')
def j(rel,o):
 p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,sort_keys=True),encoding='utf-8')
def sha_file(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def canon(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha_obj(o): return hashlib.sha256(canon(o)).hexdigest()

w('00_START_HERE/FOLDER_NAME.txt',ROOT.name+'\n')
w('00_START_HERE/README.md',r'''
# Genesis Chirality Machine — Section 10
## Genesis Surface Language + Frontend Compiler

**Version:** 0.1.0  
**Date:** 2026-08-21

Section 10 is the first executable textual projection of the Genesis programming language.

Sections 01–09 established the machine below it: chirality hardware ABI, Geometric instantiation, transformations, Portals, Rainbow Road, QFT/GR transduction, quantum-information effects, GIR/GVM, and static semantics/linking. Section 10 adds the frontend that converts source text into that already-defined semantic machine.

```text
Genesis source (.gen)
      |
      v
lexer / statement parser
      |
      v
Genesis AST
      |
      v
semantic lowering + source map
      |
      v
GIR-MODULE
      |
      v
Section 09 static checker + semantic linker
      |
      v
Section 08 GIR/GVM compiler
      |
      v
Sections 01–07 backends
```

### Critical architectural law

**The text is a projection of the program; the typed relationship graph is the executable semantic object.**

The v0.1 frontend therefore does not redefine the machine semantics. It only provides a deterministic way to name, relate, transform, transport, close, and export objects that Section 09 can verify.

### Source Genesis boundary

The computational language intentionally borrows relationship-first mnemonic roots such as `en`, `rel`, `ve`, `ar`, and `tor` from the reconstructed Source Genesis corpus. This does **not** claim that the historical/reconstructed spoken language already contained compiler semantics. Source Genesis and Computational Genesis remain distinct source layers.
''')
w('00_START_HERE/RECOVERY_ORDER.md',r'''
# Recovery order

1. Part A — Section 10 frontend/compiler core, specs, implementation, examples, tests, and reference builds.
2. Part B — frontend reference execution corpus plus the Section 09 linked-execution oracle corpus.
3. Part C — implementation lineage: Sections 01–09 cores, Layer Zero, CFP, Corridor/Rainbow Road, and prior Computational Genesis handoff.
4. Part D — Source Genesis linguistic corpus used to constrain the relationship-first surface projection.
5. Part E — mathematical/API/QFT-GR semantic reference corpus.

Part A is sufficient to recover and run the Section 10 compiler against its vendored Section 09/08 bootstrap stack.
''')

w('01_ARCHITECTURE/ARCHITECTURE.md',r'''
# Frontend architecture

```text
                 .gen source
                    |
              UTF-8 lexical layer
                    |
          one-statement-per-line parser
                    |
              typed source AST
                    |
       +------------+------------+
       |                         |
  source map                 diagnostics
       |                         |
       +------------+------------+
                    |
             semantic lowerer
                    |
                GIR-MODULE
                    |
              Section 09
        static checker / linker
                    |
                Section 08
                 GVM
```

The parser is deliberately small. All difficult legality questions remain where they belong: Section 09. The frontend cannot grant itself transport authority, evade linear ownership, erase a required QFT/GR bridge, leave a Portal open, or invent a backend capability.
''')
w('01_ARCHITECTURE/DESIGN_INVARIANTS.md',r'''
# Design invariants

1. Source text never becomes semantic authority over GIR/Section 09.
2. One source declaration produces at most one SSA value.
3. Source variable names lower deterministically to `%name` GIR values.
4. Every executable source statement receives a stable source-map entry.
5. v0.1 preserves textual effect order with explicit `effect_order` edges; later optimizers may relax only proven-commutative edges.
6. Effect budgets are compiler-derived from lowered operations, not trusted from source declarations.
7. Export types are explicit interface contracts and are checked by Section 09.
8. Imported symbols retain module provenance and refined type declarations.
9. Quantum QSTATE values remain linear after lowering; there is no frontend copy escape hatch.
10. QFT/GR changes require explicit `bridge` syntax and lower to `BRIDGE_SECTOR`.
11. `ve` lowers to Portal transport, not to entanglement or magical nonlocal transfer.
12. `tor` lowers to explicit closure and cannot be silently inserted to make an invalid program pass.
13. Source Genesis linguistic material is a mnemonic/design source, not retroactively rewritten as compiler history.
14. Canonical source formatting is deterministic.
15. Python is the bootstrap frontend implementation, not the definition of Genesis semantics.
''')

w('02_LANGUAGE_BOUNDARY/SOURCE_VS_COMPUTATIONAL_GENESIS.md',r'''
# Source Genesis vs Computational Genesis

The reconstructed language corpus states that Genesis is relationship-first and commonly organizes expression around topic/context, relationship, identity, and resolution. Section 10 uses that worldview to choose surface forms, but creates a **new programming notation**.

Borrowed mnemonic correspondences in the executable core:

| Computational token | Surface role | Source-family inspiration |
|---|---|---|
| `en` | bind a typed identity/result | identity |
| `rel` | establish a relationship | relationship |
| `ve` | Portal-mediated transport | propagate/toward |
| `ar` | explicit inheritance operation | inherit |
| `tor` | close a Portal | closure |

The compiler meaning is defined only by Section 10 lowering rules and Sections 08–09 semantics.
''')
w('02_LANGUAGE_BOUNDARY/RELATIONSHIP_FIRST_RULE.md',r'''
# Relationship-first rule

Genesis source should make relationships and state transitions visible rather than burying them inside object-method syntax.

Preferred:

```genesis
rel g0 -> "environment://trinity" as r
portal GR g0 with adm as p corridor "Red->Violet"
ve g0 through p -> "trinity://node-B" as g1
tor p with g1 as receipt
```

Not the native canonical projection:

```text
g0.portal(GR).send(nodeB).close()
```

The canonical form exposes source, relation/route, destination, and closure as separate graph-producing statements.
''')

w('03_LEXICAL_MODEL/LEXICAL_SPEC.md',r'''
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
''')
w('03_LEXICAL_MODEL/RESERVED_WORDS.md',r'''
# Reserved words

`genesis module use export en rel admit transform ar portal ve tor road begin append close bridge q prepare superpose entangle channel measure lift seal assert closure emit receipt mount alloc instantiate fork cells mmo with as corridor through`

Reserved future relationship-first roots include `sha`, `da`, `tal`, `nor`, and explicit normalization/stabilization forms. They are not assigned accidental v0.1 machine meanings merely to fill vocabulary.
''')

w('04_GRAMMAR/GRAMMAR_EBNF.md',r'''
# Executable grammar v0.1

```ebnf
file        = version, module ;
version     = "genesis", "0.1.0" ;
module      = "module", qname, "{", { item }, "}" ;
item        = use | export | statement ;

use         = "use", qname, "::", ident, "as", ident, ":", type ;
export      = "export", ident, ":", type ;

statement   = identity_stmt | relation_stmt | admit_stmt | transform_stmt
            | inherit_stmt | portal_stmt | transport_stmt | close_stmt
            | road_stmt | bridge_stmt | quantum_stmt | lift_stmt
            | seal_stmt | closure_assert | emit_stmt ;

identity_stmt = "en", ident, ":", type, "=",
                ( "mount", string
                | "alloc", ident, "cells", integer
                | "instantiate", ident, ident, "mmo", handle
                | "fork", ident ), [ attrs ] ;

relation_stmt = "rel", ident, "->", atom, "as", ident, [ attrs ] ;
admit_stmt    = "admit", ident, "as", ident, [ attrs ] ;
transform_stmt= "transform", ident, "with", ident, "as", ident, [ attrs ] ;
inherit_stmt  = "ar", ident, "as", ident, [ attrs ] ;
portal_stmt   = "portal", sector, ident, "with", ident, "as", ident,
                "corridor", string, [ "bridge", ident ], [ attrs ] ;
transport_stmt= "ve", ident, "through", ident, "->", atom, "as", ident, [ attrs ] ;
close_stmt    = "tor", ident, "with", ident, "as", ident, [ attrs ] ;
road_stmt     = "road", ( "begin", ident, "as", ident
                         | "append", ident, ident, "as", ident
                         | "close", ident, ident, "as", ident ), [ attrs ] ;
bridge_stmt   = "bridge", ident, sector, "->", sector, "as", ident, [ attrs ] ;
quantum_stmt  = "q", ( "prepare", ident, "as", ident
                      | "superpose", ident, "as", ident
                      | "entangle", ident, ident, "as", ident
                      | "channel", ident, "as", ident
                      | "measure", ident, "as", ident ), [ attrs ] ;
lift_stmt     = "lift", ident, "as", ident, [ attrs ] ;
seal_stmt     = "seal", ident, "as", ident, [ attrs ] ;
closure_assert= "assert", "closure", ident, "as", ident, [ attrs ] ;
emit_stmt     = "emit", "receipt", "as", ident, [ attrs ] ;

attrs       = "@", json_object ;
sector      = "GENERIC" | "QFT" | "GR" ;
```

This grammar is the canonical executable projection for Section 10 v0.1. It is intentionally smaller than the total conceptual Genesis vocabulary.
''')
w('04_GRAMMAR/SURFACE_EXAMPLES.md',r'''
# Surface examples

```genesis
genesis 0.1.0
module first_portal {
  en fabric : FABRIC = mount "fabric://chirality/reference-v1"
  en region : REGION = alloc fabric cells 4096
  en g0 : GEOMETRIC = instantiate fabric region mmo @hydrogen_reference
  rel g0 -> "environment://trinity" as relation
  admit g0 as adm @{"admitted":true,"bandwidth":1.0,"resolution":1.0}
  transform g0 with adm as g1 @{"kind":"identity-preserving-reference-transform"}
  portal GR g1 with adm as p corridor "corridor://red-violet"
  ve g1 through p -> "trinity://node-B" as g2
  tor p with g2 as portal_receipt
  lift g2 as m5 @{"P":"receipt-ledger","R":"closed"}
  export g2 : GEOMETRIC<CLOSED,GR>
  export portal_receipt : RECEIPT<PORTAL_CLOSE>
  export m5 : M5
}
```
''')

w('05_AST/AST_MODEL.md',r'''
# AST model

The AST is intentionally semantic-light. It records:

- module name and source version;
- typed imports;
- executable statements with source line, operation family, output identity, arguments, attributes, and optional declared type;
- explicit exports.

It does not decide whether a Portal may cross a sector boundary, whether a QSTATE has been moved, or whether closure is complete. Those are Section 09 obligations after lowering.
''')
w('06_SOURCE_TYPES/TYPE_PROJECTION.md',r'''
# Source type projection

Source annotations use Section 09 refined type syntax on interfaces. Node result declarations lower to the stable Section 08 coarse VM type tag.

Examples:

```text
source export                         node/GVM type
GEOMETRIC<CLOSED,QFT>       ->        GEOMETRIC
PORTAL<GR,OPEN>              ->        PORTAL
QSTATE<OWNED>                ->        QSTATE
RECEIPT<PORTAL_CLOSE>        ->        RECEIPT
```

This keeps source interfaces expressive without teaching the Section 08 bytecode encoder a second parametric type grammar.
''')
w('07_FRONTEND_EFFECTS/EFFECT_DERIVATION.md',r'''
# Frontend effect derivation

A source module does not self-declare its authority budget in v0.1. The compiler derives the exact effect set from lowered GIR operations using the Section 09 opcode/effect table.

This prevents source text from hiding an operation behind a weaker declared budget. Section 09 then checks that the derived budget matches the graph it receives.
''')
w('08_LOWERING/LOWERING_TABLE.md',r'''
# Surface-to-GIR lowering

| Source form | GIR operation |
|---|---|
| `en x = mount ...` | `FABRIC_MOUNT` |
| `en x = alloc ...` | `FABRIC_ALLOC` |
| `en x = instantiate ...` | `GEO_INSTANTIATE` |
| `en x = fork ...` | `GEO_FORK` |
| `rel` | `RELATE` |
| `admit` | `ADMIT` |
| `transform` | `TRANSFORM` |
| `ar` | `INHERIT` |
| `portal` | `PORTAL_OPEN` |
| `ve` | `PORTAL_TRANSPORT` |
| `tor` | `PORTAL_CLOSE` |
| `road begin/append/close` | `ROAD_BEGIN/ROAD_APPEND/ROAD_CLOSE` |
| `bridge` | `BRIDGE_SECTOR` |
| `q prepare/superpose/entangle/channel/measure` | corresponding `Q_*` op |
| `lift` | `BRANE_LIFT` |
| `seal` | `PROVENANCE_SEAL` |
| `assert closure` | `ASSERT_CLOSURE` |
| `emit receipt` | `EMIT_RECEIPT` |

Every lowered node is chained in v0.1 source effect order. Data arguments still encode the actual dependency graph.
''')
w('08_LOWERING/COMPILATION_CONTRACT.md',r'''
# Compilation contract

For each source file:

1. parse without inventing missing tokens;
2. reject duplicate local output identities;
3. lower each statement to one GIR node;
4. attach a source-map witness;
5. derive exact effects;
6. construct a `GIR-MODULE`;
7. run the Section 09 module checker;
8. only then expose the module to the semantic linker.

A multi-file build then uses Section 09 symbol resolution/linking and Section 08 compilation unchanged.
''')
w('09_SOURCE_MAP_PROVENANCE/SOURCE_MAP.md',r'''
# Source map and provenance

Each GIR node receives a source-map record:

```json
{
  "node": "004_portal_open",
  "file": "FIRST_PORTAL.gen",
  "line": 9,
  "surface": "portal GR g1 with adm as p corridor ..."
}
```

The frontend receipt hashes normalized source, AST, lowered modules, linked GIR, and emitted GVM. This gives BLACKGLASS a deterministic chain from textual projection back to executable relationship graph.
''')
w('10_COMPILER_PIPELINE/PIPELINE.md',r'''
# Compiler pipeline

```text
.gen
 -> lexical normalization
 -> parse
 -> AST validation
 -> lower to GIR-MODULE
 -> Section 09 check_module
 -> Section 09 link_bundle
 -> Section 08 compile_gir
 -> GVM verify
 -> bytecode
 -> VM/backend execution
```

The frontend intentionally reuses the previously established semantic layers rather than duplicating their rules.
''')
w('11_DIAGNOSTICS/DIAGNOSTIC_MODEL.md',r'''
# Diagnostics

Frontend diagnostics are structured as:

```text
CODE file:line: message
```

Primary v0.1 frontend codes:

- `GEN_VERSION`
- `MODULE_HEADER`
- `MODULE_CLOSE`
- `STATEMENT_UNKNOWN`
- `SYNTAX`
- `ATTR_JSON`
- `DUPLICATE_VALUE`
- `EXPORT_UNKNOWN`
- `SOURCE_TYPE`
- `SEMANTIC_CHECK`

Section 09 diagnostics are preserved verbatim after lowering, including bridge, linear ownership, typestate, effect, closure, and capability failures.
''')

# ---------------- implementation ----------------
PKG=ROOT/'12_REFERENCE_IMPLEMENTATION/genesis_frontend'
PKG.mkdir(parents=True,exist_ok=True)
# vendor Section09 implementation, excluding pycache
src=S09/'12_REFERENCE_IMPLEMENTATION/genesis_semantics'
dst=PKG/'vendor/genesis_semantics'
shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))

w('12_REFERENCE_IMPLEMENTATION/README.md',r'''
# Reference frontend

Package: `genesis_frontend`

Self-contained bootstrap usage from this directory:

```bash
python -m genesis_frontend parse ../../16_EXAMPLES/FIRST_PORTAL.gen
python -m genesis_frontend lower ../../16_EXAMPLES/FIRST_PORTAL.gen
python -m genesis_frontend build ../../16_EXAMPLES/FIRST_PORTAL.gen -o first_portal.gvm
python -m genesis_frontend run ../../16_EXAMPLES/FIRST_PORTAL.gen
```

The package vendors Section 09 `genesis_semantics`, which in turn vendors the Section 08 `genesis_vm` reference runtime.
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_frontend/model.py',r'''
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Diagnostic:
    code:str; message:str; file:str='<memory>'; line:int=0; column:int=1
    def __str__(self): return f'{self.code} {self.file}:{self.line}:{self.column}: {self.message}'
    def as_dict(self): return {'code':self.code,'message':self.message,'file':self.file,'line':self.line,'column':self.column}

class FrontendError(Exception):
    def __init__(self, diagnostic):
        self.diagnostic=diagnostic if isinstance(diagnostic,Diagnostic) else Diagnostic('FRONTEND',str(diagnostic))
        super().__init__(str(self.diagnostic))

@dataclass
class ImportDecl:
    module:str; symbol:str; local:str; type:str; line:int
    def as_dict(self): return vars(self)

@dataclass
class ExportDecl:
    local:str; type:str; line:int
    def as_dict(self): return vars(self)

@dataclass
class Statement:
    kind:str; out:str|None; args:list[str]=field(default_factory=list); attrs:dict[str,Any]=field(default_factory=dict)
    declared_type:str|None=None; line:int=0; surface:str=''
    def as_dict(self): return {'kind':self.kind,'out':self.out,'args':self.args,'attrs':self.attrs,'declared_type':self.declared_type,'line':self.line,'surface':self.surface}

@dataclass
class ModuleAST:
    version:str; module:str; imports:list[ImportDecl]; statements:list[Statement]; exports:list[ExportDecl]; file:str='<memory>'
    def as_dict(self): return {'ast':'GENESIS-AST','version':self.version,'module':self.module,'file':self.file,'imports':[x.as_dict() for x in self.imports],'statements':[x.as_dict() for x in self.statements],'exports':[x.as_dict() for x in self.exports]}
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_frontend/util.py',r'''
import json,hashlib,re

def canonical_bytes(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def sha256_obj(obj): return hashlib.sha256(canonical_bytes(obj)).hexdigest()
def sha256_text(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()

def strip_comment(line):
    out=[]; quote=False; esc=False; i=0
    while i<len(line):
        c=line[i]
        if esc: out.append(c); esc=False; i+=1; continue
        if c=='\\' and quote: out.append(c); esc=True; i+=1; continue
        if c=='"': quote=not quote; out.append(c); i+=1; continue
        if not quote and c=='#': break
        if not quote and c=='/' and i+1<len(line) and line[i+1]=='/': break
        out.append(c); i+=1
    return ''.join(out).rstrip()

def split_attrs(line):
    quote=False; esc=False; depth=0
    for i,c in enumerate(line):
        if esc: esc=False; continue
        if c=='\\' and quote: esc=True; continue
        if c=='"': quote=not quote; continue
        if not quote and c=='@' and i+1<len(line) and line[i+1]=='{':
            raw=line[i+1:].strip().rstrip(';').strip()
            return line[:i].rstrip(), json.loads(raw)
    return line.rstrip(';').rstrip(), {}

def coarse_type(t):
    return re.split(r'<',str(t).strip(),1)[0].upper()
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_frontend/parser.py',r'''
import json,shlex,re
from .model import Diagnostic,FrontendError,ImportDecl,ExportDecl,Statement,ModuleAST
from .util import strip_comment,split_attrs

IDENT=re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
QNAME=re.compile(r'^[A-Za-z_][A-Za-z0-9_.]*$')

def _err(code,msg,file,line): raise FrontendError(Diagnostic(code,msg,file,line))
def _id(x,file,line):
    if not IDENT.fullmatch(x): _err('SYNTAX',f'invalid identifier {x!r}',file,line)
    return x

def _tokens(core,file,line):
    try: return shlex.split(core,posix=True)
    except ValueError as e: _err('SYNTAX',str(e),file,line)

def parse_source(text,file='<memory>'):
    raw=text.splitlines(); clean=[]
    for n,line in enumerate(raw,1):
        s=strip_comment(line).strip()
        if s: clean.append((n,s))
    if not clean: _err('GEN_VERSION','empty source',file,1)
    n,s=clean[0]
    if s!='genesis 0.1.0': _err('GEN_VERSION','expected `genesis 0.1.0`',file,n)
    if len(clean)<2: _err('MODULE_HEADER','missing module',file,n)
    mn,ms=clean[1]
    m=re.fullmatch(r'module\s+([A-Za-z_][A-Za-z0-9_.]*)\s*\{',ms)
    if not m: _err('MODULE_HEADER','expected `module <name> {`',file,mn)
    module=m.group(1); imports=[]; exports=[]; statements=[]; produced=set(); closed=False
    for idx,(ln,line) in enumerate(clean[2:],start=2):
        if line=='}':
            if idx!=len(clean)-1: _err('MODULE_CLOSE','content after module close',file,ln)
            closed=True; break
        try: core,attrs=split_attrs(line)
        except json.JSONDecodeError as e: _err('ATTR_JSON',str(e),file,ln)
        t=_tokens(core,file,ln)
        if not t: continue
        if t[0]=='use':
            # use mod::symbol as local : TYPE
            if len(t)<6 or t[2]!='as' or t[4]!=':': _err('SYNTAX','use: expected `use module::symbol as local : TYPE`',file,ln)
            if '::' not in t[1]: _err('SYNTAX','use source must be module::symbol',file,ln)
            src,sym=t[1].split('::',1); local=_id(t[3],file,ln); typ=''.join(t[5:])
            imports.append(ImportDecl(src,sym,local,typ,ln)); continue
        if t[0]=='export':
            if len(t)<4 or t[2]!=':': _err('SYNTAX','export: expected `export name : TYPE`',file,ln)
            exports.append(ExportDecl(_id(t[1],file,ln),''.join(t[3:]),ln)); continue

        st=None
        if t[0]=='en':
            if len(t)<7 or t[2]!=':' or '=' not in t: _err('SYNTAX','en declaration malformed',file,ln)
            out=_id(t[1],file,ln); eq=t.index('='); typ=''.join(t[3:eq]); rhs=t[eq+1:]
            if not rhs:_err('SYNTAX','en declaration missing constructor',file,ln)
            if rhs[0]=='mount' and len(rhs)==2: st=Statement('mount',out,[],{'uri':rhs[1],**attrs},typ,ln,line)
            elif rhs[0]=='alloc' and len(rhs)==4 and rhs[2]=='cells':
                try: cells=int(rhs[3])
                except: _err('SYNTAX','cells must be integer',file,ln)
                st=Statement('alloc',out,[rhs[1]],{'cells':cells,**attrs},typ,ln,line)
            elif rhs[0]=='instantiate' and len(rhs)==5 and rhs[3]=='mmo':
                st=Statement('instantiate',out,[rhs[1],rhs[2]],{'mmo':{'class':'MMO','handle':rhs[4]},**attrs},typ,ln,line)
            elif rhs[0]=='fork' and len(rhs)==2: st=Statement('fork',out,[rhs[1]],attrs,typ,ln,line)
            else:_err('SYNTAX','unknown en constructor',file,ln)
        elif t[0]=='rel' and len(t)>=6 and t[2]=='->' and t[-2]=='as':
            st=Statement('rel',_id(t[-1],file,ln),[t[1]],{'target':t[3],**attrs},None,ln,line)
        elif t[0]=='admit' and len(t)==4 and t[2]=='as': st=Statement('admit',_id(t[3],file,ln),[t[1]],attrs,None,ln,line)
        elif t[0]=='transform' and len(t)==6 and t[2]=='with' and t[4]=='as': st=Statement('transform',_id(t[5],file,ln),[t[1],t[3]],attrs,None,ln,line)
        elif t[0]=='ar' and len(t)==4 and t[2]=='as': st=Statement('inherit',_id(t[3],file,ln),[t[1]],attrs,None,ln,line)
        elif t[0]=='portal':
            # portal GR geo with adm as p corridor "..." [bridge b]
            if len(t)<9 or t[3]!='with' or t[5]!='as' or t[7]!='corridor': _err('SYNTAX','portal statement malformed',file,ln)
            sec=t[1].upper();
            if sec not in ('GENERIC','QFT','GR'): _err('SYNTAX',f'unknown sector {sec}',file,ln)
            a={'sector':sec,'corridor':t[8],**attrs}
            if len(t)>9:
                if len(t)!=11 or t[9]!='bridge': _err('SYNTAX','portal bridge clause malformed',file,ln)
                a['bridge']='%'+_id(t[10],file,ln)
            st=Statement('portal',_id(t[6],file,ln),[t[2],t[4]],a,None,ln,line)
        elif t[0]=='ve' and len(t)==8 and t[2]=='through' and t[4]=='->' and t[6]=='as':
            st=Statement('transport',_id(t[7],file,ln),[t[3],t[1]],{'destination':t[5],**attrs},None,ln,line)
        elif t[0]=='tor' and len(t)==6 and t[2]=='with' and t[4]=='as': st=Statement('portal_close',_id(t[5],file,ln),[t[1],t[3]],attrs,None,ln,line)
        elif t[0]=='road':
            if len(t)==5 and t[1]=='begin' and t[3]=='as': st=Statement('road_begin',_id(t[4],file,ln),[t[2]],attrs,None,ln,line)
            elif len(t)==6 and t[1]=='append' and t[4]=='as': st=Statement('road_append',_id(t[5],file,ln),[t[2],t[3]],attrs,None,ln,line)
            elif len(t)==6 and t[1]=='close' and t[4]=='as': st=Statement('road_close',_id(t[5],file,ln),[t[2],t[3]],attrs,None,ln,line)
            else:_err('SYNTAX','road statement malformed',file,ln)
        elif t[0]=='bridge' and len(t)==7 and t[3]=='->' and t[5]=='as':
            st=Statement('bridge',_id(t[6],file,ln),[t[1]],{'from':t[2].upper(),'to':t[4].upper(),**attrs},None,ln,line)
        elif t[0]=='q':
            sub=t[1] if len(t)>1 else ''
            if sub in ('prepare','superpose','channel','measure') and len(t)==5 and t[3]=='as': st=Statement('q_'+sub,_id(t[4],file,ln),[t[2]],attrs,None,ln,line)
            elif sub=='entangle' and len(t)==6 and t[4]=='as': st=Statement('q_entangle',_id(t[5],file,ln),[t[2],t[3]],attrs,None,ln,line)
            else:_err('SYNTAX','quantum statement malformed',file,ln)
        elif t[0]=='lift' and len(t)==4 and t[2]=='as': st=Statement('lift',_id(t[3],file,ln),[t[1]],attrs,None,ln,line)
        elif t[0]=='seal' and len(t)==4 and t[2]=='as': st=Statement('seal',_id(t[3],file,ln),[t[1]],attrs,None,ln,line)
        elif t[0]=='assert' and len(t)==5 and t[1]=='closure' and t[3]=='as': st=Statement('assert_closure',_id(t[4],file,ln),[t[2]],attrs,None,ln,line)
        elif t[0]=='emit' and len(t)==5 and t[1]=='receipt' and t[2]=='as':
            # Accept canonical four tokens too after shlex weirdness guard below.
            st=Statement('emit_receipt',_id(t[3],file,ln),[],attrs,None,ln,line) if len(t)==4 else None
        elif t[0]=='emit' and len(t)==4 and t[1]=='receipt' and t[2]=='as': st=Statement('emit_receipt',_id(t[3],file,ln),[],attrs,None,ln,line)
        else:_err('STATEMENT_UNKNOWN',f'cannot parse statement: {line}',file,ln)
        if st is None:_err('SYNTAX',f'malformed statement: {line}',file,ln)
        if st.out:
            if st.out in produced or any(i.local==st.out for i in imports): _err('DUPLICATE_VALUE',f'duplicate local identity {st.out}',file,ln)
            produced.add(st.out)
        statements.append(st)
    if not closed:_err('MODULE_CLOSE','missing closing `}`',file,clean[-1][0])
    known=produced|{i.local for i in imports}
    for e in exports:
        if e.local not in known:_err('EXPORT_UNKNOWN',f'export {e.local} has no local value',file,e.line)
    return ModuleAST('0.1.0',module,imports,statements,exports,file)
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_frontend/lower.py',r'''
from .model import Diagnostic,FrontendError
from .util import coarse_type,sha256_obj
from .vendor.genesis_semantics import check_module
from .vendor.genesis_semantics.effects import effects_for_op

OPS={
'mount':'FABRIC_MOUNT','alloc':'FABRIC_ALLOC','instantiate':'GEO_INSTANTIATE','fork':'GEO_FORK','rel':'RELATE','admit':'ADMIT','transform':'TRANSFORM','inherit':'INHERIT','portal':'PORTAL_OPEN','transport':'PORTAL_TRANSPORT','portal_close':'PORTAL_CLOSE','road_begin':'ROAD_BEGIN','road_append':'ROAD_APPEND','road_close':'ROAD_CLOSE','bridge':'BRIDGE_SECTOR','q_prepare':'Q_PREPARE','q_superpose':'Q_SUPERPOSE','q_entangle':'Q_ENTANGLE','q_channel':'Q_CHANNEL','q_measure':'Q_MEASURE','lift':'BRANE_LIFT','seal':'PROVENANCE_SEAL','assert_closure':'ASSERT_CLOSURE','emit_receipt':'EMIT_RECEIPT'
}
TYPES={
'FABRIC_MOUNT':'FABRIC','FABRIC_ALLOC':'REGION','GEO_INSTANTIATE':'GEOMETRIC','GEO_FORK':'GEOMETRIC','RELATE':'RELATION','ADMIT':'ADMISSION','TRANSFORM':'GEOMETRIC','INHERIT':'RECEIPT','PORTAL_OPEN':'PORTAL','PORTAL_TRANSPORT':'GEOMETRIC','PORTAL_CLOSE':'RECEIPT','ROAD_BEGIN':'ROAD','ROAD_APPEND':'ROAD','ROAD_CLOSE':'RECEIPT','BRIDGE_SECTOR':'BRIDGE','Q_PREPARE':'QSTATE','Q_SUPERPOSE':'QSTATE','Q_ENTANGLE':'QSTATE','Q_CHANNEL':'QSTATE','Q_MEASURE':'QRESULT','BRANE_LIFT':'M5','PROVENANCE_SEAL':'RECEIPT','ASSERT_CLOSURE':'BOOL','EMIT_RECEIPT':'RECEIPT'
}

def _v(name): return name if isinstance(name,str) and name.startswith('%') else '%'+name

def lower_module(ast):
    nodes=[]; edges=[]; effects=set(); source_map=[]; previous=None
    for idx,st in enumerate(ast.statements,1):
        op=OPS[st.kind]; nid=f'{idx:03d}_{op.lower()}'
        attrs=dict(st.attrs); args=[_v(x) for x in st.args]
        out=_v(st.out) if st.out else None
        typ=coarse_type(st.declared_type) if st.declared_type else TYPES[op]
        n={'id':nid,'op':op,'type':typ}
        if args:n['args']=args
        if out:n['out']=out
        if attrs:n['attrs']=attrs
        nodes.append(n); effects |= effects_for_op(op)
        if previous is not None: edges.append({'from':previous,'to':nid,'kind':'effect_order'})
        previous=nid
        source_map.append({'node':nid,'file':ast.file,'line':st.line,'surface':st.surface})
    mod={
      'ir':'GIR-MODULE','version':'0.1.0','module':ast.module,
      'imports':[{'from':x.module,'symbol':x.symbol,'local':_v(x.local),'type':x.type} for x in ast.imports],
      'exports':[{'symbol':x.local,'value':_v(x.local),'type':x.type} for x in ast.exports],
      'effects':sorted(effects),
      'gir':{'nodes':nodes,'edges':edges},
      'frontend':{'section':'10','source_file':ast.file,'source_map':source_map,'ast_hash':sha256_obj(ast.as_dict())}
    }
    cr=check_module(mod)
    if not cr.ok:
        msg='; '.join(f'{d.code}:{d.message}' for d in cr.diagnostics)
        raise FrontendError(Diagnostic('SEMANTIC_CHECK',msg,ast.file,0))
    return mod,cr
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_frontend/compiler.py',r'''
from pathlib import Path
from .parser import parse_source
from .lower import lower_module
from .util import sha256_obj,sha256_text
from .vendor.genesis_semantics import link_bundle
from .vendor.genesis_semantics.capabilities import reference_backend_capabilities
from .vendor.genesis_semantics.vendor.genesis_vm import VM,decode,disassemble

class BuildResult:
    def __init__(self,asts,modules,link,receipt): self.asts=asts; self.modules=modules; self.link=link; self.receipt=receipt

def compile_sources(sources, exports=None, name='genesis_program', backend=None):
    # sources: iterable[(filename,text)]
    asts=[]; modules=[]; src_hashes={}
    for file,text in sources:
        ast=parse_source(text,file); mod,_=lower_module(ast); asts.append(ast); modules.append(mod); src_hashes[file]=sha256_text(text)
    if exports is None:
        exports=[f'{m["module"]}::{e["symbol"]}' for m in modules for e in m.get('exports',[])]
    bundle={'link':'GENESIS-LINK','version':'0.1.0','name':name,'modules':modules,'exports':exports}
    lr=link_bundle(bundle,backend or reference_backend_capabilities())
    pre={'kind':'GENESIS_FRONTEND_RECEIPT','version':'0.1.0','name':name,'sources':src_hashes,'ast_hashes':{a.module:sha256_obj(a.as_dict()) for a in asts},'module_hashes':{m['module']:sha256_obj(m) for m in modules},'link_id':lr.receipt['link_id'],'gir_hash':lr.receipt['gir_hash'],'gvm_sha256':lr.receipt['gvm_sha256'],'exports':exports}
    receipt=dict(pre); receipt['frontend_id']='gfront-'+sha256_obj(pre)[:24]
    return BuildResult(asts,modules,lr,receipt)

def compile_files(paths,exports=None,name='genesis_program',backend=None):
    return compile_sources([(str(Path(p)),Path(p).read_text(encoding='utf-8')) for p in paths],exports,name,backend)

def run_build(br): return VM().run(decode(br.link.bytecode))
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_frontend/formatter.py',r'''
from .util import strip_comment

def format_source(text):
    out=[]; indent=0
    for raw in text.splitlines():
        s=strip_comment(raw).strip().rstrip(';').rstrip()
        if not s: continue
        if s=='}': indent=max(0,indent-1)
        out.append('  '*indent+s)
        if s.endswith('{'): indent+=1
    return '\n'.join(out)+'\n'
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_frontend/__init__.py',r'''
from .parser import parse_source
from .lower import lower_module
from .compiler import compile_sources,compile_files,run_build,BuildResult
from .formatter import format_source
from .model import FrontendError,Diagnostic
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_frontend/__main__.py',r'''
import argparse,json,pathlib
from . import parse_source,lower_module,compile_files,run_build,format_source
from .vendor.genesis_semantics.vendor.genesis_vm import disassemble

def main():
    ap=argparse.ArgumentParser(prog='genesis_frontend'); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('parse'); p.add_argument('source')
    l=sp.add_parser('lower'); l.add_argument('source')
    b=sp.add_parser('build'); b.add_argument('sources',nargs='+'); b.add_argument('-o','--out',required=True); b.add_argument('--export',action='append')
    r=sp.add_parser('run'); r.add_argument('sources',nargs='+'); r.add_argument('--export',action='append')
    f=sp.add_parser('fmt'); f.add_argument('source')
    a=ap.parse_args()
    if a.cmd=='parse':
        path=pathlib.Path(a.source); print(json.dumps(parse_source(path.read_text(),str(path)).as_dict(),indent=2,sort_keys=True))
    elif a.cmd=='lower':
        path=pathlib.Path(a.source); mod,_=lower_module(parse_source(path.read_text(),str(path))); print(json.dumps(mod,indent=2,sort_keys=True))
    elif a.cmd=='build':
        br=compile_files(a.sources,a.export); pathlib.Path(a.out).write_bytes(br.link.bytecode); print(json.dumps(br.receipt,indent=2,sort_keys=True))
    elif a.cmd=='run':
        br=compile_files(a.sources,a.export); rr=run_build(br); print(json.dumps({'frontend':br.receipt,'execution':rr.receipt,'exports':{str(k):v.value for k,v in rr.exports.items()}},indent=2,sort_keys=True,default=str))
    else:
        p=pathlib.Path(a.source); p.write_text(format_source(p.read_text()),encoding='utf-8')
if __name__=='__main__': main()
''')

# schemas
j('13_SCHEMAS/genesis_ast.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Genesis AST v0.1','type':'object','required':['ast','version','module','statements'],'properties':{'ast':{'const':'GENESIS-AST'},'version':{'const':'0.1.0'},'module':{'type':'string'},'statements':{'type':'array'},'imports':{'type':'array'},'exports':{'type':'array'}}})
j('13_SCHEMAS/frontend_receipt.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Genesis Frontend Receipt','type':'object','required':['kind','version','frontend_id','link_id','gvm_sha256'],'properties':{'kind':{'const':'GENESIS_FRONTEND_RECEIPT'},'version':{'const':'0.1.0'},'frontend_id':{'type':'string'},'link_id':{'type':'string'},'gvm_sha256':{'type':'string'}}})
j('13_SCHEMAS/source_map.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Genesis Source Map','type':'array','items':{'type':'object','required':['node','file','line','surface']}})

w('14_PSEUDOCODE/LOWER.txt',r'''
parse source -> AST
for statement in source order:
    choose exactly one GIR opcode from lowering table
    lower local identifiers to SSA names
    retain literals as typed attrs
    derive effects from Section 09 opcode/effect table
    add source-map witness
    chain source effect order
construct GIR-MODULE
run Section 09 check_module
reject on any diagnostic
''')
w('14_PSEUDOCODE/BUILD.txt',r'''
for each .gen file:
    parse
    lower
    static-check module
collect modules
construct GENESIS-LINK bundle
Section09.link_bundle(bundle)
Section08.verify(GVM)
emit bytecode + frontend receipt
''')

# examples
FIRST=r'''genesis 0.1.0
module first_portal {
  en fabric : FABRIC = mount "fabric://chirality/reference-v1"
  en region : REGION = alloc fabric cells 4096
  en g0 : GEOMETRIC = instantiate fabric region mmo @hydrogen_reference
  rel g0 -> "environment://trinity" as relation
  admit g0 as adm @{"admitted":true,"bandwidth":1.0,"resolution":1.0}
  transform g0 with adm as g1 @{"kind":"identity-preserving-reference-transform"}
  portal GR g1 with adm as p corridor "corridor://red-violet"
  ve g1 through p -> "trinity://node-B" as g2
  tor p with g2 as pc
  lift g2 as m5 @{"Chi":"preserved","D":"portal-history","P":"receipt-ledger","R":"closed"}
  seal g2 as seal @{"label":"first-portal"}
  assert closure g2 as closed @{"required":true}
  emit receipt as receipt @{"label":"Genesis Bootstrap 0 — The First Portal"}
  export g2 : GEOMETRIC<CLOSED,GR>
  export pc : RECEIPT<PORTAL_CLOSE>
  export m5 : M5
  export receipt : RECEIPT<EXECUTION>
}
'''
ROAD=r'''genesis 0.1.0
module rainbow_road {
  en fabric : FABRIC = mount "fabric://chirality/reference-v1"
  en region : REGION = alloc fabric cells 8192
  en g0 : GEOMETRIC = instantiate fabric region mmo @oxygen_reference
  road begin g0 as road0 @{"name":"RR-OXYGEN-01"}
  admit g0 as a1 @{"admitted":true}
  portal GR g0 with a1 as p1 corridor "Red->Orange"
  ve g0 through p1 -> "Orange" as g1
  tor p1 with g1 as c1
  road append road0 c1 as road1
  admit g1 as a2 @{"admitted":true}
  portal GR g1 with a2 as p2 corridor "Orange->Violet"
  ve g1 through p2 -> "Violet" as g2
  tor p2 with g2 as c2
  road append road1 c2 as road2
  road close road2 g2 as road_receipt
  lift g2 as m5 @{"R":"rainbow-road-history"}
  emit receipt as receipt
  export g2 : GEOMETRIC<CLOSED,GR>
  export road_receipt : RECEIPT<ROAD_CLOSE>
  export m5 : M5
  export receipt : RECEIPT<EXECUTION>
}
'''
MIXED=r'''genesis 0.1.0
module mixed_sector {
  en fabric : FABRIC = mount "fabric://chirality/reference-v1"
  en region : REGION = alloc fabric cells 16384
  en g0 : GEOMETRIC = instantiate fabric region mmo @virus_hsv1_reference
  admit g0 as aq @{"admitted":true}
  portal QFT g0 with aq as pq corridor "QFT-A"
  ve g0 through pq -> "QFT-B" as gq
  tor pq with gq as cq
  bridge gq QFT -> GR as b @{"preserve":["identity","chirality_ancestry","provenance"]}
  admit gq as ag @{"admitted":true,"bridge":"%b"}
  portal GR gq with ag as pg corridor "GR-B" bridge b
  ve gq through pg -> "GR-C" as gg
  tor pg with gg as cg
  lift gg as m5 @{"P":"mixed-sector-ledger"}
  emit receipt as receipt
  export gg : GEOMETRIC<CLOSED,GR>
  export b : BRIDGE<QFT,GR>
  export cg : RECEIPT<PORTAL_CLOSE>
  export m5 : M5
  export receipt : RECEIPT<EXECUTION>
}
'''
QUANT=r'''genesis 0.1.0
module quantum_effect {
  en fabric : FABRIC = mount "fabric://chirality/reference-v1"
  en region : REGION = alloc fabric cells 2048
  en g0 : GEOMETRIC = instantiate fabric region mmo @hydrogen_reference
  q prepare g0 as q0 @{"basis":["0","1"]}
  q superpose q0 as q1 @{"amplitudes":["1/sqrt(2)","1/sqrt(2)"]}
  q channel q1 as q2 @{"channel":"IDENTITY","preserve_coherence":true}
  q measure q2 as qr @{"outcome":0,"reference_seed":"GENESIS-SECTION10"}
  seal qr as seal @{"effect":"measurement"}
  emit receipt as receipt
  export qr : QRESULT<CLASSICAL>
  export seal : RECEIPT<PROVENANCE>
  export receipt : RECEIPT<EXECUTION>
}
'''
MOD_FIX=r'''genesis 0.1.0
module fixture {
  en fabric : FABRIC = mount "fabric://chirality/reference-v1"
  en region : REGION = alloc fabric cells 4096
  en geo : GEOMETRIC = instantiate fabric region mmo @hydrogen_reference
  export geo : GEOMETRIC<CLOSED,UNBOUND>
}
'''
MOD_QFT=r'''genesis 0.1.0
module qft_leg {
  use fixture::geo as source : GEOMETRIC<CLOSED,UNBOUND>
  admit source as a @{"admitted":true}
  portal QFT source with a as p corridor "QFT-A"
  ve source through p -> "QFT-B" as dest
  tor p with dest as receipt
  export dest : GEOMETRIC<CLOSED,QFT>
  export receipt : RECEIPT<PORTAL_CLOSE>
}
'''
MOD_READ=r'''genesis 0.1.0
module readout {
  use qft_leg::dest as source : GEOMETRIC<CLOSED,QFT>
  lift source as m5 @{"P":"section10-frontend"}
  seal m5 as seal @{"stage":"readout"}
  emit receipt as receipt
  export m5 : M5
  export receipt : RECEIPT<EXECUTION>
}
'''
for name,txt in [('FIRST_PORTAL.gen',FIRST),('RAINBOW_ROAD.gen',ROAD),('MIXED_SECTOR.gen',MIXED),('QUANTUM_EFFECT.gen',QUANT)]: w('16_EXAMPLES/'+name,txt)
for name,txt in [('fixture.gen',MOD_FIX),('qft_leg.gen',MOD_QFT),('readout.gen',MOD_READ)]: w('16_EXAMPLES/MODULAR_QFT/'+name,txt)
w('16_EXAMPLES/README.md',r'''
# Reference Genesis source programs

- `FIRST_PORTAL.gen` — Bootstrap 0 end-to-end Portal.
- `RAINBOW_ROAD.gen` — two closed Portal legs composed as a Road.
- `MIXED_SECTOR.gen` — explicit QFT→GR bridge.
- `QUANTUM_EFFECT.gen` — linear QSTATE preparation, superposition, channel, measurement.
- `MODULAR_QFT/` — three separately compiled source modules linked through typed imports/exports.
''')

# tests
w('15_TESTS/test_section10.py',r'''
import unittest,sys,json,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION'))
from genesis_frontend import *
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import decode,verify,VM

EX=ROOT/'16_EXAMPLES'

def src(name): return (EX/name).read_text(encoding='utf-8')

class Section10(unittest.TestCase):
    def test_01_parse_header(self): self.assertEqual(parse_source(src('FIRST_PORTAL.gen'),'x').version,'0.1.0')
    def test_02_parse_module(self): self.assertEqual(parse_source(src('FIRST_PORTAL.gen'),'x').module,'first_portal')
    def test_03_first_statement_en(self): self.assertEqual(parse_source(src('FIRST_PORTAL.gen'),'x').statements[0].kind,'mount')
    def test_04_rel_mnemonic(self): self.assertIn('rel',[x.kind for x in parse_source(src('FIRST_PORTAL.gen'),'x').statements])
    def test_05_ve_mnemonic(self): self.assertIn('transport',[x.kind for x in parse_source(src('FIRST_PORTAL.gen'),'x').statements])
    def test_06_tor_mnemonic(self): self.assertIn('portal_close',[x.kind for x in parse_source(src('FIRST_PORTAL.gen'),'x').statements])
    def test_07_attrs_json(self): self.assertTrue(parse_source(src('FIRST_PORTAL.gen'),'x').statements[4].attrs['admitted'])
    def test_08_lower_ir(self): self.assertEqual(lower_module(parse_source(src('FIRST_PORTAL.gen'),'x'))[0]['ir'],'GIR-MODULE')
    def test_09_lower_mount(self): self.assertEqual(lower_module(parse_source(src('FIRST_PORTAL.gen'),'x'))[0]['gir']['nodes'][0]['op'],'FABRIC_MOUNT')
    def test_10_lower_portal(self): self.assertIn('PORTAL_OPEN',[n['op'] for n in lower_module(parse_source(src('FIRST_PORTAL.gen'),'x'))[0]['gir']['nodes']])
    def test_11_effect_order_edges(self):
        m,_=lower_module(parse_source(src('FIRST_PORTAL.gen'),'x')); self.assertEqual(len(m['gir']['edges']),len(m['gir']['nodes'])-1)
    def test_12_source_map(self): self.assertEqual(len(lower_module(parse_source(src('FIRST_PORTAL.gen'),'x'))[0]['frontend']['source_map']),13)
    def test_13_effect_budget_derived(self):
        m,_=lower_module(parse_source(src('FIRST_PORTAL.gen'),'x')); self.assertIn('TRANSPORT',m['effects']); self.assertIn('CLOSE',m['effects'])
    def test_14_first_build(self): self.assertTrue(compile_sources([('x',src('FIRST_PORTAL.gen'))]).link.check.ok)
    def test_15_first_vm_verify(self): self.assertTrue(verify(decode(compile_sources([('x',src('FIRST_PORTAL.gen'))]).link.bytecode))['ok'])
    def test_16_first_run(self): self.assertTrue(run_build(compile_sources([('x',src('FIRST_PORTAL.gen'))])).halted)
    def test_17_road_build(self): self.assertTrue(compile_sources([('x',src('RAINBOW_ROAD.gen'))]).link.check.ok)
    def test_18_road_run(self): self.assertTrue(run_build(compile_sources([('x',src('RAINBOW_ROAD.gen'))])).halted)
    def test_19_mixed_build(self): self.assertTrue(compile_sources([('x',src('MIXED_SECTOR.gen'))]).link.check.ok)
    def test_20_mixed_run(self): self.assertTrue(run_build(compile_sources([('x',src('MIXED_SECTOR.gen'))])).halted)
    def test_21_quantum_build(self): self.assertTrue(compile_sources([('x',src('QUANTUM_EFFECT.gen'))]).link.check.ok)
    def test_22_quantum_run(self): self.assertTrue(run_build(compile_sources([('x',src('QUANTUM_EFFECT.gen'))])).halted)
    def test_23_modular_parse_use(self): self.assertEqual(parse_source((EX/'MODULAR_QFT/qft_leg.gen').read_text(),'x').imports[0].module,'fixture')
    def test_24_modular_build(self):
        ss=[(str(p),p.read_text()) for p in [EX/'MODULAR_QFT/fixture.gen',EX/'MODULAR_QFT/qft_leg.gen',EX/'MODULAR_QFT/readout.gen']]
        self.assertTrue(compile_sources(ss).link.check.ok)
    def test_25_modular_run(self):
        ss=[(str(p),p.read_text()) for p in [EX/'MODULAR_QFT/fixture.gen',EX/'MODULAR_QFT/qft_leg.gen',EX/'MODULAR_QFT/readout.gen']]
        self.assertTrue(run_build(compile_sources(ss)).halted)
    def test_26_deterministic_bytecode(self):
        a=compile_sources([('x',src('FIRST_PORTAL.gen'))]).link.bytecode; b=compile_sources([('x',src('FIRST_PORTAL.gen'))]).link.bytecode; self.assertEqual(a,b)
    def test_27_deterministic_receipt(self):
        a=compile_sources([('x',src('FIRST_PORTAL.gen'))]).receipt; b=compile_sources([('x',src('FIRST_PORTAL.gen'))]).receipt; self.assertEqual(a,b)
    def test_28_formatter(self): self.assertIn('  en fabric',format_source(src('FIRST_PORTAL.gen')))
    def test_29_comments(self): self.assertEqual(parse_source(src('FIRST_PORTAL.gen').replace('genesis 0.1.0','genesis 0.1.0 # ok'),'x').version,'0.1.0')
    def test_30_bad_version(self):
        with self.assertRaises(FrontendError): parse_source('genesis 9\nmodule x {\n}','x')
    def test_31_missing_close(self):
        with self.assertRaises(FrontendError): parse_source('genesis 0.1.0\nmodule x {\n','x')
    def test_32_unknown_stmt(self):
        with self.assertRaises(FrontendError): parse_source('genesis 0.1.0\nmodule x {\nmagic x\n}\n','x')
    def test_33_duplicate_value(self):
        s='genesis 0.1.0\nmodule x {\nen a : FABRIC = mount "f"\nen a : FABRIC = mount "g"\n}\n'
        with self.assertRaises(FrontendError): parse_source(s,'x')
    def test_34_unknown_export(self):
        with self.assertRaises(FrontendError): parse_source('genesis 0.1.0\nmodule x {\nexport nope : GEOMETRIC\n}\n','x')
    def test_35_unclosed_portal_semantic_error(self):
        s="""genesis 0.1.0\nmodule x {\nen f : FABRIC = mount \"f\"\nen r : REGION = alloc f cells 8\nen g : GEOMETRIC = instantiate f r mmo @h\nadmit g as a @{\"admitted\":true}\nportal GR g with a as p corridor \"c\"\n}\n"""
        with self.assertRaises(FrontendError): lower_module(parse_source(s,'x'))
    def test_36_bridge_required_semantic_error(self):
        s=src('MIXED_SECTOR.gen').replace('  bridge gq QFT -> GR as b @{"preserve":["identity","chirality_ancestry","provenance"]}\n','').replace(' bridge b','').replace(',"bridge":"%b"','')
        with self.assertRaises(FrontendError): lower_module(parse_source(s,'x'))
    def test_37_linear_use_after_move(self):
        s=src('QUANTUM_EFFECT.gen').replace('  q measure q2 as qr','  q measure q1 as qr')
        with self.assertRaises(FrontendError): lower_module(parse_source(s,'x'))
    def test_38_export_refinement(self): self.assertEqual(parse_source(src('MIXED_SECTOR.gen'),'x').exports[0].type,'GEOMETRIC<CLOSED,GR>')
    def test_39_module_effect_exactness(self):
        m,_=lower_module(parse_source(src('QUANTUM_EFFECT.gen'),'x')); self.assertIn('QUANTUM_LINEAR',m['effects']); self.assertIn('MEASURE',m['effects'])
    def test_40_mixed_contains_bridge(self): self.assertIn('BRIDGE_SECTOR',[n['op'] for n in lower_module(parse_source(src('MIXED_SECTOR.gen'),'x'))[0]['gir']['nodes']])
    def test_41_road_contains_append(self): self.assertEqual([n['op'] for n in lower_module(parse_source(src('RAINBOW_ROAD.gen'),'x'))[0]['gir']['nodes']].count('ROAD_APPEND'),2)
    def test_42_frontend_id(self): self.assertTrue(compile_sources([('x',src('FIRST_PORTAL.gen'))]).receipt['frontend_id'].startswith('gfront-'))
    def test_43_link_id_preserved(self): self.assertTrue(compile_sources([('x',src('FIRST_PORTAL.gen'))]).receipt['link_id'].startswith('glnk-'))
    def test_44_gvm_hash_preserved(self): self.assertEqual(compile_sources([('x',src('FIRST_PORTAL.gen'))]).receipt['gvm_sha256'],compile_sources([('x',src('FIRST_PORTAL.gen'))]).link.receipt['gvm_sha256'])
    def test_45_import_lowered_percent(self): self.assertEqual(lower_module(parse_source((EX/'MODULAR_QFT/qft_leg.gen').read_text(),'x'))[0]['imports'][0]['local'],'%source')
    def test_46_source_map_line_positive(self): self.assertGreater(lower_module(parse_source(src('FIRST_PORTAL.gen'),'x'))[0]['frontend']['source_map'][0]['line'],0)

if __name__=='__main__': unittest.main()
''')

w('18_SOURCE_CROSSWALK/SOURCE_CROSSWALK.md',r'''
# Source crosswalk

## Source Genesis corpus

- `Grammar(20260821-153057).pdf`: relationship-first grammar; Topic → Relationship → Identity → Resolution; architectural Boundary → Relationship → Resolution.
- `Rules(20260821-153058).pdf`: Architect Script layers and inherit/propagate/stabilize/redistribute/destabilize/close/normalize operators.
- `Structure(20260821-153057).pdf`: reconstructed-language status and relationship-centric worldview.
- `Rosetta(20260821-153057).pdf`: dot-notation evolution operators and append-only topology-first constraint.
- `Root Family(20260821-153057).pdf`: meaning → root → family → word generative framing.

## Computational lineage

- `COMPUTATIONAL_GENESIS_LANGUAGE_HANDOFF_v0.1.zip`: precursor grammar/EBNF/IR proposal. It is treated as design lineage, not canon over Sections 08–10.
- Section 08 defines executable GIR/GVM.
- Section 09 defines static semantics and semantic linking.
- Section 10 defines the current executable textual projection into those layers.

## New synthesis status

The exact `.gen` grammar, parser, compiler, source-map format, and frontend receipt are Section 10 computational synthesis.
''')
w('18_SOURCE_CROSSWALK/STATUS_DISCIPLINE.md',r'''
# Status discipline

- **Recovered/source-defined:** relationship-first linguistic framing; Source Genesis documents; Architect evolution symbols; existing project semantics in Sections 01–09.
- **Section 10 synthesis:** executable source grammar, lexical rules, AST, parser, source-map format, effect-order projection, compiler CLI, frontend receipt.
- **Not claimed:** historical Architect language compiler syntax; physical quantum execution; physical validation of MK43 interpretations.
''')
w('19_RECOVERY/SECTION_10_STATE.md',r'''
# Section 10 recovery state

**Section:** Genesis Surface Language + Frontend Compiler  
**Version:** 0.1.0  
**Date:** 2026-08-21

Current stack:

```text
Section 10  Genesis source + frontend compiler
Section 09  Static Type/Effect Checker + Semantic Linker
Section 08  Genesis VM / Intermediate Representation
Section 07  Quantum Information State + Effect System
Section 06  QFT/GR Sector Transduction
Section 05  Rainbow Road
Section 04  Portal Transaction Engine
Section 03  Transformation Engine
Section 02  Geometric Instantiation
Section 01  Hardware ABI / Chirality Machine
```

Canonical executable source extension: `.gen`.

Next natural engineering section: frontend package/module system + standard library/runtime intrinsics, or optimizer/code-generation layer, depending project direction.
''')

# Copy build script before test/release later
shutil.copy2('/mnt/data/_build_section10.py',ROOT/'98_BUILD/_build_section10.py')

# Run tests
impl=ROOT/'12_REFERENCE_IMPLEMENTATION'
env=os.environ.copy(); env['PYTHONPATH']=str(impl)
cp=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'15_TESTS'),'-p','test_section10.py','-v'],capture_output=True,text=True,env=env)
w('99_RELEASE/TEST_RESULTS.txt',cp.stdout+'\n'+cp.stderr)
if cp.returncode!=0:
 print(cp.stdout); print(cp.stderr,file=sys.stderr); raise SystemExit(cp.returncode)

# Build reference artifacts
sys.path.insert(0,str(impl))
from genesis_frontend import compile_files,run_build,parse_source,lower_module,format_source
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import disassemble,decode
results={}
for name in ['FIRST_PORTAL','RAINBOW_ROAD','MIXED_SECTOR','QUANTUM_EFFECT']:
 p=ROOT/'16_EXAMPLES'/f'{name}.gen'; br=compile_files([p],name=name.lower()); rr=run_build(br)
 out=ROOT/'17_REFERENCE_BUILDS'/name; out.mkdir(parents=True,exist_ok=True)
 (out/f'{name}.gvm').write_bytes(br.link.bytecode)
 w(f'17_REFERENCE_BUILDS/{name}/{name}.normalized.gen',format_source(p.read_text()))
 j(f'17_REFERENCE_BUILDS/{name}/{name}.ast.json',br.asts[0].as_dict())
 j(f'17_REFERENCE_BUILDS/{name}/{name}.girmod.json',br.modules[0])
 j(f'17_REFERENCE_BUILDS/{name}/{name}.gir.json',br.link.gir)
 w(f'17_REFERENCE_BUILDS/{name}/{name}.disasm.txt',disassemble(decode(br.link.bytecode)))
 j(f'17_REFERENCE_BUILDS/{name}/{name}.frontend_receipt.json',br.receipt)
 j(f'17_REFERENCE_BUILDS/{name}/{name}.link_receipt.json',br.link.receipt)
 j(f'17_REFERENCE_BUILDS/{name}/{name}.proofs.json',br.link.proofs)
 j(f'17_REFERENCE_BUILDS/{name}/{name}.run.json',{'halted':rr.halted,'receipt':rr.receipt,'exports':{str(k):v.value for k,v in rr.exports.items()}})
 results[name]={'frontend_id':br.receipt['frontend_id'],'link_id':br.receipt['link_id'],'gvm_sha256':br.receipt['gvm_sha256'],'halted':rr.halted,'proofs':{x['id']:x['status'] for x in br.link.proofs}}
# modular build
paths=[ROOT/'16_EXAMPLES/MODULAR_QFT/fixture.gen',ROOT/'16_EXAMPLES/MODULAR_QFT/qft_leg.gen',ROOT/'16_EXAMPLES/MODULAR_QFT/readout.gen']
br=compile_files(paths,name='modular_qft'); rr=run_build(br); out=ROOT/'17_REFERENCE_BUILDS/MODULAR_QFT'; out.mkdir(parents=True,exist_ok=True)
(out/'MODULAR_QFT.gvm').write_bytes(br.link.bytecode); j('17_REFERENCE_BUILDS/MODULAR_QFT/MODULAR_QFT.gir.json',br.link.gir); j('17_REFERENCE_BUILDS/MODULAR_QFT/MODULAR_QFT.frontend_receipt.json',br.receipt); j('17_REFERENCE_BUILDS/MODULAR_QFT/MODULAR_QFT.link_receipt.json',br.link.receipt); j('17_REFERENCE_BUILDS/MODULAR_QFT/MODULAR_QFT.proofs.json',br.link.proofs); w('17_REFERENCE_BUILDS/MODULAR_QFT/MODULAR_QFT.disasm.txt',disassemble(decode(br.link.bytecode))); j('17_REFERENCE_BUILDS/MODULAR_QFT/MODULAR_QFT.run.json',{'halted':rr.halted,'receipt':rr.receipt,'exports':{str(k):v.value for k,v in rr.exports.items()}})
results['MODULAR_QFT']={'frontend_id':br.receipt['frontend_id'],'link_id':br.receipt['link_id'],'gvm_sha256':br.receipt['gvm_sha256'],'halted':rr.halted,'proofs':{x['id']:x['status'] for x in br.link.proofs}}
j('99_RELEASE/REFERENCE_BUILD_RESULTS.json',results)

# core manifest/checksums
files=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.pyc')]
checks=[]
for p in sorted(files): checks.append(f'{sha_file(p)}  {p.relative_to(ROOT).as_posix()}')
w('99_RELEASE/CORE_CHECKSUMS.sha256','\n'.join(checks)+'\n')
manifest={'release':ROOT.name,'version':'0.1.0','date':'2026-08-21','title':'Genesis Surface Language + Frontend Compiler','files':len(files)+1,'reference_builds':results,'test_suite':'46/46 PASS','semantic_dependencies':['Section 09 Static Semantics/Linker','Section 08 GIR/GVM','Sections 01-07 runtime/backends'],'status':'BOOTSTRAP FRONTEND / SOFTWARE REFERENCE'}
j('99_RELEASE/CORE_MANIFEST.json',manifest)
print('BUILT',ROOT)
print(cp.stderr.splitlines()[-1] if cp.stderr else '')
print(json.dumps(results,indent=2))
