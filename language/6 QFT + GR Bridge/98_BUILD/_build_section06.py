from pathlib import Path
import os, json, shutil, hashlib, textwrap, subprocess, sys, time, copy

BASE=Path('/mnt/data')
NAME='GENESIS_CHIRALITY_MACHINE_SECTION_06_QFT_GR_TRANSDUCTION_v0.1.0_20260821'
ROOT=BASE/NAME
if ROOT.exists(): shutil.rmtree(ROOT)
ROOT.mkdir()

def w(rel, txt):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(textwrap.dedent(txt).lstrip(),encoding='utf-8'); return p

def wj(rel,obj):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,sort_keys=True),encoding='utf-8'); return p

# Vendor Section 05 implementation, transitively carrying Sections 04-01.
s05=BASE/'GENESIS_CHIRALITY_MACHINE_SECTION_05_RAINBOW_ROAD_v0.1.0_20260821'
shutil.copytree(s05/'12_REFERENCE_IMPLEMENTATION', ROOT/'12_REFERENCE_IMPLEMENTATION'/'vendor_section05', dirs_exist_ok=True)

w('00_START_HERE/FOLDER_NAME.txt', NAME+'\n')
w('00_START_HERE/README.md', r'''
# Genesis Chirality Machine — Section 06
## QFT/GR Representation Bridge + Sector Transduction Engine

Version `0.1.0` — implementation layer.

Section 06 makes the QFT/GR bridge executable **as a typed representation transduction**, without asserting that QFT and GR are identical objects and without fabricating a global inverse map.

The source-backed formal spine is:

```text
Common Chirality Fabric state F
       |                |
       | rho_Q          | rho_G
       v                v
    QFT view          GR view

R_QG = { (q,g) | exists F: q=rho_Q(F), g=rho_G(F) }
```

For Corridor `W` the source bridge defines the transport candidate:

```text
P_W^chi : F_a -> F_b
rho_Q o P_W^chi = U_Q(W) o rho_Q
rho_G o P_W^chi = U_G(W) o rho_G
```

Section 06 operationalizes the **software contracts** needed to represent and audit those relationships. It does **not** claim to finish the source's open physical typing/proof obligations.

### New executable capability

A Rainbow Road may now contain explicit sector boundaries:

```text
Portal<QFT> -> Bridge<QFT,GR> -> Portal<GR>
```

or the reverse. A Portal itself remains single-sector. Sector changes occur only through a Bridge receipt at a specific realized Geometric/address.

### Core laws

1. QFT and GR are distinct readable representations.
2. A Bridge changes the readable sector/view; it does not mutate the underlying Geometric.
3. No inverse `rho_Q^-1` or `rho_G^-1` is assumed.
4. Cross-sector correspondence is established by a common-ancestry witness.
5. The same logical MMO identity and declared invariant residue must survive unless an explicit future transduction contract says otherwise.
6. Mixed-sector Roads preserve every Portal and Bridge receipt in order.
7. Bridge execution never bypasses Corridor/Portal admission for actual transport.
''')

w('00_START_HERE/RECOVERY_ORDER.md', '''
# Recovery Order

1. Genesis Layer Zero.
2. Section 01 — Hardware ABI / Chirality Fabric.
3. Section 02 — Geometric Instantiation.
4. Section 03 — Transformation Engine.
5. Section 04 — Portal Transaction Engine.
6. Section 05 — Rainbow Road Composition.
7. **Section 06 — this package.**

Part A is authoritative for Section-06 implementation semantics. Part B contains reference mixed-sector executions. Parts C-E carry source/implementation lineage and the large MK Ultra information/QFT/GR reference corpus.
''')

w('01_ARCHITECTURE/ARCHITECTURE.md', r'''
# Section-06 Architecture

```text
Geometric / MMO on Chirality Fabric
               |
               +---------------------------+
               |                           |
             rho_Q                       rho_G
               |                           |
               v                           v
       QFT Representation           GR Representation
               |                           |
               +------ R_QG ancestry ------+
                          |
                    Bridge Engine
                          |
              typed transduction receipt
                          |
                 sector/address view
                          |
                    Portal Engine
                          |
                    Rainbow Road
```

## Representation versus realization

The Geometric is the realized information object on the chirality fabric. A QFT or GR representation is a typed readout/view of that same realized state. Section 06 does not allocate a second physical Geometric merely to switch sectors.

A later Portal may re-realize the Geometric at a new fabric region, but that is Section-04 transport and remains a separate event.

## Why the bridge is not an inverse

Projection/readout can be many-to-one. The bridge therefore uses common ancestry:

```text
q ~_QG g  iff  both are declared readouts of the same underlying fabric witness.
```

The engine refuses any request that requires an undeclared inverse reconstruction.
''')

w('01_ARCHITECTURE/DESIGN_INVARIANTS.md', '''
# Section-06 Design Invariants

1. QFT and GR are representation sectors, not aliases.
2. `Bridge<QFT,GR>` and `Bridge<GR,QFT>` are explicit transactions.
3. A Portal remains single-sector; it cannot silently change sector.
4. A Bridge is representation transduction at one realized Geometric/address, not information transportation by itself.
5. The underlying Geometric segment chain remains immutable during a Bridge.
6. The base chirality fabric remains immutable.
7. No global inverse map from QFT to fabric or GR to fabric is assumed.
8. Common ancestry is represented by an explicit `FabricWitness`.
9. The canonical MMO identity, content root, residue root, and selected provenance survive Bridge transduction by default.
10. QFT/GR sector descriptors are software representation contracts, not claims of new physical derivation.
11. A mixed-sector Rainbow Road inserts Bridge actions exactly where sector changes occur.
12. Every Portal action on a mixed Road still passes Section-04 Corridor admission.
13. Mixed-road preflight includes every Portal Corridor and every Bridge compatibility check before execution.
14. Closed Portal and Bridge history is append-only.
15. If a later action fails, the mixed Road resolves `FAILED_PARTIAL` and retains the exact completion frontier.
16. BRANE M^5 re-lift records current sector plus bridge ancestry; BRANE realization Z remains BRANE-owned.
17. Source bridge statements marked open typing remain open typing in this implementation.
''')

w('02_REPRESENTATION_MODEL/SECTOR_REPRESENTATIONS.md', r'''
# Sector Representation Model

A `SectorRepresentation` is a typed readout descriptor over a realized Geometric.

Common fields:

```text
representation_view_id
sector = QFT | GR
source_instance_id
canonical_mmo_id
content_root
residue_root
fabric_witness_id
address
projection_profile
invariants
payload
status
```

## QFT payload

The reference payload can record:

* state class (`PURE_DESCRIPTOR`, `DENSITY_DESCRIPTOR`, `FIELD_HANDOFF_DESCRIPTOR`);
* coherence policy;
* superposition capability declaration;
* entanglement relation references;
* measurement state;
* normalization policy;
* canonical-Q handoff reference.

It is metadata for the software execution model; Section 06 does not synthesize an actual physical wavefunction from arbitrary MMO bytes.

## GR payload

The reference payload can record:

* manifold/geometry representation ID;
* boundary and topology references;
* connection/curvature handoff status;
* metric-readout status;
* orientation/holonomy witness references;
* Time-Shell/continuity-projection lineage.

Again, these fields type the representation boundary. They do not manufacture a metric tensor where the source has not supplied one.
''')

w('02_REPRESENTATION_MODEL/READOUT_CONTRACTS.md', r'''
# Readout Contracts

`rho_Q` and `rho_G` are implemented as **descriptor constructors** over a known Geometric state.

```text
rho_Q(instance,address) -> QFT SectorRepresentation
rho_G(instance,address) -> GR  SectorRepresentation
```

The descriptors bind to the same immutable `FabricWitness` when they are readouts of the same content/residue/identity state.

This is deliberately weaker than claiming a completed physical representation functor. It is strong enough for compiler/runtime typing, provenance, sector admission, and bridge composition.
''')

w('03_COMMON_ANCESTRY/FABRIC_WITNESS.md', r'''
# Common Fabric Witness

The Section-06 software ancestry witness is a deterministic hash over:

```text
canonical MMO identity
Geometric instance identity
fabric tag
fabric region
full-cell content root
selected invariant-residue root
source representation identity
```

For cross-sector correspondence, QFT and GR views need not have the same `representation_view_id`; they must bind to the same `fabric_witness_id` (or a future explicitly declared admissible-equivalence witness).

The witness proves only **software lineage and readout ancestry**. It is not itself a proof of physical QFT/GR unification.
''')

w('03_COMMON_ANCESTRY/R_QG_RELATION.md', r'''
# QFT/GR Common-Ancestry Relation

Source formalism:

```text
R_QG = { (q,g) | exists F: q = rho_Q(F), g = rho_G(F) }
```

Runtime representation:

```text
R_QG(q,g) is admitted when:
  q.sector == QFT
  g.sector == GR
  q.fabric_witness_id == g.fabric_witness_id
  canonical MMO identity agrees
  required invariant roots agree
  provenance policy passes
```

The relation is symmetric as a correspondence relation in this software layer. The actual transformation maps used to create/read each sector remain directionally typed.
''')

w('04_TRANSDUCTION/BRIDGE_OBJECT.md', r'''
# Bridge Object

A Bridge is a typed sector-transduction transaction:

```text
Bridge<S,T>(Geometric@Address)
```

where `(S,T)` is one of:

```text
(QFT,GR)
(GR,QFT)
```

Bridge execution:

1. characterize the immutable source Geometric;
2. construct source-sector representation `rho_S`;
3. construct target-sector representation `rho_T` from the same underlying witness;
4. validate `R_QG` common ancestry;
5. audit invariant roots and preservation contract;
6. emit immutable Bridge receipt;
7. update the logical sector/address view for subsequent Portal actions;
8. add bridge history/provenance metadata to the runtime instance envelope without rewriting its segment chain.

The Bridge does not consume Rainbow Bus capacity because it does not traverse a Corridor. Future hardware-specific transduction resources may add a separate resource class.
''')

w('04_TRANSDUCTION/NO_FORCED_INVERSE.md', r'''
# No Forced Inverse Rule

Forbidden default:

```text
GR = rho_G o rho_Q^-1(QFT)
QFT = rho_Q o rho_G^-1(GR)
```

because the source explicitly does not assume inverse maps.

Allowed execution pattern:

```text
Geometric F
  -> rho_Q(F) = q
  -> common ancestry witness F
  -> rho_G(F) = g
```

The runtime therefore changes **readout sector** by returning to the common realized object, not by pretending that one downstream representation uniquely reconstructs the other.
''')

w('05_MIXED_SECTOR_ROAD/MIXED_ROAD.md', r'''
# Mixed-Sector Rainbow Road

Section 05 intentionally required one sector for an entire Road. Section 06 lifts that restriction only by making every sector boundary explicit.

Example:

```text
ALPHA/QFT
  --Portal<QFT>--> GREEN/QFT
  --Bridge<QFT,GR>--> GREEN/GR
  --Portal<GR>--> OMEGA/GR
```

The mixed Road is an ordered action list:

```text
PORTAL
BRIDGE
PORTAL
...
```

A sector change with no domain change is a Bridge-only action. A waypoint that changes both domain and sector expands into `BRIDGE` then `PORTAL` in the target sector.

The end-to-end Road receipt contains Portal receipts, Bridge receipts, a combined action trajectory, Corridor edge trajectory, sector trajectory, and common-ancestry witnesses.
''')

w('05_MIXED_SECTOR_ROAD/PREFLIGHT.md', r'''
# Mixed-Road Preflight

Given source address `A/S0` and ordered target addresses:

```text
for target in waypoints:
    if target.sector != current.sector:
        validate Bridge(current.sector -> target.sector)
        append BRIDGE at current.domain
        current.sector = target.sector

    if target.domain != current.domain or target.boundary/logical address differs:
        select Corridor in current.sector
        append PORTAL(current -> target)
        collect capacity hold
        current = target
```

All Bridge checks and Corridor selections complete before the Road acquires its Rainbow Bus hold.
''')

w('06_QFT_SEMANTICS/QFT_SECTOR.md', r'''
# QFT Sector Contract

Section 06 imports quantum-programming concepts only as typed capabilities where needed.

The QFT representation may declare:

```text
coherence: preserved | resolved | unspecified
superposition: supported | absent | unspecified
entanglement_refs: [...]
state_kind: pure_descriptor | density_descriptor | field_handoff_descriptor
measurement: unmeasured | measured | unspecified
channel_class: unitary | isometric | CPTP | projective | classicalized | unspecified
```

These declarations allow later Genesis type/effect checking. They do not imply that every MMO is physically in a coherent superposition or entangled state.

A later dedicated quantum-information section may execute richer state/channel semantics. Section 06 only establishes the sector boundary required by the QFT/GR bridge.
''')

w('07_GR_SEMANTICS/GR_SECTOR.md', r'''
# GR Sector Contract

The GR representation may declare readable geometric roles:

```text
manifold_class
boundary_class
topology_witness
orientation_history
connection_status
curvature_status
metric_readout_status
holonomy_witnesses
```

The presence of the fields is not a claim that every field has already been physically derived. The descriptor records whether data are `PRESENT`, `REFERENCE_ONLY`, `OPEN_TYPING`, or `UNRESOLVED`.
''')

w('08_BRIDGE_RECEIPTS/RECEIPT_CONTRACT.md', r'''
# Bridge Closure Receipt

A successful Bridge receipt contains:

```text
bridge_id
source_sector
target_sector
source_instance_id
canonical_mmo_id
address
source_representation_view_id
target_representation_view_id
fabric_witness_id
source_content_root
target_content_root
source_residue_root
target_residue_root
preservation contract
R_QG witness
source segment hashes
base fabric hash
physics_status
lifecycle
```

`physics_status` is explicitly `SOFTWARE_REFERENCE_TRANSDUCTION` in v0.1.0.
''')

w('09_BRANE_LIFT/BRIDGE_BRANE_ADAPTER.md', r'''
# BRANE M^5 Bridge Adapter

After a Bridge, the same Geometric can be re-lifted into the BRANE organizational contract:

```text
I  identity: canonical MMO + current realized instance
D  dependency: bridge ID, source/target sector, representation views
Chi chirality: common fabric witness + bridge ancestry relation
R  recursion: bridge depth / ordered action history
P  provenance: Bridge receipt and source representation lineage
```

No sixth scientific axis is added. BRANE retains ownership of realization coordinate `Z`.
''')

w('10_REGISTRY/BRIDGE_REGISTRY.md', r'''
# Bridge Registry

The registry stores:

* supported sector pairs;
* representation profiles;
* bridge policies;
* common-ancestry relation receipts;
* named mixed-Road templates.

Current built-in sector pairs:

```text
QFT -> GR
GR  -> QFT
```

No implicit `GENERIC -> QFT/GR` bridge is provided in Section 06.
''')

w('11_VM_EXTENSION/GCM_SECTOR_EXTENSION.md', r'''
# Genesis Chirality Machine — Sector Extension

Provisional machine-level semantic operations:

```text
READ_QFT_VIEW instance,address -> rep
READ_GR_VIEW  instance,address -> rep
BRIDGE_QG     qft_view -> gr_view  [via common fabric witness]
BRIDGE_GQ     gr_view  -> qft_view [via common fabric witness]
ASSERT_ANCESTRY rep_a,rep_b
EMIT_BRIDGE_RECEIPT
```

These are Layer-Zero/VM semantic operations. They are not proposed CPU opcodes and do not replace the Section-01 Hardware ABI.
''')

w('14_PSEUDOCODE/BRIDGE_EXECUTE.txt', r'''
BRIDGE_EXECUTE(req):
    assert req.source_sector != req.target_sector
    assert pair(req.source_sector,req.target_sector) in {(QFT,GR),(GR,QFT)}
    hash source segments and base fabric
    characterize source content/residue
    source_rep = rho_source(source)
    target_rep = rho_target(source)
    witness = common_ancestry(source_rep,target_rep)
    assert witness admitted
    assert preservation roots agree
    assert source segments unchanged
    assert base fabric unchanged
    receipt = CLOSE_BRIDGE(...)
    return same realized Geometric + new logical sector view + receipt
''')

w('14_PSEUDOCODE/MIXED_ROAD_EXECUTE.txt', r'''
MIXED_ROAD_EXECUTE(req):
    plan = PREFLIGHT(req)
    acquire Rainbow Bus holds for every planned Portal Corridor
    current = req.source
    current_address = req.source_address
    for action in plan.actions:
        if action.kind == BRIDGE:
            b = BRIDGE_EXECUTE(current,current_address,action.target_sector)
            inherit bridge receipt into current envelope
            current_address.sector = action.target_sector
        else if action.kind == PORTAL:
            p = PORTAL_EXECUTE(current,current_address,action.target_address)
            current = p.destination
            current_address = action.target_address
        append immutable action receipt
    audit end-to-end identity, content, residue, source immutability, fabric immutability
    emit mixed Road receipt
''')

w('15_FAILURES/FAILURE_TAXONOMY.md', '''
# Section-06 Failure Taxonomy

* `UNSUPPORTED_SECTOR_PAIR` — no explicit Bridge contract exists.
* `SECTOR_IDENTITY_COLLAPSE` — implementation attempted to equate QFT and GR representations.
* `INVERSE_REQUIRED` — operation requires an undeclared inverse map.
* `COMMON_ANCESTRY_MISMATCH` — sector views do not bind to one fabric witness.
* `BRIDGE_CONTENT_DRIFT` — content root changed during readout transduction.
* `BRIDGE_RESIDUE_DRIFT` — invariant residue changed.
* `BRIDGE_PROVENANCE_BREAK` — required identity/provenance lineage is missing.
* `BRIDGE_SOURCE_MUTATED` — source segment chain changed.
* `BRIDGE_FABRIC_MUTATED` — base fabric changed.
* `MIXED_ROAD_PREFLIGHT_FAILED` — at least one Bridge/Corridor action cannot be admitted before execution.
* `MIXED_ROAD_FAILED_PARTIAL` — prior Portal/Bridge actions closed but a later action failed.
* `PORTAL_SECTOR_MISMATCH` — a Portal attempted to cross sector without Bridge.
''')

# Reference implementation package
PKG=ROOT/'12_REFERENCE_IMPLEMENTATION'/'genesis_sector_bridge'; PKG.mkdir(parents=True)
w('12_REFERENCE_IMPLEMENTATION/README.md', '''
# Section-06 Python Reference Implementation

Package: `genesis_sector_bridge`.

This is a deterministic software execution model for sector typing, common-ancestry correspondence, explicit QFT/GR transduction, and mixed-sector Rainbow Road execution. It is an implementation reference, not a claim that the source's open physical QFT/GR bridge proofs are now mathematically complete.
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/util.py', '''
import json,hashlib,time
from pathlib import Path

def stable_json(x): return json.dumps(x,sort_keys=True,separators=(',',':'),default=str).encode()
def digest_obj(x): return hashlib.sha256(stable_json(x)).hexdigest()
def file_sha256(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def now_ns(): return time.time_ns()
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/errors.py', '''
class SectorBridgeError(Exception): pass
class UnsupportedSectorPair(SectorBridgeError): pass
class CommonAncestryMismatch(SectorBridgeError): pass
class BridgeContentDrift(SectorBridgeError): pass
class BridgeResidueDrift(SectorBridgeError): pass
class BridgeSourceMutated(SectorBridgeError): pass
class BridgeFabricMutated(SectorBridgeError): pass
class InverseRequired(SectorBridgeError): pass
class MixedRoadError(SectorBridgeError):
    def __init__(self,msg,receipt=None): super().__init__(msg); self.receipt=receipt
class MixedRoadPreflightError(MixedRoadError): pass
class MixedRoadExecutionError(MixedRoadError): pass
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/model.py', '''
from dataclasses import dataclass,field
from enum import Enum
from typing import Optional

class Sector(str,Enum): QFT='QFT'; GR='GR'
class BridgeState(str,Enum): DECLARED='DECLARED'; CHARACTERIZED='CHARACTERIZED'; SOURCE_VIEW='SOURCE_VIEW'; TARGET_VIEW='TARGET_VIEW'; ANCESTRY_VERIFIED='ANCESTRY_VERIFIED'; CLOSED='CLOSED'; INHERITED='INHERITED'; FAILED='FAILED'
class MixedRoadState(str,Enum): DECLARED='DECLARED'; PREFLIGHTED='PREFLIGHTED'; BUS_RESERVED='BUS_RESERVED'; RUNNING='RUNNING'; ACTION_CLOSED='ACTION_CLOSED'; END_TO_END_AUDIT='END_TO_END_AUDIT'; CLOSED='CLOSED'; INHERITED='INHERITED'; FAILED='FAILED'; FAILED_PARTIAL='FAILED_PARTIAL'

@dataclass(frozen=True)
class BridgePreservation:
    preserve_canonical_mmo:bool=True
    preserve_representation_id:bool=True
    preserve_content_root:bool=True
    preserve_residue_root:bool=True
    preserve_source_segments:bool=True

@dataclass
class SectorRepresentation:
    representation_view_id:str
    sector:str
    source_instance_id:str
    canonical_mmo_id:str
    source_representation_id:str
    content_root:str
    residue_root:str
    fabric_witness_id:str
    address:dict
    projection_profile:str
    invariants:dict
    payload:dict
    physics_status:str='SOFTWARE_REFERENCE_READOUT'

@dataclass
class BridgeRequest:
    source_instance:dict
    source_segment_chain:list
    address:object
    source_sector:str
    target_sector:str
    preservation:BridgePreservation=field(default_factory=BridgePreservation)
    projection_profile_qft:str='QFT_REFERENCE_V0_1'
    projection_profile_gr:str='GR_REFERENCE_V0_1'
    metadata:dict=field(default_factory=dict)

@dataclass
class BridgePlan:
    bridge_id:str
    source_sector:str
    target_sector:str
    source_instance_id:str
    address:dict
    source_view:dict
    target_view:dict
    fabric_witness_id:str
    common_ancestry_relation_id:str
    preservation:dict
    lifecycle:list

@dataclass
class BridgeResult:
    instance:dict
    address:object
    source_view:dict
    target_view:dict
    plan:dict
    receipt:dict

@dataclass
class MixedSectorRoadRequest:
    source_instance:dict
    source_segment_chain:list
    source_address:object
    waypoints:list
    preservation:object
    bridge_preservation:BridgePreservation=field(default_factory=BridgePreservation)
    resolution_required:float=0.0
    bandwidth_required:float=0.0
    capacity_units_required:int=1
    chirality_class:str='ANY'
    residue_class:str='ANY'
    route_policy:str='LOWEST_COST'
    require_end_to_end_content_identity:bool=True
    road_name:Optional[str]=None
    metadata:dict=field(default_factory=dict)

@dataclass
class MixedActionPlan:
    index:int
    kind:str
    source_address:dict
    target_address:dict
    detail:dict

@dataclass
class MixedRoadPlan:
    road_id:str
    road_name:Optional[str]
    source_instance_id:str
    source_content_root:str
    source_residue_root:str
    source_address:dict
    waypoints:list
    actions:list
    hold_requirements:dict
    sector_trajectory:list
    rainbow_trajectory:list
    lifecycle:list

@dataclass
class MixedRoadResult:
    final_instance:dict
    final_address:object
    plan:dict
    receipt:dict
    action_results:list
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/ledger.py', '''
from pathlib import Path
import json,hashlib
from .util import stable_json,now_ns
class BridgeLedger:
    def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True); self.prev='0'*64
    def append(self,event):
        body={'prev_hash':self.prev,'event':event,'timestamp_ns':now_ns()}; h=hashlib.sha256(stable_json(body)).hexdigest(); body['entry_hash']=h; self.prev=h
        with self.path.open('a',encoding='utf-8') as f:f.write(json.dumps(body,sort_keys=True,separators=(',',':'))+'\\n')
        return body
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/representation.py', '''
from dataclasses import asdict
from genesis_portal_engine.model import PreservationContract
from genesis_portal_engine.residue import residue_root,characterize
from genesis_transform_engine.view import TransformView
from .model import SectorRepresentation
from .util import digest_obj

class RepresentationEngine:
    def __init__(self,fabric): self.fabric=fabric
    def characterize(self,instance,chain,fields=None):
        fields=fields or ['__FULL_CELL__']
        cached=(instance.get('brane_m5',{}).get('Chi',{}).get('post_state_root') or instance.get('brane_m5',{}).get('Chi',{}).get('content_root') or instance.get('brane_m5',{}).get('P',{}).get('transformation_receipt',{}).get('post_state_root'))
        if cached and fields==['__FULL_CELL__']:
            return {'content_root':cached,'cache':'BRANE_POST_STATE_ROOT'},cached
        v=TransformView(self.fabric,chain)
        try:
            ch=characterize(v,instance); rr=residue_root(v,instance['region']['start'],instance['region']['count'],fields)
        finally:v.close()
        return ch,rr
    def fabric_witness(self,instance,content_root,residue_root):
        return digest_obj({'canonical_mmo_id':instance.get('canonical_mmo_id'),'instance_id':instance.get('instance_id'),'source_representation_id':instance.get('representation_id'),'fabric_tag':instance.get('fabric_tag'),'region':instance.get('region'),'content_root':content_root,'residue_root':residue_root})
    def read(self,instance,chain,address,sector,profile='REFERENCE',residue_fields=None):
        ch,rr=self.characterize(instance,chain,residue_fields); fw=self.fabric_witness(instance,ch['content_root'],rr)
        common={'source_instance_id':instance['instance_id'],'canonical_mmo_id':instance.get('canonical_mmo_id'),'source_representation_id':instance.get('representation_id'),'content_root':ch['content_root'],'residue_root':rr,'fabric_witness_id':fw,'address':asdict(address),'projection_profile':profile,'invariants':{'canonical_mmo_id':instance.get('canonical_mmo_id'),'content_root':ch['content_root'],'residue_root':rr}}
        if sector=='QFT':
            payload={'state_kind':'FIELD_HANDOFF_DESCRIPTOR','coherence':'UNSPECIFIED','superposition':'UNSPECIFIED','entanglement_refs':[],'measurement':'UNSPECIFIED','channel_class':'UNSPECIFIED','canonical_q_handoff':'REFERENCE_ONLY'}
        elif sector=='GR':
            payload={'manifold_class':instance.get('mapping_profile','GEOMETRIC'),'boundary_class':'REFERENCE_ONLY','topology_witness':digest_obj({'content_root':ch['content_root'],'region':instance.get('region')}),'orientation_history':'REFERENCE_ONLY','connection_status':'OPEN_TYPING','curvature_status':'OPEN_TYPING','metric_readout_status':'REFERENCE_ONLY','holonomy_witnesses':[]}
        else: raise ValueError('unsupported sector '+str(sector))
        rid=digest_obj({'fabric_witness_id':fw,'sector':sector,'profile':profile,'address':asdict(address)})
        return SectorRepresentation(rid,sector,payload=payload,physics_status='SOFTWARE_REFERENCE_READOUT',**common)
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/ancestry.py', '''
from .util import digest_obj
from .errors import CommonAncestryMismatch

def common_ancestry(q,g):
    if {q.sector,g.sector}!={'QFT','GR'}: raise CommonAncestryMismatch('R_QG requires QFT and GR views')
    if q.fabric_witness_id!=g.fabric_witness_id: raise CommonAncestryMismatch('fabric witness mismatch')
    if q.canonical_mmo_id!=g.canonical_mmo_id: raise CommonAncestryMismatch('MMO identity mismatch')
    if q.content_root!=g.content_root: raise CommonAncestryMismatch('content root mismatch')
    if q.residue_root!=g.residue_root: raise CommonAncestryMismatch('residue root mismatch')
    relation_id=digest_obj({'relation':'R_QG','q':q.representation_view_id,'g':g.representation_view_id,'fabric_witness_id':q.fabric_witness_id})
    return {'kind':'R_QG_COMMON_ANCESTRY','relation_id':relation_id,'admitted':True,'fabric_witness_id':q.fabric_witness_id,'qft_view_id':q.representation_view_id if q.sector=='QFT' else g.representation_view_id,'gr_view_id':g.representation_view_id if g.sector=='GR' else q.representation_view_id,'canonical_mmo_id':q.canonical_mmo_id,'content_root':q.content_root,'residue_root':q.residue_root}
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/audit.py', '''
def audit_bridge_receipt(r):
    f=[]
    if r.get('status')!='CLOSED': f.append('status')
    if r.get('source_sector')==r.get('target_sector'): f.append('sector_change')
    if {r.get('source_sector'),r.get('target_sector')}!={'QFT','GR'}: f.append('sector_pair')
    if r.get('source_content_root')!=r.get('target_content_root'): f.append('content_root')
    if r.get('source_residue_root')!=r.get('target_residue_root'): f.append('residue_root')
    if not r.get('common_ancestry',{}).get('admitted'): f.append('common_ancestry')
    if r.get('fabric_witness_id')!=r.get('common_ancestry',{}).get('fabric_witness_id'): f.append('fabric_witness')
    if r.get('physics_status')!='SOFTWARE_REFERENCE_TRANSDUCTION': f.append('physics_status')
    return {'pass':not f,'findings':f}

def audit_mixed_road_receipt(r):
    f=[]
    if r.get('status')!='CLOSED':f.append('status')
    if r.get('source_content_root')!=r.get('final_content_root'):f.append('content_root')
    if not r.get('actions'):f.append('actions')
    if len(r.get('action_receipts',[]))!=len(r.get('actions',[])):f.append('action_count')
    for x in r.get('bridge_receipts',[]):
        if not audit_bridge_receipt(x)['pass']: f.append('bridge_receipt')
    return {'pass':not f,'findings':f}
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/brane.py', '''
import copy
class BridgeBraneAdapter:
    def adapt(self,instance,receipt):
        bm=copy.deepcopy(instance.get('brane_m5',{}))
        bm.setdefault('I',{})['instance_id']=instance.get('instance_id'); bm['I']['canonical_mmo_id']=instance.get('canonical_mmo_id')
        bm.setdefault('D',{})['bridge_id']=receipt['bridge_id']; bm['D']['source_sector']=receipt['source_sector']; bm['D']['target_sector']=receipt['target_sector']; bm['D']['representation_views']=[receipt['source_representation_view_id'],receipt['target_representation_view_id']]
        bm.setdefault('Chi',{})['fabric_witness_id']=receipt['fabric_witness_id']; bm['Chi']['R_QG_relation_id']=receipt['common_ancestry']['relation_id']; bm['Chi']['current_sector']=receipt['target_sector']
        bm.setdefault('R',{})['bridge_depth']=int(bm.get('R',{}).get('bridge_depth',0))+1; bm['R']['last_bridge_closed']=True
        bm.setdefault('P',{})['bridge_receipt']=receipt
        return bm
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/bridge.py', '''
from dataclasses import asdict
import copy
from genesis_portal_engine.model import PortalAddress
from .model import BridgePlan,BridgeResult,BridgeState
from .representation import RepresentationEngine
from .ancestry import common_ancestry
from .audit import audit_bridge_receipt
from .brane import BridgeBraneAdapter
from .ledger import BridgeLedger
from .errors import *
from .util import digest_obj,file_sha256,now_ns

class SectorBridgeEngine:
    SUPPORTED={('QFT','GR'),('GR','QFT')}
    def __init__(self,fabric,output_dir,ledger_path=None):
        from pathlib import Path
        self.fabric=fabric; self.output_dir=Path(output_dir); self.output_dir.mkdir(parents=True,exist_ok=True); self.ledger=BridgeLedger(ledger_path or self.output_dir/'BRIDGE_LEDGER.jsonl'); self.reps=RepresentationEngine(fabric)
    def _validate(self,req):
        if req.source_sector==req.target_sector: raise UnsupportedSectorPair('bridge requires sector change')
        if (req.source_sector,req.target_sector) not in self.SUPPORTED: raise UnsupportedSectorPair(str((req.source_sector,req.target_sector)))
        if req.address.sector!=req.source_sector: raise UnsupportedSectorPair('source address sector mismatch')
    def plan(self,req):
        self._validate(req); lifecycle=[BridgeState.DECLARED.value,BridgeState.CHARACTERIZED.value]
        prof_s=req.projection_profile_qft if req.source_sector=='QFT' else req.projection_profile_gr
        prof_t=req.projection_profile_qft if req.target_sector=='QFT' else req.projection_profile_gr
        s=self.reps.read(req.source_instance,req.source_segment_chain,req.address,req.source_sector,prof_s)
        lifecycle.append(BridgeState.SOURCE_VIEW.value)
        tgt_addr=PortalAddress(req.address.domain_id,req.address.boundary_id,req.address.logical_location,req.target_sector,req.address.recursive_order,req.address.fabric_tag)
        t=self.reps.read(req.source_instance,req.source_segment_chain,tgt_addr,req.target_sector,prof_t)
        lifecycle.append(BridgeState.TARGET_VIEW.value)
        ca=common_ancestry(s,t); lifecycle.append(BridgeState.ANCESTRY_VERIFIED.value)
        bridge_id=digest_obj({'source_view':s.representation_view_id,'target_view':t.representation_view_id,'relation':ca['relation_id'],'preservation':asdict(req.preservation),'metadata':req.metadata})
        return BridgePlan(bridge_id,req.source_sector,req.target_sector,req.source_instance['instance_id'],asdict(req.address),asdict(s),asdict(t),s.fabric_witness_id,ca['relation_id'],asdict(req.preservation),lifecycle)
    def execute(self,req):
        source_hashes={str(p):file_sha256(p) for p in req.source_segment_chain}; fabric_hash=file_sha256(self.fabric.path)
        try:
            plan=self.plan(req); s=type('R',(),plan.source_view); t=type('R',(),plan.target_view)
            # reconstruct relation using dicts to avoid type assumptions
            ca={'kind':'R_QG_COMMON_ANCESTRY','relation_id':plan.common_ancestry_relation_id,'admitted':True,'fabric_witness_id':plan.fabric_witness_id,'qft_view_id':plan.source_view['representation_view_id'] if req.source_sector=='QFT' else plan.target_view['representation_view_id'],'gr_view_id':plan.target_view['representation_view_id'] if req.target_sector=='GR' else plan.source_view['representation_view_id'],'canonical_mmo_id':req.source_instance.get('canonical_mmo_id'),'content_root':plan.source_view['content_root'],'residue_root':plan.source_view['residue_root']}
            if req.preservation.preserve_content_root and plan.source_view['content_root']!=plan.target_view['content_root']: raise BridgeContentDrift('content')
            if req.preservation.preserve_residue_root and plan.source_view['residue_root']!=plan.target_view['residue_root']: raise BridgeResidueDrift('residue')
            if {str(p):file_sha256(p) for p in req.source_segment_chain}!=source_hashes: raise BridgeSourceMutated('segments')
            if file_sha256(self.fabric.path)!=fabric_hash: raise BridgeFabricMutated('fabric')
            plan.lifecycle.append(BridgeState.CLOSED.value)
            receipt={'kind':'SECTOR_BRIDGE_CLOSURE_RECEIPT','status':'CLOSED','bridge_id':plan.bridge_id,'source_sector':req.source_sector,'target_sector':req.target_sector,'source_instance_id':req.source_instance['instance_id'],'canonical_mmo_id':req.source_instance.get('canonical_mmo_id'),'source_representation_id':req.source_instance.get('representation_id'),'address':plan.address,'source_representation_view_id':plan.source_view['representation_view_id'],'target_representation_view_id':plan.target_view['representation_view_id'],'fabric_witness_id':plan.fabric_witness_id,'common_ancestry':ca,'source_content_root':plan.source_view['content_root'],'target_content_root':plan.target_view['content_root'],'source_residue_root':plan.source_view['residue_root'],'target_residue_root':plan.target_view['residue_root'],'preservation':plan.preservation,'source_segment_hashes':source_hashes,'base_fabric_sha256':fabric_hash,'physics_status':'SOFTWARE_REFERENCE_TRANSDUCTION','lifecycle':list(plan.lifecycle),'timestamp_ns':now_ns()}
            audit=audit_bridge_receipt(receipt); receipt['audit']=audit
            if not audit['pass']: raise SectorBridgeError('bridge audit '+str(audit['findings']))
            out=copy.deepcopy(req.source_instance); out['history']=list(out.get('history',[]))+[{'event':'SECTOR_BRIDGE_CLOSED','bridge_id':plan.bridge_id,'source_sector':req.source_sector,'target_sector':req.target_sector,'timestamp_ns':now_ns()}]; out['provenance']=list(out.get('provenance',[]))+[{'sector_bridge_receipt':receipt}]; out['current_sector']=req.target_sector; out['brane_m5']=BridgeBraneAdapter().adapt(out,receipt)
            plan.lifecycle.append(BridgeState.INHERITED.value); receipt['lifecycle']=list(plan.lifecycle); self.ledger.append(receipt)
            target_address=PortalAddress(req.address.domain_id,req.address.boundary_id,req.address.logical_location,req.target_sector,req.address.recursive_order,req.address.fabric_tag)
            import json
            (self.output_dir/(plan.bridge_id+'.bridge.json')).write_text(json.dumps({'plan':asdict(plan),'receipt':receipt,'instance':out},indent=2,sort_keys=True),encoding='utf-8')
            return BridgeResult(out,target_address,plan.source_view,plan.target_view,asdict(plan),receipt)
        except Exception as exc:
            fail={'kind':'SECTOR_BRIDGE_FAILURE_RECEIPT','status':'FAILED','source_instance_id':req.source_instance.get('instance_id'),'source_sector':req.source_sector,'target_sector':req.target_sector,'error_type':type(exc).__name__,'error':str(exc),'timestamp_ns':now_ns()}; self.ledger.append(fail); raise
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/mixedroad.py', '''
from dataclasses import asdict
import copy
from genesis_portal_engine.model import PortalRequest,PortalAddress
from .model import MixedActionPlan,MixedRoadPlan,MixedRoadResult,MixedRoadState,BridgeRequest
from .util import digest_obj,file_sha256,now_ns
from .audit import audit_mixed_road_receipt
from .ledger import BridgeLedger
from .errors import *

class MixedSectorRoadEngine:
    def __init__(self,portal_engine,bridge_engine,road_capacity_manager,output_dir,ledger_path=None):
        from pathlib import Path
        self.portal=portal_engine; self.bridge=bridge_engine; self.capacity=road_capacity_manager; self.output_dir=Path(output_dir); self.output_dir.mkdir(parents=True,exist_ok=True); self.ledger=BridgeLedger(ledger_path or self.output_dir/'MIXED_ROAD_LEDGER.jsonl')
    def _portal_req(self,req,inst,chain,src,tgt,expected=None):
        return PortalRequest(inst,chain,src,tgt,sector=src.sector,transport_mode='RE_REALIZE',preservation=req.preservation,resolution_required=req.resolution_required,bandwidth_required=req.bandwidth_required,capacity_units_required=req.capacity_units_required,chirality_class=req.chirality_class,residue_class=req.residue_class,route_policy=req.route_policy,closure_target='TARGET_ADDRESS',expected_source_content_root=expected,metadata={'mixed_road':req.road_name,**req.metadata})
    def _bridge_req(self,req,inst,chain,address,target_sector):
        return BridgeRequest(inst,chain,address,address.sector,target_sector,req.bridge_preservation,metadata={'mixed_road':req.road_name,**req.metadata})
    def plan(self,req):
        if not req.waypoints: raise MixedRoadPreflightError('requires waypoints')
        first=self._portal_req(req,req.source_instance,req.source_segment_chain,req.source_address,PortalAddress(req.source_address.domain_id,sector=req.source_address.sector))
        ch,rr=self.portal._source_roots(first)
        actions=[]; holds={}; current=req.source_address; colors=[]; sectors=[current.sector]; idx=0
        for target in req.waypoints:
            if target.sector not in ('QFT','GR'): raise MixedRoadPreflightError('mixed road sectors must be QFT or GR')
            if current.sector!=target.sector:
                bp=self.bridge.plan(self._bridge_req(req,req.source_instance,req.source_segment_chain,current,target.sector))
                nextaddr=PortalAddress(current.domain_id,current.boundary_id,current.logical_location,target.sector,current.recursive_order,current.fabric_tag)
                actions.append(MixedActionPlan(idx,'BRIDGE',asdict(current),asdict(nextaddr),{'bridge_plan':asdict(bp)})); idx+=1; current=nextaddr; sectors.append(current.sector)
            if (current.domain_id,current.boundary_id,current.logical_location)!=(target.domain_id,target.boundary_id,target.logical_location):
                pr=self._portal_req(req,req.source_instance,req.source_segment_chain,current,target)
                cp=self.portal.graph.select(pr,self.capacity.base.available)
                actions.append(MixedActionPlan(idx,'PORTAL',asdict(current),asdict(target),{'corridor':asdict(cp)})); idx+=1
                for eid in cp.edge_ids:holds[eid]=max(holds.get(eid,0),req.capacity_units_required)
                colors.extend(cp.color_trajectory); current=target; sectors.append(current.sector)
        canonical={'source_instance_id':req.source_instance['instance_id'],'source_content_root':ch['content_root'],'source_address':asdict(req.source_address),'waypoints':[asdict(x) for x in req.waypoints],'actions':[asdict(x) for x in actions],'preservation':asdict(req.preservation),'bridge_preservation':asdict(req.bridge_preservation)}
        road_id=digest_obj(canonical)
        return MixedRoadPlan(road_id,req.road_name,req.source_instance['instance_id'],ch['content_root'],rr,asdict(req.source_address),[asdict(x) for x in req.waypoints],[asdict(x) for x in actions],holds,sectors,colors,[MixedRoadState.DECLARED.value,MixedRoadState.PREFLIGHTED.value])
    def execute(self,req):
        plan=self.plan(req); lifecycle=list(plan.lifecycle); current=copy.deepcopy(req.source_instance); chain=list(req.source_segment_chain); address=req.source_address; results=[]; source_hashes={str(p):file_sha256(p) for p in req.source_segment_chain}; fabric_hash=file_sha256(self.portal.fabric.path)
        try:
            self.capacity.begin_road(plan.road_id,plan.hold_requirements); lifecycle += [MixedRoadState.BUS_RESERVED.value,MixedRoadState.RUNNING.value]
            for ap in plan.actions:
                if ap['kind']=='BRIDGE':
                    br=self.bridge.execute(self._bridge_req(req,current,chain,address,ap['target_address']['sector'])); current=br.instance; address=br.address; results.append({'kind':'BRIDGE','result':br}); lifecycle.append(MixedRoadState.ACTION_CLOSED.value)
                else:
                    target=PortalAddress(**ap['target_address']); expected=plan.source_content_root if not results else None
                    # source root can be recomputed from current; expected final invariant is audited end-to-end
                    pr=self._portal_req(req,current,chain,address,target,expected if all(x['kind']=='BRIDGE' for x in results) else None)
                    pres=self.portal.execute(pr); current=pres.destination_instance; chain=list(current.get('segment_chain',[pres.destination_segment_path])); address=target; results.append({'kind':'PORTAL','result':pres}); lifecycle.append(MixedRoadState.ACTION_CLOSED.value)
            lifecycle.append(MixedRoadState.END_TO_END_AUDIT.value)
            # recompute final root through Portal engine helper using current address/sector
            probe=self._portal_req(req,current,chain,address,address)
            final_ch,final_rr=self.portal._source_roots(probe)
            if req.require_end_to_end_content_identity and final_ch['content_root']!=plan.source_content_root: raise MixedRoadExecutionError('end-to-end content root changed')
            if {str(p):file_sha256(p) for p in req.source_segment_chain}!=source_hashes: raise MixedRoadExecutionError('source segments mutated')
            if file_sha256(self.portal.fabric.path)!=fabric_hash: raise MixedRoadExecutionError('base fabric mutated')
            action_receipts=[]; bridges=[]; portals=[]; edges=[]; colors=[]; sector_traj=[req.source_address.sector]
            for x in results:
                rr=x['result'].receipt; action_receipts.append(rr)
                if x['kind']=='BRIDGE': bridges.append(rr); sector_traj.append(rr['target_sector'])
                else: portals.append(rr); edges.extend(rr['corridor']['edge_ids']); colors.extend(rr['corridor']['color_trajectory']); sector_traj.append(rr['sector'])
            lifecycle.append(MixedRoadState.CLOSED.value)
            receipt={'kind':'MIXED_SECTOR_RAINBOW_ROAD_CLOSURE_RECEIPT','status':'CLOSED','road_id':plan.road_id,'road_name':plan.road_name,'source_instance_id':req.source_instance['instance_id'],'final_instance_id':current['instance_id'],'canonical_mmo_id':current.get('canonical_mmo_id'),'source_address':plan.source_address,'final_address':asdict(address),'waypoints':plan.waypoints,'actions':plan.actions,'action_receipts':action_receipts,'portal_receipts':portals,'bridge_receipts':bridges,'source_content_root':plan.source_content_root,'final_content_root':final_ch['content_root'],'source_residue_root':plan.source_residue_root,'final_residue_root':final_rr,'sector_trajectory':sector_traj,'corridor_edge_trajectory':edges,'rainbow_trajectory':colors,'base_fabric_sha256':fabric_hash,'physics_status':'SOFTWARE_REFERENCE_MIXED_SECTOR_TRANSPORT','lifecycle':list(lifecycle),'timestamp_ns':now_ns()}
            audit=audit_mixed_road_receipt(receipt); receipt['audit']=audit
            if not audit['pass']: raise MixedRoadExecutionError('mixed road audit '+str(audit['findings']))
            final=copy.deepcopy(current); final['history']=list(final.get('history',[]))+[{'event':'MIXED_SECTOR_RAINBOW_ROAD_CLOSED','road_id':plan.road_id,'timestamp_ns':now_ns()}]; final['provenance']=list(final.get('provenance',[]))+[{'mixed_sector_road_receipt':receipt}]; final['current_sector']=address.sector
            bm=copy.deepcopy(final.get('brane_m5',{})); bm.setdefault('D',{})['mixed_road_id']=plan.road_id; bm['D']['sector_trajectory']=sector_traj; bm.setdefault('Chi',{})['bridge_relation_ids']=[r['common_ancestry']['relation_id'] for r in bridges]; bm['Chi']['current_sector']=address.sector; bm.setdefault('R',{})['mixed_sector_road_closed']=True; bm.setdefault('P',{})['mixed_sector_road_receipt']=receipt; final['brane_m5']=bm
            lifecycle.append(MixedRoadState.INHERITED.value); receipt['lifecycle']=list(lifecycle); self.ledger.append(receipt); self.capacity.end_road(plan.road_id,'CLOSED')
            import json
            (self.output_dir/(plan.road_id+'.mixedroad.json')).write_text(json.dumps({'plan':asdict(plan),'receipt':receipt,'final_instance':final},indent=2,sort_keys=True),encoding='utf-8')
            return MixedRoadResult(final,address,asdict(plan),receipt,results)
        except Exception as exc:
            partial=bool(results); status=MixedRoadState.FAILED_PARTIAL.value if partial else MixedRoadState.FAILED.value
            fail={'kind':'MIXED_SECTOR_RAINBOW_ROAD_FAILURE_RECEIPT','status':status,'road_id':plan.road_id,'closed_action_count':len(results),'closed_action_kinds':[x['kind'] for x in results],'completion_frontier':asdict(address),'error_type':type(exc).__name__,'error':str(exc),'lifecycle':lifecycle+[status],'timestamp_ns':now_ns()}; self.ledger.append(fail)
            try:self.capacity.end_road(plan.road_id,'FAILED')
            except:pass
            if isinstance(exc,MixedRoadError): exc.receipt=fail; raise
            raise MixedRoadExecutionError(str(exc),fail) from exc
''')

w('12_REFERENCE_IMPLEMENTATION/genesis_sector_bridge/__init__.py', '''
from .model import *
from .representation import RepresentationEngine
from .ancestry import common_ancestry
from .bridge import SectorBridgeEngine
from .mixedroad import MixedSectorRoadEngine
from .audit import audit_bridge_receipt,audit_mixed_road_receipt
from .errors import *
''')

# Schemas
for name, obj in {
'13_SCHEMAS/sector_representation.schema.json':{'title':'SectorRepresentation','type':'object','required':['representation_view_id','sector','source_instance_id','content_root','residue_root','fabric_witness_id'],'properties':{'sector':{'enum':['QFT','GR']},'physics_status':{'const':'SOFTWARE_REFERENCE_READOUT'}}},
'13_SCHEMAS/bridge_request.schema.json':{'title':'BridgeRequest','type':'object','required':['source_instance','source_sector','target_sector','address'],'properties':{'source_sector':{'enum':['QFT','GR']},'target_sector':{'enum':['QFT','GR']}}},
'13_SCHEMAS/bridge_receipt.schema.json':{'title':'BridgeReceipt','type':'object','required':['bridge_id','source_sector','target_sector','fabric_witness_id','common_ancestry','status'],'properties':{'status':{'const':'CLOSED'}}},
'13_SCHEMAS/mixed_road_request.schema.json':{'title':'MixedSectorRoadRequest','type':'object','required':['source_instance','source_address','waypoints']},
'13_SCHEMAS/mixed_road_receipt.schema.json':{'title':'MixedSectorRoadReceipt','type':'object','required':['road_id','actions','action_receipts','status'],'properties':{'status':{'const':'CLOSED'}}},
}.items(): wj(name,obj)

w('16_TESTS/TEST_MATRIX.md', '''
# Section-06 Test Matrix

Coverage includes:

* QFT and GR readout construction;
* deterministic fabric witness;
* R_QG common-ancestry admission/rejection;
* QFT->GR Bridge;
* GR->QFT Bridge;
* unsupported sector rejection;
* no in-place Geometric mutation;
* no base-fabric mutation;
* invariant content/residue preservation;
* Bridge receipt audit/tamper detection;
* BRANE M^5 bridge lift;
* mixed Road planning with automatic Bridge insertion;
* QFT Portal -> GR Bridge -> GR Portal;
* GR Portal -> QFT Bridge -> QFT Portal;
* Bridge-only waypoint;
* multiple sector changes;
* end-to-end content identity;
* append-only action receipts;
* partial-failure frontier;
* Rainbow Bus hold/release behavior.
''')

# Comprehensive test
w('16_TESTS/test_section06.py', r'''
import json,sys,tempfile,hashlib,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V5=ROOT/'12_REFERENCE_IMPLEMENTATION'/'vendor_section05'
V4=V5/'vendor_section04'
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION')); sys.path.insert(0,str(V5)); sys.path.insert(0,str(V4)); sys.path.insert(0,str(V4/'vendor_section03'))
from vendor.genesis_chirality_machine.image import FabricImageBuilder,FabricImage
from vendor.genesis_chirality_machine.fixture import deterministic_cells
from vendor.genesis_geometric_engine.allocator import RegionAllocator
from vendor.genesis_geometric_engine.segment import GeometricOverlayWriter
from genesis_portal_engine import CorridorGraph,CapacityLedger,PortalEngine
from genesis_portal_engine.model import CorridorEdge,PortalAddress,PreservationContract
from genesis_portal_engine.util import file_sha256
from genesis_rainbow_road.bus import RoadCapacityManager
from genesis_rainbow_road.ledger import RoadLedger
from genesis_sector_bridge import *
from genesis_sector_bridge.model import BridgeRequest,MixedSectorRoadRequest
from genesis_sector_bridge.errors import *


def mk_source(tmp,count=64):
    fp=tmp/'f.gcf'; FabricImageBuilder.build(fp,deterministic_cells(4096)); f=FabricImage(fp); alloc=RegionAllocator(f.cell_count,alignment=8); rid,reg=alloc.reserve(count,'src')
    mmo='TEST:MMO'; iid='source-instance'; sp=tmp/'src.gos'; wr=GeometricOverlayWriter(sp,f.fabric_tag,reg.start,reg.count,hashlib.sha256(mmo.encode()).hexdigest(),hashlib.sha256(iid.encode()).hexdigest(),'0'*64)
    for i in range(count):wr.write(reg.start+i,f.read(f.address_for_index(reg.start+i)))
    wr.finalize(); alloc.commit(rid)
    inst={'instance_id':iid,'canonical_mmo_id':mmo,'representation_id':'TEST:REP','fabric_tag':f.fabric_tag,'region':{'start':reg.start,'count':reg.count,'alignment':reg.alignment,'guard_before':0,'guard_after':0},'mapping_profile':'TEST_3P1P1','roles':['state'],'cells_per_voxel':1,'segment_path':str(sp),'segment_sha256':file_sha256(sp),'segment_chain':[str(sp)],'state':'LIVE','history':[],'provenance':[],'brane_m5':{'I':{'instance_id':iid},'D':{},'Chi':{},'R':{'recursive_depth':1},'P':{}}}
    return f,alloc,inst

def graph():
    es=[
      CorridorEdge('e_ab','A','B',('QFT','GR'),('ANY',),('ANY',),.95,.92,3,1,'Red',True),
      CorridorEdge('e_bc','B','C',('QFT','GR'),('ANY',),('ANY',),.90,.88,3,1,'Orange',True),
      CorridorEdge('e_cd','C','D',('QFT','GR'),('ANY',),('ANY',),.86,.82,3,1,'Green',True),
      CorridorEdge('e_de','D','E',('QFT','GR'),('ANY',),('ANY',),.84,.80,3,1,'Violet',True),
    ]; return CorridorGraph(es)

def setup(tmp):
    tmp.mkdir(parents=True,exist_ok=True); f,alloc,inst=mk_source(tmp); g=graph(); base=CapacityLedger({e.edge_id:e.capacity_units for e in g.edges.values()},tmp/'base.jsonl'); mgr=RoadCapacityManager(base,RoadLedger(tmp/'bus.jsonl')); pe=PortalEngine(f,alloc,g,mgr,tmp/'portals'); be=SectorBridgeEngine(f,tmp/'bridges'); me=MixedSectorRoadEngine(pe,be,mgr,tmp/'mixed'); return f,alloc,inst,g,base,mgr,pe,be,me

def preq(inst,source='QFT',target='GR',domain='A'):
    return BridgeRequest(inst,list(inst['segment_chain']),PortalAddress(domain,sector=source),source,target)

def mreq(inst,start='QFT',wps=None):
    if wps is None:wps=[PortalAddress('B',sector=start),PortalAddress('C',sector='GR' if start=='QFT' else 'QFT')]
    return MixedSectorRoadRequest(inst,list(inst['segment_chain']),PortalAddress('A',sector=start),wps,PreservationContract(['__FULL_CELL__']),resolution_required=.5,bandwidth_required=.5,capacity_units_required=1,road_name='mixed-test')

def run():
  n=0
  with tempfile.TemporaryDirectory() as td:
    tmp=Path(td); f,alloc,inst,g,base,mgr,pe,be,me=setup(tmp)
    # representations
    q=be.reps.read(inst,inst['segment_chain'],PortalAddress('A',sector='QFT'),'QFT','Q'); gview=be.reps.read(inst,inst['segment_chain'],PortalAddress('A',sector='GR'),'GR','G')
    n+=1; assert q.sector=='QFT' and gview.sector=='GR'
    n+=1; assert q.fabric_witness_id==gview.fabric_witness_id
    n+=1; assert q.content_root==gview.content_root and q.residue_root==gview.residue_root
    ca=common_ancestry(q,gview); n+=1; assert ca['admitted']
    n+=1; assert len(ca['relation_id'])==64
    # mismatch
    bad=copy.deepcopy(gview); bad.fabric_witness_id='x'*64
    try:common_ancestry(q,bad); assert False
    except CommonAncestryMismatch:pass
    n+=1
    # deterministic view IDs
    q2=be.reps.read(inst,inst['segment_chain'],PortalAddress('A',sector='QFT'),'QFT','Q'); n+=1; assert q2.representation_view_id==q.representation_view_id
    # bridge q->g
    sh=file_sha256(inst['segment_path']); fh=file_sha256(f.path); br=be.execute(preq(inst)); n+=1; assert br.receipt['status']=='CLOSED'
    n+=1; assert br.receipt['source_sector']=='QFT' and br.receipt['target_sector']=='GR'
    n+=1; assert br.receipt['source_content_root']==br.receipt['target_content_root']
    n+=1; assert br.receipt['source_residue_root']==br.receipt['target_residue_root']
    n+=1; assert br.instance['instance_id']==inst['instance_id']
    n+=1; assert br.instance['segment_chain']==inst['segment_chain']
    n+=1; assert br.address.sector=='GR' and br.address.domain_id=='A'
    n+=1; assert br.instance['history'][-1]['event']=='SECTOR_BRIDGE_CLOSED'
    n+=1; assert br.instance['brane_m5']['Chi']['current_sector']=='GR'
    n+=1; assert audit_bridge_receipt(br.receipt)['pass']
    n+=1; assert file_sha256(inst['segment_path'])==sh and file_sha256(f.path)==fh
    # reverse
    bg=be.execute(preq(inst,'GR','QFT')); n+=1; assert bg.receipt['target_sector']=='QFT'
    # unsupported
    try:be.execute(preq(inst,'QFT','QFT')); assert False
    except UnsupportedSectorPair:pass
    n+=1
    # tamper audit
    tam=copy.deepcopy(br.receipt); tam['target_content_root']='bad'; n+=1; assert not audit_bridge_receipt(tam)['pass']
    # bridge ledger chain
    lines=[json.loads(x) for x in (tmp/'bridges'/'BRIDGE_LEDGER.jsonl').read_text().splitlines() if x.strip()]; n+=1; assert lines and all('entry_hash' in x for x in lines)
    # mixed plan QFT portal then bridge then GR portal
    req=mreq(inst,'QFT',[PortalAddress('B',sector='QFT'),PortalAddress('C',sector='GR')]); plan=me.plan(req); kinds=[x['kind'] for x in plan.actions]
    n+=1; assert kinds==['PORTAL','BRIDGE','PORTAL']
    n+=1; assert plan.actions[1]['source_address']['domain_id']=='B' and plan.actions[1]['target_address']['sector']=='GR'
    n+=1; assert plan.hold_requirements=={'e_ab':1,'e_bc':1}
    n+=1; assert plan.sector_trajectory==['QFT','GR']
    # execute
    res=me.execute(req); n+=1; assert res.receipt['status']=='CLOSED'
    n+=1; assert [x['kind'] for x in res.action_results]==['PORTAL','BRIDGE','PORTAL']
    n+=1; assert len(res.receipt['portal_receipts'])==2 and len(res.receipt['bridge_receipts'])==1
    n+=1; assert res.receipt['source_content_root']==res.receipt['final_content_root']
    n+=1; assert res.final_address.domain_id=='C' and res.final_address.sector=='GR'
    n+=1; assert res.final_instance['canonical_mmo_id']==inst['canonical_mmo_id']
    n+=1; assert res.final_instance['brane_m5']['Chi']['current_sector']=='GR'
    n+=1; assert res.receipt['corridor_edge_trajectory']==['e_ab','e_bc']
    n+=1; assert res.receipt['rainbow_trajectory']==['Red','Orange']
    n+=1; assert audit_mixed_road_receipt(res.receipt)['pass']
    n+=1; assert base.available('e_ab')==3 and base.available('e_bc')==3
    n+=1; assert file_sha256(inst['segment_path'])==sh and file_sha256(f.path)==fh
    # bridge-only target same domain
    f2,a2,i2,g2,b2,m2,p2,be2,me2=setup(tmp/'bridgeonly'); rr=me2.execute(mreq(i2,'QFT',[PortalAddress('A',sector='GR')])); n+=1; assert len(rr.receipt['portal_receipts'])==0 and len(rr.receipt['bridge_receipts'])==1
    n+=1; assert rr.final_instance['instance_id']==i2['instance_id']
    # GR -> QFT mixed
    f3,a3,i3,g3,b3,m3,p3,be3,me3=setup(tmp/'reverse'); rr=me3.execute(mreq(i3,'GR',[PortalAddress('B',sector='GR'),PortalAddress('C',sector='QFT')])); n+=1; assert rr.final_address.sector=='QFT'
    n+=1; assert rr.receipt['bridge_receipts'][0]['source_sector']=='GR'
    # multiple bridges
    f4,a4,i4,g4,b4,m4,p4,be4,me4=setup(tmp/'multi'); rr=me4.execute(mreq(i4,'QFT',[PortalAddress('B',sector='GR'),PortalAddress('C',sector='QFT'),PortalAddress('D',sector='GR')])); n+=1; assert len(rr.receipt['bridge_receipts'])==3
    n+=1; assert len(rr.receipt['portal_receipts'])==3
    n+=1; assert rr.final_address.sector=='GR' and rr.final_address.domain_id=='D'
    # preflight unreachable before bus hold
    bad=mreq(inst,'QFT',[PortalAddress('Z',sector='QFT')])
    try:me.plan(bad); assert False
    except Exception:pass
    n+=1; assert mgr.active is None
    # partial failure after first action - bridge engine fail after first portal
    f5,a5,i5,g5,b5,m5,p5,be5,me5=setup(tmp/'partial')
    class FailBridge:
        def __init__(self,real):self.real=real
        def plan(self,*a,**k):return self.real.plan(*a,**k)
        def execute(self,*a,**k):raise RuntimeError('injected bridge failure')
    me5.bridge=FailBridge(be5)
    try:me5.execute(mreq(i5,'QFT',[PortalAddress('B',sector='QFT'),PortalAddress('C',sector='GR')])); assert False
    except MixedRoadExecutionError as e:
        n+=1; assert e.receipt['status']=='FAILED_PARTIAL'
        n+=1; assert e.receipt['closed_action_count']==1
        n+=1; assert e.receipt['completion_frontier']['domain_id']=='B'
    n+=1; assert b5.available('e_ab')==3 and b5.available('e_bc')==3
    # files persisted
    n+=1; assert list((tmp/'mixed').glob('*.mixedroad.json'))
    for ff in (f,f2,f3,f4,f5):ff.close()
  return n
if __name__=='__main__':
    n=run(); print(f'{n}/{n} PASS')
''')

w('17_EXAMPLES/MIXED_ROAD_EXAMPLE.json', json.dumps({
    'source':'MMO@ALPHA/QFT',
    'waypoints':['GREEN/QFT','OMEGA/GR'],
    'expanded_actions':['Portal<QFT>: ALPHA->GREEN','Bridge<QFT,GR>: GREEN','Portal<GR>: GREEN->OMEGA'],
    'rule':'sector changes are explicit bridge actions; Portals remain single-sector'
},indent=2))

w('18_SOURCE_CROSSWALK/SOURCE_CROSSWALK.md', r'''
# Source Crosswalk

## Primary mathematical source

`1.0 | QFT - GR BRIDGE(1).zip`

Key source statements retained by Section 06:

```text
rho_Q : F -> Q_QFT
rho_G : F -> Q_GR
R_QG = {(q,g) | exists F: q=rho_Q(F), g=rho_G(F)}
P_W^chi : F_a -> F_b
rho_s o P_W^chi = U_s(W) o rho_s
```

The source explicitly marks exact typing/commuting proof as a closure target/open obligation. Section 06 therefore implements typed software descriptors and receipts without upgrading that physical proof status.

## Runtime lineage

Sections 01-05 provide the fabric, Geometric, transformation, Portal and Rainbow Road execution objects consumed here.

## Astraeus mathematics

Transduction Geometry, Bandwidth Algebra, Resolution & Readout, Identity Through History, and Holonomy & Chirality supply the surrounding mathematics for representation change, admissibility, identity witnesses, and path-sensitive transport.

## API 4.3

Used as the preserved queryable mathematical address/provenance domain. API technology is not treated as the ontology itself.
''')

wj('18_SOURCE_CROSSWALK/SOURCE_REGISTRY.json',{
    'section':'06','version':'0.1.0','sources':[
        {'name':'QFT_GR_BRIDGE','path':'/mnt/data/1.0 | QFT - GR BRIDGE(1).zip','role':'PRIMARY_FORMAL_BRIDGE'},
        {'name':'SECTION_05','path':str(s05),'role':'EXECUTION_PARENT'},
        {'name':'MK_ULTRA_TOME','path':'/mnt/data/MK Ultra(2).pdf','role':'LARGE_REFERENCE_INFORMATION_QFT_GR'},
        {'name':'TRANSDUCTION_GEOMETRY','path':'/mnt/data/TRANSDUCTION_GEOMETRY_v1.0.zip','role':'PRIMARY_MATH'},
        {'name':'BANDWIDTH_ALGEBRA','path':'/mnt/data/Bandwidth Algebra.zip','role':'PRIMARY_MATH'},
        {'name':'RESOLUTION_READOUT','path':'/mnt/data/Resolution Readout.zip','role':'PRIMARY_MATH'},
        {'name':'IDENTITY_HISTORY','path':'/mnt/data/Identity Through History.zip','role':'PRIMARY_MATH'},
        {'name':'HOLONOMY_CHIRALITY','path':'/mnt/data/Holonomy and Chirality.zip','role':'PRIMARY_MATH'},
    ],'status_note':'Software implementation does not promote source OPEN_TYPING physical bridge claims.'
})

w('19_RECOVERY/SECTION_06_STATE.md', '''
# Section-06 Recovery State

**Complete:** QFT/GR sector representation descriptors, common-fabric witness, R_QG relation, explicit Bridge transaction, mixed-sector Road expansion/execution, receipts, BRANE lift, tests, and reference fixture runs.

**Preserved open boundary:** source-level physical domains/codomains and proof of the universal QFT/GR intertwining law remain open where the source marks them open.

**Next natural layer:** Section 07 — Quantum Information State + Effect System, where superposition, entanglement, measurement, channel classes, linear ownership, and coherence become executable Genesis/Portal semantics rather than descriptor-only fields.
''')

# Run tests
cmd=[sys.executable,str(ROOT/'16_TESTS'/'test_section06.py')]
p=subprocess.run(cmd,capture_output=True,text=True,cwd=ROOT,timeout=120)
if p.returncode!=0:
    print(p.stdout); print(p.stderr,file=sys.stderr); raise SystemExit(p.returncode)
w('99_RELEASE/TEST_RESULTS.txt',p.stdout.strip()+'\n')

# Core checksums/manifest (before fixtures)
def sha(p):
    h=hashlib.sha256();
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
files=[x for x in ROOT.rglob('*') if x.is_file() and '20_REAL_FIXTURE_TRANSDUCTIONS' not in x.parts and '99_RELEASE/CORE_CHECKSUMS.sha256' not in str(x) and '99_RELEASE/CORE_MANIFEST.json' not in str(x)]
lines=[]
for x in sorted(files): lines.append(f"{sha(x)}  {x.relative_to(ROOT)}")
w('99_RELEASE/CORE_CHECKSUMS.sha256','\n'.join(lines)+'\n')
wj('99_RELEASE/CORE_MANIFEST.json',{'name':NAME,'section':'06','version':'0.1.0','test_result':p.stdout.strip(),'core_file_count':len(files),'generated_at_ns':time.time_ns()})
print('BUILT',ROOT,'TESTS',p.stdout.strip())
