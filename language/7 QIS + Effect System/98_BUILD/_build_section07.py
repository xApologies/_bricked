from pathlib import Path
import shutil, json, textwrap, hashlib, os, zipfile, math, cmath, random, subprocess, sys

ROOT = Path('/mnt/data/GENESIS_CHIRALITY_MACHINE_SECTION_07_QUANTUM_INFORMATION_EFFECTS_v0.1.0_20260821')
if ROOT.exists(): shutil.rmtree(ROOT)
for d in [
'00_START_HERE','01_ARCHITECTURE','02_STATE_MODEL','03_LINEAR_OWNERSHIP','04_SUPERPOSITION','05_ENTANGLEMENT','06_CHANNELS','07_MEASUREMENT','08_EFFECT_SYSTEM','09_PORTAL_INTEGRATION','10_BRIDGE_BOUNDARY','11_BRANE_LIFT','12_REFERENCE_IMPLEMENTATION/genesis_quantum_effects','12_REFERENCE_IMPLEMENTATION/vendor_section06','13_SCHEMAS','14_PSEUDOCODE','15_FAILURES','16_TESTS','17_EXAMPLES','18_SOURCE_CROSSWALK','19_RECOVERY','20_REFERENCE_QUANTUM_INFORMATION_RUNS','98_BUILD','99_RELEASE']:
    (ROOT/d).mkdir(parents=True, exist_ok=True)

def w(rel, txt):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(textwrap.dedent(txt).lstrip(),encoding='utf-8')
def j(rel,obj):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,sort_keys=True),encoding='utf-8')

w('00_START_HERE/FOLDER_NAME.txt', ROOT.name+'\n')
w('00_START_HERE/README.md', r'''
# Genesis Chirality Machine — Section 07
## Quantum Information State + Effect System

**Version:** 0.1.0 — software reference implementation
**Date:** 2026-08-21

Section 07 adds quantum-information semantics to the Genesis Chirality Machine without redefining the chirality fabric as a qubit array and without claiming that the present software emulator is quantum hardware.

The section introduces:

- pure and density-state reference representations;
- superposition as coherent state-space structure, not classical duplication;
- entanglement as a joint nonseparable relationship, not a transport channel;
- unitary/isometric/CPTP-style channel classes;
- projective measurement and classicalization boundaries;
- linear ownership and explicit no-cloning enforcement for nonclassical state handles;
- coherence, trace, normalization, purity, fidelity, and recoverability diagnostics;
- quantum effect contracts for `Portal<QFT>`;
- an explicit rule that QFT/GR transduction does **not** automatically preserve quantum coherence or entanglement;
- BRANE M5 effect/provenance lift fields;
- a small generic finite-dimensional reference simulator used only as an execution oracle for future Genesis language semantics.

### Governing distinction

```text
chirality fabric            = common organizational substrate in the project architecture
quantum-information state   = optional typed state carried/read in the QFT sector
entanglement                 = joint state relationship
Portal                       = information transport transaction
Corridor                     = admissible transport path
Rainbow Road                 = persistent composition of Portals
Bridge<QFT,GR>               = typed representation transduction, not an assumed quantum channel
```

### Scope boundary

Everything in Section 07 is a **software reference semantics**. It is designed to make the future Genesis compiler precise. It does not claim that an MMO, a chirality fabric cell, or a QFT/GR bridge has been physically realized as quantum hardware.
''')
w('00_START_HERE/RECOVERY_ORDER.md', r'''
# Recovery order
1. Mount Part A first. It contains the complete Section 07 architecture, reference implementation, schemas, tests, examples, source crosswalk, and recovery state.
2. Mount Part B for reference quantum-information runs and Section 06 mixed-sector fixtures.
3. Mount Part C for implementation lineage Sections 01–06, CFP, Rainbow Road, Corridor mathematics, and Layer Zero.
4. Mount Part D for Astraeus mathematics, API 4.3, and the QFT/GR bridge.
5. Mount Part E for the MK Ultra Tome and quantum/information reference corpus.

Do not silently promote software reference semantics into physical claims.
''')

w('01_ARCHITECTURE/ARCHITECTURE.md', r'''
# Section 07 architecture

```text
MMO / Geometric
      |
      | QFT readout / quantum-information attachment
      v
Quantum State Handle
      |
      +-- linear ownership / no cloning
      +-- superposition
      +-- entanglement graph
      +-- unitary / channel effects
      +-- measurement / classicalization
      |
      v
Portal<QFT> Quantum Effect Envelope
      |
      v
Corridor admission + Rainbow Road transport
      |
      +-- QFT -> QFT: quantum-preserving effects MAY be declared if the channel contract admits them
      |
      +-- QFT -> GR: Section 06 Bridge is representation transduction only;
                    quantum coherence/entanglement do not automatically cross
      v
Closure Receipt + History + Provenance + BRANE M5 effect lift
```

## Central rule
Genesis does not treat a quantum state as a copyable Python value. A nonclassical state is an owned resource with a lifecycle. Operations must declare what they preserve, consume, measure, decohere, or classicalize.

## Why this exists
The future Genesis language is Portal-native and information-transformational. Quantum programming languages already supply mature semantics for coherent state transformation, joint states, measurement, channels, and linear ownership. Section 07 inherits those semantics only where they solve an actual Genesis problem.
''')
w('01_ARCHITECTURE/DESIGN_INVARIANTS.md', r'''
# Design invariants

1. **Chirality is deeper than quantum readout in this architecture.** Quantum state representation is optional and sector-scoped.
2. **Entanglement is not transportation.** It is a joint-state relationship. A Portal remains required for controllable information transport.
3. **No implicit cloning.** Nonclassical state handles cannot be copied by assignment semantics in the reference model.
4. **Measurement is an effect boundary.** It changes typestate and emits a classical result receipt.
5. **QFT/GR bridge is not automatically a quantum channel.** Section 06 common-ancestry transduction preserves declared structural invariants only.
6. **No hidden information preservation.** Lossy/projective/dephasing channels must advertise effects.
7. **Normalization and trace are audited.** Pure states remain norm 1; density states remain trace 1 within tolerance.
8. **Portal quantum effects are QFT-scoped.** GR Portal semantics remain geometric unless an explicit future bridge/channel type is defined.
9. **MMO identity is not quantum-state identity.** Quantum state attachments are representation/effect objects associated with an MMO/Geometric.
10. **Software reference only.** State-vector and density-matrix simulation is an execution oracle, not a physical implementation claim.
''')

w('02_STATE_MODEL/QUANTUM_INFORMATION_STATE.md', r'''
# Quantum information state model

Section 07 uses a generic finite-dimensional state model. It deliberately does not make `qubit` the primitive Genesis object.

A pure reference state is

`|psi> = sum_i a_i |b_i>`

with `sum_i |a_i|^2 = 1`.

A density state is a positive, trace-one operator represented in the reference backend as a finite complex matrix. The implementation validates Hermiticity and trace; full positive-semidefinite certification is intentionally limited to small reference cases.

Each state is attached to:

- a `state_id`;
- an optional `source_instance_id` / MMO identity;
- a basis or joint member ordering;
- a lifecycle/ownership token;
- a provenance trail;
- the QFT sector.

This is an execution model for language semantics, not a claim that every MMO literally is a finite qubit register.
''')
w('02_STATE_MODEL/STATE_KINDS.md', r'''
# State kinds

- `CLASSICAL`: definite information, freely copyable after classicalization under ordinary object rules.
- `PURE`: normalized coherent state vector.
- `DENSITY`: mixed or reduced state.
- `JOINT`: state over two or more named members.
- `MEASURED`: post-measurement state with classical outcome lineage.
- `DECOHERED`: density state after a coherence-reducing channel.
- `CONSUMED`: handle no longer owns a live quantum resource.

A state kind is not a physical ontology. It is a programming-language typestate used by the reference runtime.
''')

w('03_LINEAR_OWNERSHIP/LINEAR_RESOURCE_MODEL.md', r'''
# Linear resource model

Quantum information is not modeled as an ordinary copyable value. The runtime registry gives each live nonclassical state one ownership token.

Allowed operations:

- `borrow_metadata`: inspect non-state metadata without duplicating amplitudes;
- `move`: transfer ownership to a new owner label while preserving the state ID;
- `consume`: terminate the live handle;
- `measure`: consume the coherent handle and produce a measured successor plus classical result;
- `classical_copy`: only after an explicitly classical result exists.

Forbidden operation:

- `clone_quantum_state` for any live PURE/DENSITY/JOINT quantum resource.

This is a compiler/runtime discipline inspired by quantum no-cloning and linear type systems. It is stronger than Python aliasing semantics and will become a Genesis type/effect rule.
''')
w('03_LINEAR_OWNERSHIP/OWNERSHIP_LIFECYCLE.md', r'''
# Ownership lifecycle

```text
ALLOCATED -> OWNED -> MOVED -> OWNED
                    -> MEASURED -> CLASSICAL_RESULT + POST_MEASURE_STATE
                    -> CONSUMED

OWNED --borrow_metadata--> OWNED
OWNED --clone--> ERROR
```

The registry is deterministic and auditable. An ownership receipt records old owner, new owner, state ID, operation, and timestamp.
''')

w('04_SUPERPOSITION/SUPERPOSITION.md', r'''
# Superposition semantics

Superposition is coherent state-space composition, not a list of simultaneous classical values.

The reference constructor accepts named branches and complex amplitudes, normalizes them, and produces a `PURE` state. Branch labels are semantic basis labels. The runtime does not infer physical basis meaning from their names.

Compiler consequence: a superposed value cannot be branched on by ordinary classical `if` without an explicit measurement or readout effect.
''')
w('04_SUPERPOSITION/COHERENCE.md', r'''
# Coherence diagnostics

For density state `rho`, the reference coherence diagnostic is the sum of absolute off-diagonal entries. It is a software diagnostic, not a universal physical coherence measure.

Section 07 also exposes:

- norm / trace;
- purity `Tr(rho^2)`;
- pure-state fidelity `|<psi|phi>|^2`;
- optional exact-recovery comparison against a preserved source state.

Diagnostics never replace the declared effect contract.
''')

w('05_ENTANGLEMENT/ENTANGLEMENT.md', r'''
# Entanglement semantics

Entanglement is represented as a **joint state** whose member decomposition cannot be treated as independent owned pure states.

A canonical reference fixture uses a Bell-like state:

`(|00> + |11>) / sqrt(2)`

for two named semantic members. The runtime can compute a two-level reduced density matrix for diagnostics.

## Rule
Entanglement is a relationship resource, not a message channel. A controllable payload still moves through a Portal/Corridor/Rainbow Road transaction.
''')
w('05_ENTANGLEMENT/ENTANGLEMENT_OWNERSHIP.md', r'''
# Entanglement ownership

A joint state owns the coherent relationship. Member labels do not each own an independently copyable state.

Operations that separate, measure, or discard a subsystem must declare the effect. The reference implementation prevents extracting a standalone pure state from an entangled member without measurement/reduction semantics.
''')

w('06_CHANNELS/CHANNEL_CLASSES.md', r'''
# Channel classes

Section 07 recognizes these semantic channel classes:

- `IDENTITY`
- `UNITARY`
- `ISOMETRIC_REFERENCE`
- `CPTP_REFERENCE`
- `DEPHASING`
- `PROJECTIVE`
- `CLASSICALIZE`
- `STRUCTURAL_TRANSDUCTION`

`UNITARY` requires a square matrix with `U†U = I` within tolerance.

`CPTP_REFERENCE` uses Kraus operators and verifies the trace-preservation condition `sum K†K = I` within tolerance. Complete positivity is inherited from the Kraus representation used by the reference backend.

`STRUCTURAL_TRANSDUCTION` is intentionally **not** a quantum channel claim. It names the Section 06 QFT/GR structural bridge boundary.
''')
w('06_CHANNELS/RECOVERY_AND_FIDELITY.md', r'''
# Recovery and fidelity

Quantum transport contracts may declare:

- exact identity preservation;
- fidelity threshold;
- coherence threshold;
- entanglement preservation requirement;
- trace/norm preservation;
- recoverability target.

A Portal cannot claim a stronger preservation class than the channel implementation and audit demonstrate.
''')

w('07_MEASUREMENT/MEASUREMENT.md', r'''
# Measurement semantics

Measurement is explicit. The reference computational-basis measurement:

1. validates a live owned state;
2. computes outcome probabilities;
3. samples with an injected deterministic/random source;
4. emits a classical outcome receipt;
5. creates a normalized post-measurement state;
6. marks the original coherent handle consumed.

The future Genesis compiler should treat measurement as an effectful operation that changes typestate and may destroy superposition/entanglement.
''')
w('07_MEASUREMENT/CLASSICALIZATION.md', r'''
# Classicalization

Classicalization means a quantum resource has crossed an explicit readout boundary and produced ordinary copyable information. It is not a synonym for QFT->GR transduction.

A classical result may be copied under normal data semantics. The quantum parent remains in its measured/consumed lineage state.
''')

w('08_EFFECT_SYSTEM/EFFECT_ALGEBRA.md', r'''
# Quantum effect algebra

Effects are compiler-visible declarations:

`READ_META, SUPERPOSE, ENTANGLE, UNITARY, CHANNEL, DEPHASE, MEASURE, CLASSICALIZE, QFT_PORTAL_TRANSPORT, STRUCTURAL_TRANSDUCE, RECOVER`.

Each effect specifies:

- required input typestate;
- output typestate;
- whether ownership is consumed/moved;
- whether norm/trace is preserved;
- whether coherence may decrease;
- whether entanglement may be destroyed;
- permitted sector;
- whether a classical result is emitted.

Effects compose only when output typestate satisfies the next effect's input contract.
''')
w('08_EFFECT_SYSTEM/STATIC_RULES.md', r'''
# Static rules

1. `SUPERPOSE` requires QFT quantum semantics and creates a coherent PURE state.
2. `ENTANGLE` consumes/moves component ownership into one JOINT state.
3. `UNITARY` preserves norm and does not classicalize.
4. `DEPHASE` returns a density state and may reduce coherence.
5. `MEASURE` consumes a live coherent handle and emits a classical outcome plus measured successor.
6. `QFT_PORTAL_TRANSPORT` requires a QFT Portal and a declared channel.
7. `STRUCTURAL_TRANSDUCE` may change QFT/GR representation but does not imply preservation of quantum coherence.
8. A GR-only Portal cannot accept a live coherent quantum handle unless a future explicit channel/bridge type is registered.
''')

w('09_PORTAL_INTEGRATION/QUANTUM_PORTAL_ENVELOPE.md', r'''
# Quantum Portal envelope

A `Portal<QFT>` may carry a `QuantumEffectEnvelope` containing:

- `quantum_state_id`;
- channel class and channel ID;
- ownership token;
- preservation contract;
- source/destination Portal addresses;
- source MMO/Geometric identity;
- coherence/fidelity requirements;
- entanglement relationship IDs;
- expected closure effects.

The Portal engine remains responsible for Corridor admission and information transportation. Section 07 adds quantum state/effect validation around that transaction.
''')
w('09_PORTAL_INTEGRATION/PORTAL_QUANTUM_CLOSURE.md', r'''
# Portal quantum closure

Quantum closure requires both layers to pass:

1. ordinary Section 04/05 Portal/Road closure;
2. Section 07 quantum effect audit.

A closed transport receipt records:

- source and destination state IDs;
- channel class;
- ownership transition;
- norm/trace checks;
- fidelity/coherence checks where declared;
- entanglement-preservation status where declared;
- ordinary Portal/Corridor receipt ID;
- MMO identity/provenance linkage.
''')

w('10_BRIDGE_BOUNDARY/QFT_GR_QUANTUM_BOUNDARY.md', r'''
# QFT/GR bridge quantum boundary

Section 06 established `Bridge<QFT,GR>` and `Bridge<GR,QFT>` as typed **representation transductions over common chirality ancestry**.

Section 07 deliberately does **not** reinterpret that bridge as a unitary, isometry, CPTP channel, or entanglement-preserving physical transport.

Default policy:

```text
LIVE QUANTUM STATE + QFT->GR BRIDGE
    => reject quantum-preservation claim
    => permit one of:
         A. measure/classicalize first;
         B. carry only declared structural invariant capsule;
         C. use a future separately registered quantum bridge channel.
```

This rule prevents the implementation from claiming physics that the source bridge does not establish.
''')
w('10_BRIDGE_BOUNDARY/STRUCTURAL_INVARIANT_CAPSULE.md', r'''
# Structural invariant capsule

A `StructuralInvariantCapsule` may preserve non-quantum identity information across the Section 06 bridge:

- canonical MMO ID;
- content root;
- residue root;
- source representation ID;
- chirality/common-ancestry witness;
- provenance/history references.

It intentionally excludes amplitudes, phase coherence, and entanglement-preservation claims unless a future explicit channel contract proves them.
''')

w('11_BRANE_LIFT/QUANTUM_EFFECT_BRANE_ADAPTER.md', r'''
# BRANE M5 quantum-effect adapter

Section 07 does not add a seventh BRANE dimension. Quantum effects are carried as domain content and provenance inside the existing organizational contract:

- `I`: source MMO / Geometric / quantum-state identity references;
- `D`: channel, Portal, entanglement, measurement dependencies;
- `Chi`: chirality/admissibility and effect-class constraints;
- `R`: quantum-state lifecycle, ownership transitions, measurement/transport history;
- `P`: receipts, state hashes, channel definitions, audit results.

BRANE retains ownership of realization coordinate `Z`.
''')

# Reference implementation
pkg='12_REFERENCE_IMPLEMENTATION/genesis_quantum_effects'
w(pkg+'/__init__.py', r'''
from .model import *
from .state import *
from .linear import *
from .channels import *
from .measurement import *
from .effects import *
from .portal import *
from .bridge_policy import *
''')
w(pkg+'/errors.py', r'''
class QuantumEffectError(Exception): pass
class StateValidationError(QuantumEffectError): pass
class NormalizationError(StateValidationError): pass
class OwnershipError(QuantumEffectError): pass
class NoCloningError(OwnershipError): pass
class ConsumedStateError(OwnershipError): pass
class ChannelValidationError(QuantumEffectError): pass
class EffectViolation(QuantumEffectError): pass
class QuantumSectorViolation(QuantumEffectError): pass
class MeasurementError(QuantumEffectError): pass
class BridgeQuantumBoundaryError(QuantumEffectError): pass
class QuantumClosureError(QuantumEffectError): pass
''')
w(pkg+'/util.py', r'''
import hashlib,json,time,math

def now_ns(): return time.time_ns()
def stable(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),default=str)
def digest(obj): return hashlib.sha256(stable(obj).encode()).hexdigest()
def cpair(z): return [float(z.real),float(z.imag)]
def cfrom(x): return complex(float(x[0]),float(x[1]))
def close(a,b,tol=1e-9): return abs(a-b)<=tol
''')
w(pkg+'/model.py', r'''
from dataclasses import dataclass,field
from enum import Enum
from typing import Optional

class StateKind(str,Enum):
    CLASSICAL='CLASSICAL'; PURE='PURE'; DENSITY='DENSITY'; JOINT='JOINT'; MEASURED='MEASURED'; DECOHERED='DECOHERED'; CONSUMED='CONSUMED'
class OwnershipState(str,Enum): OWNED='OWNED'; MOVED='MOVED'; MEASURED='MEASURED'; CONSUMED='CONSUMED'
class ChannelClass(str,Enum): IDENTITY='IDENTITY'; UNITARY='UNITARY'; ISOMETRIC_REFERENCE='ISOMETRIC_REFERENCE'; CPTP_REFERENCE='CPTP_REFERENCE'; DEPHASING='DEPHASING'; PROJECTIVE='PROJECTIVE'; CLASSICALIZE='CLASSICALIZE'; STRUCTURAL_TRANSDUCTION='STRUCTURAL_TRANSDUCTION'
class Effect(str,Enum): READ_META='READ_META'; SUPERPOSE='SUPERPOSE'; ENTANGLE='ENTANGLE'; UNITARY='UNITARY'; CHANNEL='CHANNEL'; DEPHASE='DEPHASE'; MEASURE='MEASURE'; CLASSICALIZE='CLASSICALIZE'; QFT_PORTAL_TRANSPORT='QFT_PORTAL_TRANSPORT'; STRUCTURAL_TRANSDUCE='STRUCTURAL_TRANSDUCE'; RECOVER='RECOVER'

@dataclass
class QuantumState:
    state_id:str
    kind:str
    basis:list
    amplitudes:list=field(default_factory=list)
    density:list=field(default_factory=list)
    members:list=field(default_factory=list)
    source_instance_id:Optional[str]=None
    canonical_mmo_id:Optional[str]=None
    sector:str='QFT'
    provenance:list=field(default_factory=list)
    metadata:dict=field(default_factory=dict)

@dataclass
class OwnershipRecord:
    state_id:str
    token:str
    owner:str
    status:str='OWNED'
    version:int=0

@dataclass
class QuantumPreservation:
    preserve_norm:bool=True
    preserve_trace:bool=True
    preserve_coherence:bool=False
    preserve_entanglement:bool=False
    min_fidelity:float=0.0
    min_coherence:float=0.0

@dataclass
class QuantumEffectEnvelope:
    state_id:str
    channel_class:str
    channel_id:str
    ownership_token:str
    source_address:dict
    target_address:dict
    preservation:QuantumPreservation=field(default_factory=QuantumPreservation)
    entanglement_relation_ids:list=field(default_factory=list)
    metadata:dict=field(default_factory=dict)
''')
w(pkg+'/linalg.py', r'''
import math
from .errors import ChannelValidationError,StateValidationError

def dagger(A): return [[complex(A[j][i]).conjugate() for j in range(len(A))] for i in range(len(A[0]))]
def matmul(A,B):
    if not A or not B or len(A[0])!=len(B): raise StateValidationError('shape mismatch')
    return [[sum(complex(A[i][k])*complex(B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def matvec(A,v):
    if not A or len(A[0])!=len(v): raise StateValidationError('shape mismatch')
    return [sum(complex(A[i][k])*complex(v[k]) for k in range(len(v))) for i in range(len(A))]
def eye(n): return [[1+0j if i==j else 0j for j in range(n)] for i in range(n)]
def add(A,B): return [[complex(A[i][j])+complex(B[i][j]) for j in range(len(A[0]))] for i in range(len(A))]
def scalar(c,A): return [[c*complex(x) for x in row] for row in A]
def outer(v,w=None):
    w=v if w is None else w
    return [[complex(v[i])*complex(w[j]).conjugate() for j in range(len(w))] for i in range(len(v))]
def trace(A): return sum(complex(A[i][i]) for i in range(min(len(A),len(A[0]))))
def frob(A,B): return math.sqrt(sum(abs(complex(A[i][j])-complex(B[i][j]))**2 for i in range(len(A)) for j in range(len(A[0]))))
def is_unitary(U,tol=1e-9):
    if not U or len(U)!=len(U[0]): return False
    return frob(matmul(dagger(U),U),eye(len(U)))<=tol
def density_from_state(v): return outer(v)
def purity(rho):
    return float(trace(matmul(rho,rho)).real)
def coherence_l1(rho):
    return float(sum(abs(complex(rho[i][j])) for i in range(len(rho)) for j in range(len(rho)) if i!=j))
def tensor_vec(a,b): return [complex(x)*complex(y) for x in a for y in b]
def tensor(A,B):
    return [[complex(A[i][j])*complex(B[k][l]) for j in range(len(A[0])) for l in range(len(B[0]))] for i in range(len(A)) for k in range(len(B))]
def validate_kraus(ops,tol=1e-9):
    if not ops: raise ChannelValidationError('no Kraus operators')
    n=len(ops[0][0]); acc=[[0j for _ in range(n)] for _ in range(n)]
    for K in ops:
        if len(K)!=n or len(K[0])!=n: raise ChannelValidationError('Kraus shape')
        acc=add(acc,matmul(dagger(K),K))
    if frob(acc,eye(n))>tol: raise ChannelValidationError('not trace preserving')
    return True
''')
w(pkg+'/state.py', r'''
import math,copy
from .model import QuantumState,StateKind
from .util import digest,cpair,cfrom,now_ns
from .linalg import density_from_state,trace,purity,coherence_l1
from .errors import NormalizationError,StateValidationError

class StateFactory:
    @staticmethod
    def pure(basis,amps,source_instance_id=None,canonical_mmo_id=None,members=None,metadata=None):
        if len(basis)!=len(amps) or not basis: raise StateValidationError('basis/amplitude mismatch')
        amps=[complex(x) for x in amps]; norm=sum(abs(x)**2 for x in amps)
        if norm<=0: raise NormalizationError('zero norm')
        amps=[x/math.sqrt(norm) for x in amps]
        payload={'kind':'PURE','basis':list(basis),'amps':[cpair(x) for x in amps],'source':source_instance_id,'mmo':canonical_mmo_id,'members':members or [],'metadata':metadata or {}}
        sid=digest(payload)
        kind=StateKind.JOINT.value if members and len(members)>1 else StateKind.PURE.value
        return QuantumState(sid,kind,list(basis),[cpair(x) for x in amps],[],list(members or []),source_instance_id,canonical_mmo_id,'QFT',[{'event':'STATE_CREATED','timestamp_ns':now_ns()}],metadata or {})
    @staticmethod
    def density(basis,rho,source_instance_id=None,canonical_mmo_id=None,members=None,kind='DENSITY',metadata=None):
        n=len(basis)
        if len(rho)!=n or any(len(r)!=n for r in rho): raise StateValidationError('density shape')
        rr=[[complex(x) for x in row] for row in rho]
        tr=trace(rr)
        if abs(tr-1)>1e-8: raise NormalizationError('density trace != 1')
        for i in range(n):
            for j in range(n):
                if abs(rr[i][j]-rr[j][i].conjugate())>1e-8: raise StateValidationError('density not Hermitian')
        payload={'kind':kind,'basis':list(basis),'rho':[[cpair(x) for x in row] for row in rr],'source':source_instance_id,'mmo':canonical_mmo_id,'members':members or [],'metadata':metadata or {}}
        sid=digest(payload)
        return QuantumState(sid,kind,list(basis),[],[[cpair(x) for x in row] for row in rr],list(members or []),source_instance_id,canonical_mmo_id,'QFT',[{'event':'DENSITY_CREATED','timestamp_ns':now_ns()}],metadata or {})

def ampvec(state): return [cfrom(x) for x in state.amplitudes]
def rhomat(state):
    if state.density: return [[cfrom(x) for x in row] for row in state.density]
    return density_from_state(ampvec(state))
def diagnostics(state):
    rho=rhomat(state)
    norm=sum(abs(x)**2 for x in ampvec(state)) if state.amplitudes else None
    return {'state_id':state.state_id,'kind':state.kind,'norm':norm,'trace':float(trace(rho).real),'purity':purity(rho),'coherence_l1':coherence_l1(rho),'member_count':len(state.members)}
def pure_fidelity(a,b):
    av,bv=ampvec(a),ampvec(b)
    if len(av)!=len(bv): raise StateValidationError('fidelity dimension')
    return float(abs(sum(x.conjugate()*y for x,y in zip(av,bv)))**2)
''')
w(pkg+'/linear.py', r'''
from .model import OwnershipRecord,OwnershipState,StateKind
from .util import digest,now_ns
from .errors import OwnershipError,NoCloningError,ConsumedStateError

class LinearOwnershipRegistry:
    def __init__(self): self.records={}; self.receipts=[]
    def claim(self,state,owner):
        if state.state_id in self.records and self.records[state.state_id].status==OwnershipState.OWNED.value: raise OwnershipError('already owned')
        tok=digest({'state_id':state.state_id,'owner':owner,'nonce':len(self.records)})
        r=OwnershipRecord(state.state_id,tok,owner,OwnershipState.OWNED.value,0); self.records[state.state_id]=r
        self.receipts.append({'op':'CLAIM','state_id':state.state_id,'owner':owner,'token':tok,'timestamp_ns':now_ns()}); return r
    def assert_owned(self,state_id,token):
        r=self.records.get(state_id)
        if not r or r.status!=OwnershipState.OWNED.value or r.token!=token: raise ConsumedStateError('state not live-owned')
        return r
    def borrow_metadata(self,state_id,token):
        r=self.assert_owned(state_id,token); rec={'op':'BORROW_METADATA','state_id':state_id,'owner':r.owner,'timestamp_ns':now_ns()}; self.receipts.append(rec); return rec
    def move(self,state_id,token,new_owner):
        r=self.assert_owned(state_id,token); old=r.owner; r.owner=new_owner; r.version+=1; r.token=digest({'state_id':state_id,'owner':new_owner,'version':r.version}); rec={'op':'MOVE','state_id':state_id,'old_owner':old,'new_owner':new_owner,'token':r.token,'timestamp_ns':now_ns()}; self.receipts.append(rec); return r
    def clone(self,state,token):
        self.assert_owned(state.state_id,token)
        if state.kind!=StateKind.CLASSICAL.value: raise NoCloningError('live nonclassical state cannot be cloned')
        return {'classical_copy_of':state.state_id}
    def consume(self,state_id,token,reason='CONSUMED'):
        r=self.assert_owned(state_id,token); r.status=OwnershipState.CONSUMED.value; r.version+=1; rec={'op':'CONSUME','state_id':state_id,'reason':reason,'timestamp_ns':now_ns()}; self.receipts.append(rec); return rec
''')
w(pkg+'/superposition.py', r'''
from .state import StateFactory

def superpose(branches,amplitudes,**kw):
    return StateFactory.pure(branches,amplitudes,**kw)
''')
w(pkg+'/entanglement.py', r'''
import math
from .state import StateFactory,ampvec,rhomat
from .linalg import tensor_vec,density_from_state
from .errors import StateValidationError


def bell_pair(member_a,member_b,source_instance_id=None,canonical_mmo_id=None):
    s=1/math.sqrt(2)
    return StateFactory.pure(['00','01','10','11'],[s,0,0,s],source_instance_id,canonical_mmo_id,[member_a,member_b],{'relationship':'BELL_REFERENCE'})

def tensor_product(a,b,member_names=None):
    av,bv=ampvec(a),ampvec(b)
    basis=[f'{x}|{y}' for x in a.basis for y in b.basis]
    members=member_names or (list(a.members or [a.state_id])+list(b.members or [b.state_id]))
    return StateFactory.pure(basis,tensor_vec(av,bv),a.source_instance_id or b.source_instance_id,a.canonical_mmo_id or b.canonical_mmo_id,members,{'relationship':'TENSOR_PRODUCT'})

def reduced_two_level(state,which=0):
    if len(state.basis)!=4 or len(state.members)!=2: raise StateValidationError('reference reduction supports two 2-level members')
    v=ampvec(state)
    # basis order 00,01,10,11. partial trace over other member.
    if which==0:
        r00=abs(v[0])**2+abs(v[1])**2; r11=abs(v[2])**2+abs(v[3])**2; r01=v[0]*v[2].conjugate()+v[1]*v[3].conjugate()
    else:
        r00=abs(v[0])**2+abs(v[2])**2; r11=abs(v[1])**2+abs(v[3])**2; r01=v[0]*v[1].conjugate()+v[2]*v[3].conjugate()
    return [[r00,r01],[r01.conjugate(),r11]]

def is_entangled_reference(state,tol=1e-9):
    if len(state.members)!=2 or len(state.basis)!=4: return False
    red=reduced_two_level(state,0)
    purity=(red[0][0]*red[0][0]+red[0][1]*red[1][0]+red[1][0]*red[0][1]+red[1][1]*red[1][1]).real
    return purity < 1-tol
''')
w(pkg+'/channels.py', r'''
import math
from .model import ChannelClass
from .state import StateFactory,ampvec,rhomat,diagnostics
from .linalg import matvec,matmul,dagger,add,scalar,validate_kraus,is_unitary,trace
from .errors import ChannelValidationError
from .util import digest,now_ns

class QuantumChannel:
    def __init__(self,channel_class,operators=None,name=None):
        self.channel_class=str(channel_class.value if hasattr(channel_class,'value') else channel_class); self.operators=operators or []; self.name=name or self.channel_class
        self.channel_id=digest({'class':self.channel_class,'ops':[[[[float(complex(x).real),float(complex(x).imag)] for x in row] for row in op] for op in self.operators],'name':self.name})
        self.validate()
    def validate(self):
        if self.channel_class==ChannelClass.UNITARY.value:
            if len(self.operators)!=1 or not is_unitary(self.operators[0]): raise ChannelValidationError('invalid unitary')
        elif self.channel_class in (ChannelClass.CPTP_REFERENCE.value,ChannelClass.DEPHASING.value): validate_kraus(self.operators)
        elif self.channel_class==ChannelClass.IDENTITY.value: pass
        return True
    def apply(self,state):
        if self.channel_class==ChannelClass.IDENTITY.value:
            if state.amplitudes: return StateFactory.pure(state.basis,ampvec(state),state.source_instance_id,state.canonical_mmo_id,state.members,{'channel_id':self.channel_id,'parent_state_id':state.state_id,'identity_successor':True})
            return StateFactory.density(state.basis,rhomat(state),state.source_instance_id,state.canonical_mmo_id,state.members,state.kind,{'channel_id':self.channel_id,'parent_state_id':state.state_id,'identity_successor':True})
        if self.channel_class==ChannelClass.UNITARY.value and state.amplitudes:
            out=matvec(self.operators[0],ampvec(state)); return StateFactory.pure(state.basis,out,state.source_instance_id,state.canonical_mmo_id,state.members,{'channel_id':self.channel_id,'parent_state_id':state.state_id})
        rho=rhomat(state); n=len(rho); acc=[[0j for _ in range(n)] for _ in range(n)]
        for K in self.operators: acc=add(acc,matmul(matmul(K,rho),dagger(K)))
        kind='DECOHERED' if self.channel_class==ChannelClass.DEPHASING.value else 'DENSITY'
        return StateFactory.density(state.basis,acc,state.source_instance_id,state.canonical_mmo_id,state.members,kind,{'channel_id':self.channel_id,'parent_state_id':state.state_id})

def identity_channel(): return QuantumChannel(ChannelClass.IDENTITY,[], 'IDENTITY')
def hadamard_channel():
    s=1/math.sqrt(2); return QuantumChannel(ChannelClass.UNITARY,[[[s,s],[s,-s]]],'H')
def phase_flip_channel(): return QuantumChannel(ChannelClass.UNITARY,[[[1,0],[0,-1]]],'Z')
def dephasing_channel(p=0.5):
    if p<0 or p>1: raise ChannelValidationError('p range')
    a=math.sqrt(1-p); b=math.sqrt(p)
    I=[[a,0],[0,a]]; Z=[[b,0],[0,-b]]
    return QuantumChannel(ChannelClass.DEPHASING,[I,Z],f'DEPHASE({p})')
''')
w(pkg+'/measurement.py', r'''
import random
from .state import ampvec,StateFactory
from .util import now_ns,digest
from .errors import MeasurementError

class MeasurementEngine:
    def __init__(self,ownership): self.ownership=ownership
    def measure_basis(self,state,token,rng=None):
        self.ownership.assert_owned(state.state_id,token)
        if not state.amplitudes: raise MeasurementError('reference basis measurement requires pure state')
        rng=rng or random.Random()
        probs=[abs(x)**2 for x in ampvec(state)]; x=rng.random(); c=0.0; idx=len(probs)-1
        for i,p in enumerate(probs):
            c+=p
            if x<=c: idx=i; break
        out=state.basis[idx]; self.ownership.consume(state.state_id,token,'MEASURED')
        amps=[0j]*len(probs); amps[idx]=1+0j
        post=StateFactory.pure(state.basis,amps,state.source_instance_id,state.canonical_mmo_id,state.members,{'measurement_parent':state.state_id,'outcome':out}); post.kind='MEASURED'
        rec={'kind':'MEASUREMENT_RECEIPT','measurement_id':digest({'state':state.state_id,'outcome':out,'index':idx}),'source_state_id':state.state_id,'post_state_id':post.state_id,'outcome':out,'outcome_index':idx,'probability':probs[idx],'classical_result':True,'timestamp_ns':now_ns()}
        return out,post,rec
''')
w(pkg+'/effects.py', r'''
from .model import Effect,StateKind
from .errors import EffectViolation,QuantumSectorViolation

EFFECT_RULES={
 Effect.SUPERPOSE.value: {'sector':'QFT','inputs':{'CLASSICAL','PURE'},'output':'PURE','consumes':False,'coherence':'CREATE'},
 Effect.ENTANGLE.value: {'sector':'QFT','inputs':{'PURE','JOINT'},'output':'JOINT','consumes':True,'coherence':'PRESERVE_OR_CREATE'},
 Effect.UNITARY.value: {'sector':'QFT','inputs':{'PURE','JOINT'},'output':'PURE_OR_JOINT','consumes':False,'coherence':'PRESERVE'},
 Effect.CHANNEL.value: {'sector':'QFT','inputs':{'PURE','JOINT','DENSITY','DECOHERED'},'output':'DENSITY_OR_PURE','consumes':False,'coherence':'DECLARED'},
 Effect.DEPHASE.value: {'sector':'QFT','inputs':{'PURE','JOINT','DENSITY'},'output':'DECOHERED','consumes':False,'coherence':'MAY_REDUCE'},
 Effect.MEASURE.value: {'sector':'QFT','inputs':{'PURE','JOINT'},'output':'MEASURED','consumes':True,'coherence':'DESTROY_ALLOWED'},
 Effect.QFT_PORTAL_TRANSPORT.value: {'sector':'QFT','inputs':{'PURE','JOINT','DENSITY','DECOHERED'},'output':'DECLARED_BY_CHANNEL','consumes':False,'coherence':'DECLARED'},
 Effect.STRUCTURAL_TRANSDUCE.value: {'sector':'ANY','inputs':{'ANY'},'output':'STRUCTURAL_VIEW','consumes':False,'coherence':'NOT_CLAIMED'},
}

class EffectChecker:
    def check(self,effect,state_kind,sector):
        e=effect.value if hasattr(effect,'value') else str(effect); r=EFFECT_RULES.get(e)
        if not r: return {'admitted':True,'effect':e,'rule':'UNSPECIALIZED'}
        if r['sector']!='ANY' and sector!=r['sector']: raise QuantumSectorViolation(f'{e} requires {r["sector"]}')
        if 'ANY' not in r['inputs'] and state_kind not in r['inputs']: raise EffectViolation(f'{e} rejects {state_kind}')
        return {'admitted':True,'effect':e,'rule':r}
''')
w(pkg+'/audit.py', r'''
from .state import diagnostics,pure_fidelity
from .entanglement import is_entangled_reference

def audit_transition(source,target,preservation):
    a,b=diagnostics(source),diagnostics(target); findings=[]
    if preservation.preserve_norm and source.amplitudes and target.amplitudes and abs((a['norm'] or 0)-(b['norm'] or 0))>1e-8: findings.append('norm drift')
    if preservation.preserve_trace and abs(a['trace']-b['trace'])>1e-8: findings.append('trace drift')
    if preservation.preserve_coherence and b['coherence_l1']+1e-8 < max(a['coherence_l1'],preservation.min_coherence): findings.append('coherence below preservation')
    fidelity=None
    if source.amplitudes and target.amplitudes and len(source.amplitudes)==len(target.amplitudes):
        fidelity=pure_fidelity(source,target)
        if fidelity+1e-8 < preservation.min_fidelity: findings.append('fidelity below threshold')
    if preservation.preserve_entanglement and is_entangled_reference(source) and not is_entangled_reference(target): findings.append('entanglement lost')
    return {'pass':not findings,'findings':findings,'source':a,'target':b,'fidelity':fidelity}
''')
w(pkg+'/ledger.py', r'''
import json
from pathlib import Path
class Ledger:
    def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
    def append(self,obj):
        with self.path.open('a',encoding='utf-8') as f:f.write(json.dumps(obj,sort_keys=True,default=str)+'\n')
''')
w(pkg+'/portal.py', r'''
from dataclasses import asdict
from .model import QuantumEffectEnvelope,QuantumPreservation
from .effects import EffectChecker
from .audit import audit_transition
from .util import digest,now_ns
from .errors import QuantumSectorViolation,QuantumClosureError

class QuantumPortalEngine:
    def __init__(self,ownership,ledger=None): self.ownership=ownership; self.effects=EffectChecker(); self.ledger=ledger
    def transport(self,state,envelope,channel,ordinary_portal_receipt=None):
        if state.sector!='QFT': raise QuantumSectorViolation('quantum transport requires QFT state')
        if envelope.source_address.get('sector')!='QFT' or envelope.target_address.get('sector')!='QFT': raise QuantumSectorViolation('Portal<QFT> required')
        self.ownership.assert_owned(state.state_id,envelope.ownership_token)
        self.effects.check('QFT_PORTAL_TRANSPORT',state.kind,'QFT')
        target=channel.apply(state)
        audit=audit_transition(state,target,envelope.preservation)
        if not audit['pass']: raise QuantumClosureError(str(audit['findings']))
        moved=self.ownership.move(state.state_id,envelope.ownership_token,'PORTAL:'+envelope.target_address.get('domain_id','target'))
        newown=self.ownership.claim(target,moved.owner)
        # old semantic state handle is consumed after channel result owns successor.
        self.ownership.consume(state.state_id,moved.token,'PORTAL_SUCCESSOR_CREATED')
        rec={'kind':'QUANTUM_PORTAL_CLOSURE_RECEIPT','status':'CLOSED','quantum_portal_id':digest({'source':state.state_id,'target':target.state_id,'channel':channel.channel_id,'src':envelope.source_address,'dst':envelope.target_address}),'source_state_id':state.state_id,'target_state_id':target.state_id,'channel_id':channel.channel_id,'channel_class':channel.channel_class,'source_address':envelope.source_address,'target_address':envelope.target_address,'source_instance_id':state.source_instance_id,'canonical_mmo_id':state.canonical_mmo_id,'preservation':asdict(envelope.preservation),'audit':audit,'ordinary_portal_receipt_id':(ordinary_portal_receipt or {}).get('portal_id'),'target_ownership_token':newown.token,'entanglement_relation_ids':list(envelope.entanglement_relation_ids),'physics_status':'SOFTWARE_REFERENCE_QUANTUM_INFORMATION_TRANSPORT','timestamp_ns':now_ns()}
        if self.ledger:self.ledger.append(rec)
        return target,newown,rec
''')
w(pkg+'/bridge_policy.py', r'''
from dataclasses import dataclass
from .errors import BridgeQuantumBoundaryError
from .util import digest,now_ns

@dataclass
class StructuralInvariantCapsule:
    canonical_mmo_id:str
    source_instance_id:str
    content_root:str
    residue_root:str
    representation_id:str
    common_ancestry_witness:str
    provenance_refs:list

class QuantumBridgePolicy:
    def require_structural_only(self,state,bridge_receipt):
        if state.kind in ('PURE','JOINT','DENSITY','DECOHERED'):
            return {'admitted':True,'quantum_state_preserved':False,'policy':'STRUCTURAL_ONLY','reason':'Section 06 bridge is not typed as quantum channel'}
        return {'admitted':True,'quantum_state_preserved':False,'policy':'STRUCTURAL_ONLY'}
    def assert_preserve_quantum(self,state,bridge_receipt):
        raise BridgeQuantumBoundaryError('QFT/GR structural bridge does not establish quantum-coherence preservation')
    def capsule(self,instance,bridge_receipt):
        ca=bridge_receipt.get('common_ancestry',{})
        return StructuralInvariantCapsule(instance.get('canonical_mmo_id'),instance.get('instance_id'),bridge_receipt.get('source_content_root'),bridge_receipt.get('source_residue_root'),instance.get('representation_id'),ca.get('fabric_witness_id') or bridge_receipt.get('fabric_witness_id'),[bridge_receipt.get('bridge_id')])
''')
w(pkg+'/brane.py', r'''
from dataclasses import asdict
class QuantumEffectBraneAdapter:
    def adapt(self,instance,state,receipts):
        base=dict(instance.get('brane_m5') or {})
        base.setdefault('I',{}).update({'quantum_state_id':state.state_id,'canonical_mmo_id':state.canonical_mmo_id})
        base.setdefault('D',{}).update({'quantum_receipt_ids':[r.get('quantum_portal_id') or r.get('measurement_id') for r in receipts if isinstance(r,dict)]})
        base.setdefault('Chi',{}).update({'quantum_sector':'QFT','state_kind':state.kind})
        base.setdefault('R',{}).update({'quantum_effect_count':len(receipts),'quantum_state_members':list(state.members)})
        base.setdefault('P',{}).update({'quantum_effect_receipts':receipts})
        return base
''')
w('12_REFERENCE_IMPLEMENTATION/README.md', r'''
# Reference implementation
`genesis_quantum_effects` is a small, dependency-free Python execution oracle for Section 07 semantics.

It intentionally supports only finite-dimensional reference cases. It is not intended as a high-performance quantum simulator and is not a claim of physical quantum execution.

The package vendors Section 06's reference implementation so future Genesis compiler work can test quantum effects against the established Portal/Rainbow Road/QFT-GR stack.
''')

# vendor Section06 reference implementation
src=Path('/mnt/data/GENESIS_CHIRALITY_MACHINE_SECTION_06_QFT_GR_TRANSDUCTION_v0.1.0_20260821/12_REFERENCE_IMPLEMENTATION')
dst=ROOT/'12_REFERENCE_IMPLEMENTATION/vendor_section06'
if dst.exists(): shutil.rmtree(dst)
shutil.copytree(src,dst)

# Schemas
j('13_SCHEMAS/quantum_state.schema.json',{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Genesis Quantum Information State","type":"object","required":["state_id","kind","basis","sector"],"properties":{"state_id":{"type":"string"},"kind":{"enum":["CLASSICAL","PURE","DENSITY","JOINT","MEASURED","DECOHERED","CONSUMED"]},"basis":{"type":"array","items":{"type":"string"}},"amplitudes":{"type":"array"},"density":{"type":"array"},"members":{"type":"array","items":{"type":"string"}},"source_instance_id":{"type":["string","null"]},"canonical_mmo_id":{"type":["string","null"]},"sector":{"const":"QFT"}}})
j('13_SCHEMAS/quantum_effect_envelope.schema.json',{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Quantum Effect Envelope","type":"object","required":["state_id","channel_class","channel_id","ownership_token","source_address","target_address","preservation"],"properties":{"state_id":{"type":"string"},"channel_class":{"type":"string"},"channel_id":{"type":"string"},"ownership_token":{"type":"string"},"source_address":{"type":"object"},"target_address":{"type":"object"},"preservation":{"type":"object"}}})
j('13_SCHEMAS/quantum_portal_receipt.schema.json',{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Quantum Portal Receipt","type":"object","required":["kind","status","source_state_id","target_state_id","channel_id","audit"],"properties":{"kind":{"const":"QUANTUM_PORTAL_CLOSURE_RECEIPT"},"status":{"const":"CLOSED"},"source_state_id":{"type":"string"},"target_state_id":{"type":"string"},"channel_id":{"type":"string"},"audit":{"type":"object"}}})
j('13_SCHEMAS/measurement_receipt.schema.json',{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Measurement Receipt","type":"object","required":["measurement_id","source_state_id","post_state_id","outcome","probability"],"properties":{"measurement_id":{"type":"string"},"source_state_id":{"type":"string"},"post_state_id":{"type":"string"},"outcome":{"type":"string"},"probability":{"type":"number","minimum":0,"maximum":1}}})
j('13_SCHEMAS/structural_invariant_capsule.schema.json',{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Structural Invariant Capsule","type":"object","required":["canonical_mmo_id","source_instance_id","content_root","residue_root"],"properties":{"canonical_mmo_id":{"type":"string"},"source_instance_id":{"type":"string"},"content_root":{"type":"string"},"residue_root":{"type":"string"},"representation_id":{"type":"string"},"common_ancestry_witness":{"type":["string","null"]}}})

w('14_PSEUDOCODE/QUANTUM_PORTAL_EXECUTE.txt', r'''
QUANTUM_PORTAL_EXECUTE(state, envelope, channel):
    require state.sector == QFT
    require envelope source and target sectors == QFT
    require unique live ownership token
    validate effect QFT_PORTAL_TRANSPORT
    validate channel class
    target_state := channel(state)
    audit norm/trace/coherence/fidelity/entanglement contract
    if audit fails: reject closure
    move/consume source ownership
    allocate ownership of target_state
    emit Quantum Portal Closure Receipt
    attach receipt to history/provenance/BRANE M5
    return target_state
''')
w('14_PSEUDOCODE/MEASURE.txt', r'''
MEASURE(state, owner_token, observable/basis):
    require unique live ownership
    calculate outcome probabilities
    sample outcome
    consume coherent parent handle
    construct normalized measured successor
    emit classical result + Measurement Receipt
    classical result may now be copied
    return (outcome, measured_successor, receipt)
''')
w('14_PSEUDOCODE/ENTANGLE.txt', r'''
ENTANGLE(A, B):
    require QFT semantics
    require unique ownership of A and B
    move/consume component ownership into joint relationship
    construct JOINT state over tensor basis
    register entanglement relation
    do not expose independent pure member state
    return joint_state
''')
w('14_PSEUDOCODE/QFT_GR_BOUNDARY.txt', r'''
CROSS_QFT_GR(state, bridge):
    if request says preserve live quantum coherence/entanglement:
        reject: bridge is structural transduction, not quantum channel
    choose:
        measure/classicalize before bridge
        OR construct StructuralInvariantCapsule and bridge structural information
        OR use future explicitly registered quantum bridge channel
''')

w('15_FAILURES/FAILURE_TAXONOMY.md', r'''
# Section 07 failure taxonomy

- `STATE_NOT_NORMALIZED`
- `DENSITY_TRACE_VIOLATION`
- `DENSITY_HERMITICITY_VIOLATION`
- `QUANTUM_STATE_ALREADY_OWNED`
- `QUANTUM_STATE_CONSUMED`
- `NO_CLONING_VIOLATION`
- `EFFECT_TYPESTATE_VIOLATION`
- `QUANTUM_SECTOR_VIOLATION`
- `INVALID_UNITARY`
- `INVALID_KRAUS_CHANNEL`
- `COHERENCE_CONTRACT_FAILED`
- `FIDELITY_CONTRACT_FAILED`
- `ENTANGLEMENT_CONTRACT_FAILED`
- `MEASUREMENT_EFFECT_REQUIRED`
- `QFT_GR_QUANTUM_PRESERVATION_UNTYPED`
- `QUANTUM_PORTAL_CLOSURE_FAILED`

Failures are typed execution outcomes; they must not be converted to silent projection or fallback behavior.
''')

# Tests
w('16_TESTS/TEST_MATRIX.md', r'''
# Test matrix

The Section 07 test suite covers pure-state normalization, density validation, superposition, coherence, unitary validation, dephasing, Kraus trace preservation, fidelity, Bell-state entanglement, reduced-state purity, linear ownership, move/borrow, no-cloning, measurement consumption, deterministic measurement, effect typing, QFT-only Portal enforcement, quantum Portal closure, preservation failures, bridge structural-only policy, explicit rejection of quantum-preserving QFT/GR bridge claims, structural invariant capsules, and BRANE M5 effect lift.
''')
w('16_TESTS/test_section07.py', r'''
import unittest,math,random,sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'12_REFERENCE_IMPLEMENTATION'))
from genesis_quantum_effects import *
from genesis_quantum_effects.superposition import superpose
from genesis_quantum_effects.entanglement import bell_pair,reduced_two_level,is_entangled_reference,tensor_product
from genesis_quantum_effects.channels import *
from genesis_quantum_effects.state import diagnostics,pure_fidelity,StateFactory
from genesis_quantum_effects.linalg import trace,purity
from genesis_quantum_effects.measurement import MeasurementEngine
from genesis_quantum_effects.effects import EffectChecker
from genesis_quantum_effects.audit import audit_transition
from genesis_quantum_effects.portal import QuantumPortalEngine
from genesis_quantum_effects.bridge_policy import QuantumBridgePolicy
from genesis_quantum_effects.brane import QuantumEffectBraneAdapter
from genesis_quantum_effects.ledger import Ledger
from genesis_quantum_effects.errors import *

class T(unittest.TestCase):
    def q0(self): return StateFactory.pure(['0','1'],[1,0],source_instance_id='I',canonical_mmo_id='M')
    def qp(self): return StateFactory.pure(['0','1'],[1,1],source_instance_id='I',canonical_mmo_id='M')
    def test_01_normalize(self): self.assertAlmostEqual(diagnostics(self.qp())['norm'],1)
    def test_02_zero_norm(self):
        with self.assertRaises(NormalizationError): StateFactory.pure(['0'],[0])
    def test_03_density_trace(self): self.assertAlmostEqual(diagnostics(StateFactory.density(['0','1'],[[.5,0],[0,.5]]))['trace'],1)
    def test_04_density_bad_trace(self):
        with self.assertRaises(NormalizationError): StateFactory.density(['0','1'],[[1,0],[0,1]])
    def test_05_density_bad_hermitian(self):
        with self.assertRaises(StateValidationError): StateFactory.density(['0','1'],[[.5,.2],[.1,.5]])
    def test_06_superposition(self): self.assertGreater(diagnostics(self.qp())['coherence_l1'],0)
    def test_07_hadamard(self):
        out=hadamard_channel().apply(self.q0()); self.assertAlmostEqual(abs(complex(*out.amplitudes[0]))**2,.5)
    def test_08_unitary_invalid(self):
        with self.assertRaises(ChannelValidationError): QuantumChannel(ChannelClass.UNITARY,[[[1,1],[0,1]]])
    def test_09_dephase_trace(self): self.assertAlmostEqual(diagnostics(dephasing_channel(.5).apply(self.qp()))['trace'],1)
    def test_10_dephase_coherence(self): self.assertLess(diagnostics(dephasing_channel(.5).apply(self.qp()))['coherence_l1'],diagnostics(self.qp())['coherence_l1']+1e-9)
    def test_11_fidelity_self(self): self.assertAlmostEqual(pure_fidelity(self.qp(),self.qp()),1)
    def test_12_bell(self): self.assertTrue(is_entangled_reference(bell_pair('A','B')))
    def test_13_reduced_mixed(self):
        r=reduced_two_level(bell_pair('A','B')); self.assertAlmostEqual(purity(r),.5)
    def test_14_tensor_product(self): self.assertEqual(len(tensor_product(self.q0(),self.q0(),['A','B']).basis),4)
    def test_15_claim(self):
        R=LinearOwnershipRegistry(); q=self.q0(); rec=R.claim(q,'A'); self.assertEqual(rec.owner,'A')
    def test_16_double_claim(self):
        R=LinearOwnershipRegistry(); q=self.q0(); R.claim(q,'A')
        with self.assertRaises(OwnershipError): R.claim(q,'B')
    def test_17_borrow(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A'); R.borrow_metadata(q.state_id,r.token); self.assertEqual(R.records[q.state_id].status,'OWNED')
    def test_18_move(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A'); r2=R.move(q.state_id,r.token,'B'); self.assertEqual(r2.owner,'B')
    def test_19_no_clone(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A')
        with self.assertRaises(NoCloningError): R.clone(q,r.token)
    def test_20_consumed(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A'); R.consume(q.state_id,r.token)
        with self.assertRaises(ConsumedStateError): R.assert_owned(q.state_id,r.token)
    def test_21_measure(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A'); out,post,rec=MeasurementEngine(R).measure_basis(q,r.token,random.Random(1)); self.assertEqual(out,'0'); self.assertEqual(post.kind,'MEASURED')
    def test_22_measure_consumes(self):
        R=LinearOwnershipRegistry(); q=self.q0(); r=R.claim(q,'A'); MeasurementEngine(R).measure_basis(q,r.token,random.Random(1)); self.assertEqual(R.records[q.state_id].status,'CONSUMED')
    def test_23_effect_qft(self): self.assertTrue(EffectChecker().check(Effect.UNITARY,'PURE','QFT')['admitted'])
    def test_24_effect_gr_reject(self):
        with self.assertRaises(QuantumSectorViolation): EffectChecker().check(Effect.UNITARY,'PURE','GR')
    def test_25_effect_typestate_reject(self):
        with self.assertRaises(EffectViolation): EffectChecker().check(Effect.UNITARY,'MEASURED','QFT')
    def test_26_audit_identity(self): self.assertTrue(audit_transition(self.q0(),self.q0(),QuantumPreservation(min_fidelity=1))['pass'])
    def test_27_audit_fidelity_fail(self):
        q1=StateFactory.pure(['0','1'],[0,1]); self.assertFalse(audit_transition(self.q0(),q1,QuantumPreservation(min_fidelity=.9))['pass'])
    def test_28_quantum_portal(self):
        R=LinearOwnershipRegistry(); q=self.q0(); own=R.claim(q,'SRC'); env=QuantumEffectEnvelope(q.state_id,'IDENTITY','id',own.token,{'sector':'QFT','domain_id':'A'},{'sector':'QFT','domain_id':'B'},QuantumPreservation(min_fidelity=1)); t,o,rec=QuantumPortalEngine(R).transport(q,env,identity_channel()); self.assertEqual(rec['status'],'CLOSED')
    def test_29_quantum_portal_gr_reject(self):
        R=LinearOwnershipRegistry(); q=self.q0(); own=R.claim(q,'SRC'); env=QuantumEffectEnvelope(q.state_id,'IDENTITY','id',own.token,{'sector':'QFT','domain_id':'A'},{'sector':'GR','domain_id':'B'})
        with self.assertRaises(QuantumSectorViolation): QuantumPortalEngine(R).transport(q,env,identity_channel())
    def test_30_quantum_portal_coherence_fail(self):
        R=LinearOwnershipRegistry(); q=self.qp(); own=R.claim(q,'SRC'); env=QuantumEffectEnvelope(q.state_id,'DEPHASING','d',own.token,{'sector':'QFT','domain_id':'A'},{'sector':'QFT','domain_id':'B'},QuantumPreservation(preserve_coherence=True,min_coherence=diagnostics(q)['coherence_l1']))
        with self.assertRaises(QuantumClosureError): QuantumPortalEngine(R).transport(q,env,dephasing_channel(.5))
    def test_31_bridge_policy_structural(self): self.assertFalse(QuantumBridgePolicy().require_structural_only(self.q0(),{})['quantum_state_preserved'])
    def test_32_bridge_quantum_reject(self):
        with self.assertRaises(BridgeQuantumBoundaryError): QuantumBridgePolicy().assert_preserve_quantum(self.q0(),{})
    def test_33_capsule(self):
        inst={'canonical_mmo_id':'M','instance_id':'I','representation_id':'R'}; br={'source_content_root':'C','source_residue_root':'RR','bridge_id':'B','fabric_witness_id':'F'}; c=QuantumBridgePolicy().capsule(inst,br); self.assertEqual(c.content_root,'C')
    def test_34_brane(self):
        inst={'canonical_mmo_id':'M','brane_m5':{}}; q=self.q0(); b=QuantumEffectBraneAdapter().adapt(inst,q,[{'measurement_id':'m'}]); self.assertEqual(b['Chi']['quantum_sector'],'QFT')
    def test_35_channel_id_stable(self): self.assertEqual(hadamard_channel().channel_id,hadamard_channel().channel_id)
    def test_36_bell_norm(self): self.assertAlmostEqual(diagnostics(bell_pair('A','B'))['norm'],1)
    def test_37_dephase_purity(self): self.assertLessEqual(diagnostics(dephasing_channel(.5).apply(self.qp()))['purity'],1+1e-9)
    def test_38_measure_probability(self):
        R=LinearOwnershipRegistry(); q=self.q0(); own=R.claim(q,'A'); _,_,rec=MeasurementEngine(R).measure_basis(q,own.token,random.Random(2)); self.assertAlmostEqual(rec['probability'],1)
    def test_39_structural_transduce_any(self): self.assertTrue(EffectChecker().check(Effect.STRUCTURAL_TRANSDUCE,'PURE','GR')['admitted'])
    def test_40_joint_kind(self): self.assertEqual(bell_pair('A','B').kind,'JOINT')

if __name__=='__main__': unittest.main()
''')

j('17_EXAMPLES/SUPERPOSITION_EXAMPLE.json',{"kind":"GENESIS_QUANTUM_EXAMPLE","operation":"SUPERPOSE","basis":["route:red-orange","route:red-violet"],"amplitudes":[[0.7071067811865476,0],[0.7071067811865476,0]],"note":"Semantic route superposition example only; not a claim that current Rainbow Road hardware implements coherent path superposition."})
j('17_EXAMPLES/ENTANGLEMENT_EXAMPLE.json',{"kind":"GENESIS_QUANTUM_EXAMPLE","operation":"ENTANGLE","members":["MMO_A:view","MMO_B:view"],"state":"(|00>+|11>)/sqrt(2)","rule":"relationship is not transportation; Portal remains required for controllable payload transfer"})
j('17_EXAMPLES/QUANTUM_PORTAL_EXAMPLE.json',{"kind":"QUANTUM_PORTAL_REQUEST_EXAMPLE","source":{"domain_id":"RED","sector":"QFT"},"target":{"domain_id":"GREEN","sector":"QFT"},"channel":"IDENTITY","preserve":{"norm":True,"trace":True,"coherence":True,"entanglement":False}})

w('18_SOURCE_CROSSWALK/SOURCE_CROSSWALK.md', r'''
# Source crosswalk

## Source-backed inputs

- **MK Ultra Tome, Volume VI**: quantum state spaces, probability, quantization, measurement/readable quantum structure.
- **MK Ultra Tome, Volume XIII**: holography and information transfer, tensor networks/error correction, information conservation across projections.
- **MK Ultra foundational information chapter**: information flow requires a channel, propagation law, and recoverability criterion; quantum density/projector mathematics is treated as established external mathematics at the interface.
- **QFT/GR Bridge v1**: QFT and GR are representation sectors with common chirality ancestry; the bridge is a transduction architecture rather than whole-object identity.
- **Astraeus books**: Transduction Geometry, Bandwidth Algebra, Resolution & Readout, Identity Through History, Holonomy & Chirality.
- **Sections 04–06**: Portal, Corridor, Rainbow Road, and explicit sector transduction execution contracts.

## Section 07 design additions

Linear ownership, the finite-dimensional Python simulator, channel/effect classes, and the explicit quantum-Portal envelope are **implementation design choices** informed by established quantum programming practice. They are not claimed as recovered MK Ultra axioms.
''')
j('18_SOURCE_CROSSWALK/SOURCE_REGISTRY.json',{
"sources":[
{"name":"MK Ultra Tome","path":"/mnt/data/MK Ultra(2).pdf","role":"quantum/information architecture"},
{"name":"QFT-GR Bridge v1","path":"/mnt/data/1.0 | QFT - GR BRIDGE(1).zip","role":"sector/common-chirality transduction"},
{"name":"Section 06 core","path":"/mnt/data/GENESIS_CHIRALITY_MACHINE_SECTION_06_QFT_GR_TRANSDUCTION_v0.1.0_20260821_PART_A_CORE.zip","role":"parent execution layer"},
{"name":"MK43 Tome information live model","path":"/mnt/data/BLACKGLASS_ACTIVE_MOUNT_20260821/LIVE_MODELS/MK43_TOME_QFT_GR_INFORMATION/LIVE/MK43_TOME_QFT_GR_INFORMATION_LIVE_MODEL_v0.1.md","role":"targeted source interpretation"}
],"status_rule":"source-derived, established mathematics, and Section-07 design additions remain labeled separately"})

w('19_RECOVERY/SECTION_07_STATE.md', r'''
# Section 07 recovery state

**Status:** IMPLEMENTED SOFTWARE REFERENCE

Section 07 adds quantum-information typestate/effect semantics above Section 06.

Recovery invariants:

- quantum state is optional QFT-sector representation, not the chirality fabric itself;
- nonclassical state ownership is linear in the language/runtime model;
- no-cloning is enforced at the handle layer;
- entanglement is joint relationship, not transport;
- measurement is explicit and classicalizes an outcome;
- Portal<QFT> may carry a declared quantum channel/effect envelope;
- QFT/GR bridge is structural-only with respect to quantum coherence until a future explicit quantum bridge channel is typed;
- BRANE remains six-dimensional with M5 organizational contract plus realization Z;
- all current quantum execution is software reference simulation.

Next natural section: Section 08 — Genesis VM / IR instruction model, lowering Sections 01–07 into a compact machine-facing intermediate representation.
''')

# build reference integration runs
sys.path.insert(0,str(ROOT/'12_REFERENCE_IMPLEMENTATION'))
from genesis_quantum_effects.state import StateFactory, diagnostics, pure_fidelity
from genesis_quantum_effects.linear import LinearOwnershipRegistry
from genesis_quantum_effects.channels import identity_channel,hadamard_channel,dephasing_channel
from genesis_quantum_effects.measurement import MeasurementEngine
from genesis_quantum_effects.entanglement import bell_pair,is_entangled_reference,reduced_two_level
from genesis_quantum_effects.model import QuantumEffectEnvelope,QuantumPreservation
from genesis_quantum_effects.portal import QuantumPortalEngine
from genesis_quantum_effects.bridge_policy import QuantumBridgePolicy
from genesis_quantum_effects.brane import QuantumEffectBraneAdapter

# use known real MMO ids from prior sections as identity anchors; no physical quantum claim.
fixtures=[
 ('HSV1','HSV1-REFERENCE-MMO-QMODEL-01','dd7fb7fa4d53f5695e4c8788de131877'),
 ('HYDROGEN','H:HYDROGEN_V2','217fc789e846f8e268f9cb627fa7faa2'),
 ('OXYGEN','O:OXYGEN_PHASE5_V1','640e97db2023233927e5a18d61763296'),
 ('BLANK','BLANK_MANIFOLD_V0_1','3ea26902ff4719fa2d1b65a44c1508d')]
runs=[]
for label,mmo,inst in fixtures:
    q=StateFactory.pure(['branch0','branch1'],[1,1],inst,mmo,metadata={'fixture_label':label})
    ownreg=LinearOwnershipRegistry(); own=ownreg.claim(q,label+':source')
    env=QuantumEffectEnvelope(q.state_id,'IDENTITY','IDENTITY',own.token,{'domain_id':'RED','sector':'QFT'},{'domain_id':'GREEN','sector':'QFT'},QuantumPreservation(True,True,True,False,1.0,0.0),metadata={'fixture':label})
    tgt,town,receipt=QuantumPortalEngine(ownreg).transport(q,env,identity_channel())
    bell=bell_pair(label+':A',label+':B',inst,mmo)
    red=reduced_two_level(bell)
    # independent measurement run
    qm=StateFactory.pure(['0','1'],[1,1],inst,mmo); rm=LinearOwnershipRegistry(); om=rm.claim(qm,label+':measure'); outcome,post,mrec=MeasurementEngine(rm).measure_basis(qm,om.token,random.Random(7))
    result={'label':label,'canonical_mmo_id':mmo,'source_instance_id':inst,'quantum_state_id':q.state_id,'portal_target_state_id':tgt.state_id,'portal_closed':receipt['status']=='CLOSED','identity_channel_fidelity':receipt['audit']['fidelity'],'coherence_preserved':receipt['audit']['target']['coherence_l1']>=receipt['audit']['source']['coherence_l1']-1e-8,'bell_reference_entangled':is_entangled_reference(bell),'bell_reduced_purity':float((red[0][0]*red[0][0]+red[0][1]*red[1][0]+red[1][0]*red[0][1]+red[1][1]*red[1][1]).real),'measurement_outcome':outcome,'measurement_probability':mrec['probability'],'bridge_quantum_policy':QuantumBridgePolicy().require_structural_only(q,{}),'physics_status':'SOFTWARE_REFERENCE_ONLY'}
    runs.append(result)
    j(f'20_REFERENCE_QUANTUM_INFORMATION_RUNS/{label}_RUN.json',result)
j('20_REFERENCE_QUANTUM_INFORMATION_RUNS/INTEGRATION_RESULTS.json',runs)

# run tests
cmd=[sys.executable,str(ROOT/'16_TESTS/test_section07.py')]
p=subprocess.run(cmd,capture_output=True,text=True)
(ROOT/'99_RELEASE/TEST_RESULTS.txt').write_text(p.stdout+p.stderr,encoding='utf-8')
if p.returncode!=0:
    print(p.stdout,p.stderr); raise SystemExit('tests failed')
# Count tests from output
w('99_RELEASE/INTEGRATION_TEST_RESULTS.txt', f"reference_fixture_runs={len(runs)}\nall_pass={all(x['portal_closed'] and x['coherence_preserved'] and x['bell_reference_entangled'] for x in runs)}\n")

# Build script copy
shutil.copy2('/mnt/data/_build_section07.py', ROOT/'98_BUILD/_build_section07.py')

# manifests/checksums core
files=[p for p in ROOT.rglob('*') if p.is_file() and '99_RELEASE/CORE_' not in str(p)]
manifest=[]; checks=[]
for pth in sorted(files):
    rel=str(pth.relative_to(ROOT)); data=pth.read_bytes(); h=hashlib.sha256(data).hexdigest(); manifest.append({'path':rel,'bytes':len(data),'sha256':h}); checks.append(f'{h}  {rel}')
j('99_RELEASE/CORE_MANIFEST.json',{'package':ROOT.name,'version':'0.1.0','file_count':len(manifest),'files':manifest})
w('99_RELEASE/CORE_CHECKSUMS.sha256','\n'.join(checks)+'\n')
print(ROOT)
print((ROOT/'99_RELEASE/TEST_RESULTS.txt').read_text())
