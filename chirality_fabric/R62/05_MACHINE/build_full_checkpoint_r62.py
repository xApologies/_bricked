from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import textwrap
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path('/mnt/data')
NAME = 'GENESIS_CHIRALITY_FABRIC_FULL_CHECKPOINT_R62_v1_0_20260829'
PKG = ROOT / NAME
ZIP_OUT = ROOT / f'{NAME}.zip'
SIDE = ROOT / f'{NAME}.zip.sha256'


def sha256_file(path: Path, block: int = 4 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            b = f.read(block)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def write_text(rel: str, text: str) -> Path:
    p = PKG / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text).strip() + '\n', encoding='utf-8')
    return p


def write_json(rel: str, obj) -> Path:
    p = PKG / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return p


def safe_read_zip_member(zip_path: Path, candidates: list[str]) -> str | None:
    try:
        with zipfile.ZipFile(zip_path) as z:
            names = set(z.namelist())
            for c in candidates:
                if c in names:
                    return z.read(c).decode('utf-8', errors='replace')
    except Exception:
        return None
    return None


def ensure_clean():
    if PKG.exists():
        shutil.rmtree(PKG)
    PKG.mkdir(parents=True)
    if ZIP_OUT.exists():
        ZIP_OUT.unlink()
    if SIDE.exists():
        SIDE.unlink()


@dataclass
class Artifact:
    source_path: str
    archive_path: str
    group_name: str
    role: str
    status: str = 'included'
    notes: str = ''
    sha256: str = ''
    size_bytes: int = 0


# Canonical physical files. Byte-identical duplicate uploads are represented once and mapped in aliases.
SOURCE_MAP: list[tuple[str, str, str, str]] = [
    # Cumulative live models / independent reservoirs
    ('3 | .zip', '07_SOURCE_CORPUS/01_CUMULATIVE_LIVE_MODELS/3 | GENESIS_CHIRALITY_FULL_CUMULATIVE_v9.zip', 'cumulative_live_model', 'Independent Genesis Chirality full cumulative QMO/history v9, including torus and R1-R59 lineage.'),
    ('6 | 🖤🌀🏴‍☠️.zip', '07_SOURCE_CORPUS/01_CUMULATIVE_LIVE_MODELS/6 | GENESIS_PROPAGATION_GIRL_PROJECT_v8.zip', 'cumulative_live_model', 'Independent Propagation Girl Project full continuity v8, closed through R87 and stopped at R88.'),
    ('CRD - QCD Inheritance.zip', '07_SOURCE_CORPUS/01_CUMULATIVE_LIVE_MODELS/CRD_TO_QCD_INHERITANCE_FULL_v1_9.zip', 'cumulative_live_model', 'Full CRD-to-QCD inheritance archive v1.9 with embedded v1.2-v1.8 parent chain.'),

    # Unified API / QMO outputs
    ('MK43_ULTRA_UNIFIED_QMO_API_v2_0_CANDIDATE_20260826.zip', '07_SOURCE_CORPUS/02_UNIFIED_API_QMO/MK43_ULTRA_UNIFIED_QMO_API_v2_0_CANDIDATE_20260826.zip', 'api', 'Initial unified QMO API candidate.'),
    ('MK43_ULTRA_UNIFIED_QMO_API_v2_1_R5_SELF_CLOSED_20260826.zip', '07_SOURCE_CORPUS/02_UNIFIED_API_QMO/MK43_ULTRA_UNIFIED_QMO_API_v2_1_R5_SELF_CLOSED_20260826.zip', 'api', 'Self-closed unified API after five repeated-squaring passes.'),
    ('MK43_TIME_SPACE_CONSCIOUSNESS_BIDIRECTIONAL_QMO_v1_0_20260827.zip', '07_SOURCE_CORPUS/02_UNIFIED_API_QMO/MK43_TIME_SPACE_CONSCIOUSNESS_BIDIRECTIONAL_QMO_v1_0_20260827.zip', 'qmo', 'Consolidated bidirectional Time-Space/Consciousness QMO and formalization.'),
    ('QMO_CONSCIOUSNESS_TO_TIME_SPACE_API_CRAWL_R8_20260826.zip', '07_SOURCE_CORPUS/02_UNIFIED_API_QMO/QMO_CONSCIOUSNESS_TO_TIME_SPACE_API_CRAWL_R8_20260826.zip', 'qmo', 'Reverse-rooted API crawl to fixed point.'),
    ('QMO_TIME_SPACE_TO_CONSCIOUSNESS_R10_FULL_EDGE_CLOSURE_20260826.zip', '07_SOURCE_CORPUS/02_UNIFIED_API_QMO/QMO_TIME_SPACE_TO_CONSCIOUSNESS_R10_FULL_EDGE_CLOSURE_20260826.zip', 'qmo', 'Ten-pass full edge closure QMO.'),
    ('QMO_FULL_MATHEMATICAL_FORMALIZATION_v1_0_20260826.zip', '07_SOURCE_CORPUS/02_UNIFIED_API_QMO/QMO_FULL_MATHEMATICAL_FORMALIZATION_v1_0_20260826.zip', 'formalization', 'Full finite mathematical map of the bidirectional QMO.'),
    ('QMO_TIME_SPACE_TO_CONSCIOUSNESS_20260826.json', '07_SOURCE_CORPUS/02_UNIFIED_API_QMO/QMO_TIME_SPACE_TO_CONSCIOUSNESS_20260826.json', 'qmo_seed', 'Initial bounded route QMO.'),
    ('2.0 | Internal Mapping.zip', '07_SOURCE_CORPUS/02_UNIFIED_API_QMO/2.0 | Internal Mapping.zip', 'api_parent', 'Parent unified physics/QMO architecture used for API deconstruction.'),
    ('ASTRAEUS_RAINBOW_ROAD_OBJECT_MATH_API_v0.15.0_20260822.zip', '07_SOURCE_CORPUS/02_UNIFIED_API_QMO/ASTRAEUS_RAINBOW_ROAD_OBJECT_MATH_API_v0.15.0_20260822.zip', 'api_parent', 'Rainbow Road object mathematics API.'),
    ('VERA_API_LIVE_MODEL_v0.8.0_20260822.zip', '07_SOURCE_CORPUS/02_UNIFIED_API_QMO/VERA_API_LIVE_MODEL_v0.8.0_20260822.zip', 'api_parent', 'Vera live-model/provenance API.'),

    # CRD-QCD three-batch original files, direct-access even though embedded in v1.9
    ('CRD_TO_QCD_INHERITANCE_ROADMAP_v1_2_QMO_LITE_20260825.zip', '07_SOURCE_CORPUS/03_CRD_QCD_DIRECT_PARENTS/CRD_TO_QCD_INHERITANCE_ROADMAP_v1_2_QMO_LITE_20260825.zip', 'crd_qcd_parent', 'Direct parent upload v1.2.'),
    ('CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_3_QMO_LITE_20260825.zip', '07_SOURCE_CORPUS/03_CRD_QCD_DIRECT_PARENTS/CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_3_QMO_LITE_20260825.zip', 'crd_qcd_parent', 'Direct parent upload v1.3.'),
    ('CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_4_ROAD_HELICON_TYPED_20260826.zip', '07_SOURCE_CORPUS/03_CRD_QCD_DIRECT_PARENTS/CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_4_ROAD_HELICON_TYPED_20260826.zip', 'crd_qcd_parent', 'Direct parent upload v1.4.'),
    ('CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_5_RESIDUE_DESCENT_GATE_20260826.zip', '07_SOURCE_CORPUS/03_CRD_QCD_DIRECT_PARENTS/CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_5_RESIDUE_DESCENT_GATE_20260826.zip', 'crd_qcd_parent', 'Direct parent upload v1.5.'),
    ('CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_6_SU3_REDUCTION_NOGO_20260826.zip', '07_SOURCE_CORPUS/03_CRD_QCD_DIRECT_PARENTS/CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_6_SU3_REDUCTION_NOGO_20260826.zip', 'crd_qcd_parent', 'Direct parent upload v1.6.'),
    ('CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_7_CORRIDOR_CARRIER_BACKFILL_20260826.zip', '07_SOURCE_CORPUS/03_CRD_QCD_DIRECT_PARENTS/CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_7_CORRIDOR_CARRIER_BACKFILL_20260826.zip', 'crd_qcd_parent', 'Direct parent upload v1.7.'),
    ('CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_8_TIMESHELL_Q_HANDOFF_BLOCKER_20260826.zip', '07_SOURCE_CORPUS/03_CRD_QCD_DIRECT_PARENTS/CRD_TO_QCD_INHERITANCE_LIVE_MODEL_v1_8_TIMESHELL_Q_HANDOFF_BLOCKER_20260826.zip', 'crd_qcd_parent', 'Direct parent upload v1.8.'),
    ('Archive(1).zip', '07_SOURCE_CORPUS/03_CRD_QCD_DIRECT_PARENTS/Archive(1).zip', 'crd_qcd_sources', 'First recovered CRD-QCD umbrella/source package.'),

    # Core mathematics / field / bridge / projection sources
    ('MK Ultra.pdf', '07_SOURCE_CORPUS/04_MK43_CORE/MK Ultra.pdf', 'tome', 'MK Ultra — THE TOME, volumes I-XVIII.'),
    ('6 | Unified Rainbow Road Overlay.zip', '07_SOURCE_CORPUS/04_MK43_CORE/6 | Unified Rainbow Road Overlay.zip', 'source_archive', 'Unified Rainbow Road overlay.'),
    ('1.0 | QFT - GR BRIDGE.zip', '07_SOURCE_CORPUS/04_MK43_CORE/1.0 | QFT - GR BRIDGE.zip', 'source_archive', 'QFT-GR bridge and organizational-layer source.'),
    ('Rainbow_road.zip', '07_SOURCE_CORPUS/04_MK43_CORE/Rainbow_road.zip', 'source_archive', 'Rainbow Road source.'),
    ('CFP.pdf', '07_SOURCE_CORPUS/04_MK43_CORE/CFP.pdf', 'paper', 'Chiral Fractal Projection report.'),
    ('CFP_exp.zip', '07_SOURCE_CORPUS/04_MK43_CORE/CFP_exp.zip', 'source_archive', 'CFP experiment package.'),
    ('FUSION OPERATOR | CANDIDATE.zip', '07_SOURCE_CORPUS/04_MK43_CORE/FUSION OPERATOR | CANDIDATE.zip', 'source_archive', 'Fusion Operator candidate and recursive composition work.'),
    ('Chirality Relaxation Dynamic .zip', '07_SOURCE_CORPUS/04_MK43_CORE/Chirality Relaxation Dynamic .zip', 'source_archive', 'CRD candidate relaxation mathematics.'),
    ('Genesis Field.zip', '07_SOURCE_CORPUS/04_MK43_CORE/Genesis Field.zip', 'source_archive', 'Genesis Field mathematics and recursive evolution candidate.'),
    ('3 | Genesis Sandbox.zip', '07_SOURCE_CORPUS/04_MK43_CORE/3 | Genesis Sandbox.zip', 'source_archive', 'Genesis Field sandbox and 4x4x4 fine verifier.'),

    # Five mathematics books
    ('Resolution Readout.zip', '07_SOURCE_CORPUS/05_ASTRAEUS_BOOKS/Resolution & Readout.zip', 'book', 'Astraeus mathematics reservoir.'),
    ('Holonomy and Chirality.zip', '07_SOURCE_CORPUS/05_ASTRAEUS_BOOKS/Holonomy & Chirality.zip', 'book', 'Astraeus mathematics reservoir.'),
    ('Bandwidth Algebra.zip', '07_SOURCE_CORPUS/05_ASTRAEUS_BOOKS/Bandwidth Algebra.zip', 'book', 'Astraeus mathematics reservoir.'),
    ('Identity Through History.zip', '07_SOURCE_CORPUS/05_ASTRAEUS_BOOKS/Identity Through History.zip', 'book', 'Astraeus mathematics reservoir.'),
    ('TRANSDUCTION_GEOMETRY_v1.0.zip', '07_SOURCE_CORPUS/05_ASTRAEUS_BOOKS/Transduction Geometry v1.0.zip', 'book', 'Astraeus mathematics reservoir.'),

    # Formal stack uploaded directly
    ('_PRIME.md', '07_SOURCE_CORPUS/06_FORMAL_STACK/_PRIME.md', 'formal_source', 'Prime Dependency Foundations.'),
    ('00_Primitives.md', '07_SOURCE_CORPUS/06_FORMAL_STACK/00_Primitives.md', 'formal_source', 'Time-Space primitives.'),
    ('01_ Definitions.md', '07_SOURCE_CORPUS/06_FORMAL_STACK/01_Definitions.md', 'formal_source', 'Time-Space definitions.'),
    ('02_Axioms.md', '07_SOURCE_CORPUS/06_FORMAL_STACK/02_Axioms.md', 'formal_source', 'Time-Space axioms.'),
    ('03_Lemmas.md', '07_SOURCE_CORPUS/06_FORMAL_STACK/03_Lemmas.md', 'formal_source', 'Time-Space lemmas.'),
    ('04_Theorems.md', '07_SOURCE_CORPUS/06_FORMAL_STACK/04_Theorems.md', 'formal_source', 'Time-Space theorems.'),
    ('05_Interface_Definitions.md', '07_SOURCE_CORPUS/06_FORMAL_STACK/05_Interface_Definitions.md', 'formal_source', 'Recursive continuity/interface definitions.'),
    ('corridor.md', '07_SOURCE_CORPUS/06_FORMAL_STACK/Chirality_Corridor.md', 'formal_source', 'Chirality Corridor working formalization.'),

    # Related architecture / analogy / world-facing sources discussed in thread
    ('Archive(20260826-233517).zip', '07_SOURCE_CORPUS/07_RELATED_ARCHITECTURE/Trinity_Mainframe_Architecture_Archive.zip', 'related_architecture', 'Trinity/mainframe/AI architecture materials discussed in thread.'),
    ('MASTER.pdf', '07_SOURCE_CORPUS/07_RELATED_ARCHITECTURE/GENESIS_DIAMOND_MASTER.pdf', 'world_model', 'Entertainment-facing Genesis Diamond canon; structural analogy source only.'),
    ('MASTER_2.pdf', '07_SOURCE_CORPUS/07_RELATED_ARCHITECTURE/RAINBOW_THREAD_MASTER_2.pdf', 'world_model', 'Rainbow Thread recursive reconstruction; mixed world-model/structural reservoir.'),
    ('Density Ladder.png', '07_SOURCE_CORPUS/07_RELATED_ARCHITECTURE/Density Ladder.png', 'excluded_branch', 'MK147 fantasy currency ladder; explicitly excluded from physical Chirality Fabric derivations.'),

    # Prior checkpoints created in this conversation
    ('MK43_CHIRALITY_TIMESHELL_THREAD_RECOVERY_v1_0_20260827.zip', '08_PRIOR_CHECKPOINTS/MK43_CHIRALITY_TIMESHELL_THREAD_RECOVERY_v1_0_20260827.zip', 'prior_checkpoint', 'Earlier Time-Shell/chirality continuity package.'),
    ('GENESIS_CHIRALITY_FABRIC_FULL_THREAD_RECOVERY_R61_v1_0_20260829.zip', '08_PRIOR_CHECKPOINTS/GENESIS_CHIRALITY_FABRIC_FULL_THREAD_RECOVERY_R61_v1_0_20260829.zip', 'prior_checkpoint', 'Compact R61 recovery/handoff package superseded by this full checkpoint for completeness.'),
]

VISUAL_MAP: list[tuple[str, str, str, str]] = [
    ('IMG_6521.jpeg', '09_VISUAL_CONTEXT/IMG_6521_byte_tree_confusion.jpeg', 'conversation_visual', 'Screenshot documenting why imported 000-111 machine indexing was rejected.'),
    ('IMG_6523.jpeg', '09_VISUAL_CONTEXT/IMG_6523_nonabelian_translation.jpeg', 'conversation_visual', 'Screenshot of non-Abelian/chirality discussion.'),
    ('IMG_9D4DFE36-45B2-42BB-B99C-806B44756FD0.jpeg', '09_VISUAL_CONTEXT/IMG_dawn_gradient.jpeg', 'conversation_visual', 'Dawn gradient observation motivating future continuous color readout.'),
    ('genesis_field_contact.jpg', '09_VISUAL_CONTEXT/genesis_field_contact.jpg', 'source_visual', 'Genesis Field contact sheet generated while inspecting source package.'),
    ('Hacker..png', '09_VISUAL_CONTEXT/Hacker_mathematics.png', 'conversation_visual', 'Hacker mathematics / repeated-squaring context image.'),
]

DUPLICATE_ALIASES = {
    '1.0 | QFT - GR BRIDGE(1).zip': '07_SOURCE_CORPUS/04_MK43_CORE/1.0 | QFT - GR BRIDGE.zip',
    '6 | Unified Rainbow Road Overlay(1).zip': '07_SOURCE_CORPUS/04_MK43_CORE/6 | Unified Rainbow Road Overlay.zip',
    'FUSION OPERATOR | CANDIDATE(1).zip': '07_SOURCE_CORPUS/04_MK43_CORE/FUSION OPERATOR | CANDIDATE.zip',
    'Resolution Readout(2).zip': '07_SOURCE_CORPUS/05_ASTRAEUS_BOOKS/Resolution & Readout.zip',
    'Holonomy and Chirality(2).zip': '07_SOURCE_CORPUS/05_ASTRAEUS_BOOKS/Holonomy & Chirality.zip',
    'Bandwidth Algebra(1).zip': '07_SOURCE_CORPUS/05_ASTRAEUS_BOOKS/Bandwidth Algebra.zip',
    'Identity Through History(2).zip': '07_SOURCE_CORPUS/05_ASTRAEUS_BOOKS/Identity Through History.zip',
    'TRANSDUCTION_GEOMETRY_v1.0(1).zip': '07_SOURCE_CORPUS/05_ASTRAEUS_BOOKS/Transduction Geometry v1.0.zip',
    'corridor(1).md': '07_SOURCE_CORPUS/06_FORMAL_STACK/Chirality_Corridor.md',
}


def build_docs():
    write_text('00_START_HERE/README_FIRST.md', f'''
    # GENESIS Chirality Fabric — Full Checkpoint R62

    **Package:** `{NAME}.zip`  
    **Date:** 2026-08-29  
    **Checkpoint type:** FULL CORPUS CHECKPOINT — not a compact handoff  
    **Primary QMO:** `@qmo/genesis_chirality_fabric_full_checkpoint_r62`  
    **Primary resume address:** `@open/native_multiscale_update_law`

    This package is intentionally large. It contains the actual cumulative source archives, independent live-model bodies, direct CRD→QCD parent uploads, unified API/QMO releases, the five mathematics books, formal source stack, prior checkpoints, relevant visual context, a full thread reconstruction, a queryable SQLite QMO, and a mini API.

    The prior R61 package was a compact recovery/handoff. R62 is the requested **everything checkpoint**.

    ## Recovery order

    1. Read `00_START_HERE/SCOPE_AND_COMPLETENESS.md`.
    2. Read `01_CANON/CANONICAL_STATE_R62.md`.
    3. Query `05_MACHINE/genesis_chirality_full_checkpoint.sqlite` through `05_MACHINE/qmo_api.py`.
    4. Treat `3 | GENESIS_CHIRALITY_FULL_CUMULATIVE_v9.zip`, `6 | GENESIS_PROPAGATION_GIRL_PROJECT_v8.zip`, and `CRD_TO_QCD_INHERITANCE_FULL_v1_9.zip` as independent reservoirs until explicit reconciliation.
    5. Resume at `@open/native_multiscale_update_law`.

    ## Core recovery sentence

    > Chirality-native geometry is the ontology. Tile-level paths alter incident relationships; seed, byte/bite, block, and Time-Shell domains re-resolve; recursive closure and History determine what future generators remain available. The canonical coupling/path-selection law is still open.

    Recovery breadcrumb: **ですね**
    ''')

    write_text('00_START_HERE/SCOPE_AND_COMPLETENESS.md', '''
    # Scope and Completeness

    This is a **full technical checkpoint of the GENESIS / MK43 Chirality Fabric work represented in the active conversation and its explicitly imported companion models**.

    It includes unique logical content rather than storing byte-identical uploads twice. Exact duplicate filenames are preserved in `06_MANIFEST/DUPLICATE_ALIAS_MAP.json`; their canonical bytes are present once.

    It deliberately includes nested cumulative ZIPs even when they contain prior checkpoints, because lineage and provenance are part of the object. It also includes the direct v1.2–v1.8 CRD→QCD uploads for convenient access, despite their presence inside v1.9.

    It is not a verbatim export of the ChatGPT message stream. The conversation is represented by:

    - a detailed chronology,
    - a technical reconstruction,
    - canon and supersession ledgers,
    - equations, objects, claims, relationships, analogies, source receipts, and open debt in SQLite,
    - all available project artifacts uploaded or generated in the working runtime.

    Non-project résumé drafts and unrelated personal media are excluded. Relevant discussion images and world-model analogy sources are included and explicitly typed.
    ''')

    write_text('00_START_HERE/RECOVERY_PROMPT.md', '''
    # Full Checkpoint Recovery Prompt

    ですね

    Recover the GENESIS / MK43 Chirality Fabric project from this package as a full corpus checkpoint, not merely a summary.

    1. Mount the three independent cumulative reservoirs separately:
       - Genesis Chirality v9,
       - Propagation Girl Project v8,
       - CRD→QCD v1.9.
    2. Mount the unified MK43 QMO API, bidirectional Time-Space⇄Consciousness QMO, Rainbow Road, Genesis Field/Sandbox, formal Time-Space stack, CRD, Fusion, and the five Astraeus mathematics books.
    3. Load `05_MACHINE/genesis_chirality_full_checkpoint.sqlite` and use `05_MACHINE/qmo_api.py` as the recovery index.
    4. Preserve the authority firewalls in `01_CANON/AUTHORITY_AND_FIREWALLS.md`.
    5. Do not import conventional computer-science arrays, binary indexing, voxel adjacency, QCD, SU(2), or SU(3) into the native chirality ontology.
    6. Resume the active mathematical question:

       `@open/native_multiscale_update_law`

       Given one or more local tile color/phase paths inside a sandboxed 4×4×4 Chirality Block, determine what relational, multiscale, closure, History, Bandwidth, and Time-Shell constraints force the next admissible configuration.

    Current strongest localization:

    geometric adjacency → local color/phase continuity → Bandwidth-filtered generators → connection/selection or joint event → transport → sector/readout crossing → History append → changed future availability.

    Fixed-parameter conservative transfers commute. Any native noncommutativity must enter through state-, History-, Bandwidth-, connection-, closure-, or Time-Shell-dependent transport.
    ''')

    write_text('01_CANON/CANONICAL_STATE_R62.md', '''
    # Canonical Current State — R62

    ## 1. Foundational ordering

    The dependency/realization spine remains:

    Genesis Field → Time-Space → Resolution → Bandwidth → Persistence → Chirality → Helicon → Graviton → Time Shell → spacetime.

    Time-Space and spacetime are distinct. Chirality is upstream organizational grammar, not a downstream decoration.

    T0–T4 are treated as time-independent organizational regimes in the current pipeline reading. The T5 corridor is where a Time Shell is instantiated and localized temporal ordering begins. Each instantiated Time Shell carries a local chirality field/update History.

    ## 2. Native Chirality Fabric geometry

    - Chirality tile: one geometric position with occupancy and, when occupied, local chromatic/energy-density state.
    - Chirality seed: a native 2×2 arrangement of four tiles.
    - Right-handed toy profile: `[[0,1],[1,0]]`.
    - Left-handed mirror profile: `[[1,0],[0,1]]`; chromatic rule remains open.
    - Chirality byte/bite: set-lift of the seed into a 2×2×2 three-dimensional organization. Exact set-lift remains open.
    - Chirality block: native 4×4×4 domain with 64 tile positions. Current working profile uses 32 occupied and 32 unoccupied positions.
    - Chirality fabric: recursive extension of native blocks; no imported machine ontology may define it.

    Coordinates are optional charts. They are not tile identity, occupancy, or foundational zero.

    ## 3. Chromatic toy model

    Active toy weights:

    Red=1, Orange=2, Yellow=3, Green=4, Blue=5, Violet=6.

    An occupied tile carries one current chromatic anchor. A larger domain may resolve a local color charge by the truncated arithmetic mean of its contributing occupied colors. This is a toy readout, not yet the physical density law.

    Examples:

    - Orange(2)+Green(4) → mean 3 → Yellow seed.
    - Red(1)+Violet(6) → mean 3.5 → truncate to 3 → Yellow seed.
    - Two Yellow seed layers → Yellow byte/bite.

    The MK147 Density Ladder is fantasy/currency canon and is excluded from physical Chirality Fabric derivations.

    ## 4. Energy

    Recovered API objects include local energy density and native energy:

    - `rho_E = R T / V` in the recovered API notation.
    - `epsilon_MK = Delta Pi_min`.
    - `Pi = sum_d I_d B_d R_d O_d C_d`.

    Discovery provenance matters: native energy/unit energy emerged when independent API calls for unit strength and energy density were combined as seeds in a dependency landscape/QMO closure. The mature dependency graph is not identical to that discovery history.

    Working association: each occupied tile state may carry local energy density; chromatic basin/color is investigated as a readout of that density. The exact map remains open.

    ## 5. Torus and color transport

    A fixed-occupancy two-tile seed admits the candidate configuration space

    `T^2 = S_A^1 × S_B^1`.

    Each occupied tile has a cyclic phase coordinate. Long-range changes such as Orange→Violet, Green→Red, and Yellow→Blue are ordinary torus paths. They may be primitive, composed, or coarsely read; the current mathematics does not decide which.

    The torus supplies continuity, orientation, reachability, and winding History. It does not select the realized direction/path/reach.

    ## 6. Multiscale update

    A tile update necessarily changes:

    - the tile state,
    - every incident relationship involving that tile,
    - the complete seed configuration.

    It does not, by itself, prove that a related tile changes color. The partner may remain stable, gain different future availability, or be forced to compensate only if closure/persistence requires it.

    A block-level change is not primitive repainting. It is the resolved outcome of local tile paths, relationship propagation, seed re-resolution, byte/bite re-resolution, block re-resolution, recursive closure, History append, and changed future generator availability.

    Multiple local updates may be:

    - independent and commuting,
    - coupled and order-dependent,
    - or one joint event with no arbitrary serial order.

    ## 7. Noncommutativity result

    Bare fixed-parameter conservative transfers commute whenever both compositions are admissible:

    `T_{f,eps} ∘ T_{e,delta} = T_{e,delta} ∘ T_{f,eps}`.

    Therefore QCD-like/non-Abelian order-dependence cannot originate from raw adjacency plus fixed additive transfer alone. A sufficient—not canonical—route is state-dependent transport where the first event changes the admissibility or magnitude of the second.

    ## 8. Active frontier

    Primary open object:

    `@open/native_multiscale_update_law`

    Closely coupled open objects:

    - `@open/tile_coupling_law`
    - `@open/bandwidth_semantics`
    - `@open/seed_set_lift`
    - `@open/readout_composition`
    - `@open/canonical_noncommutativity`
    - `@open/simultaneous_update_semantics`
    - `@open/energy_density_color_map`
    - `@open/unoccupied_tile_state`
    - `@open/left_handed_chromatic_branch`
    - `@open/torus_path_selector`
    - `@open/block_red_to_green_realization`

    QCD remains a downstream comparison target. The direct six-basin→three-color quotient and automatic rank-3/SU(3) inheritance remain rejected without a witness.
    ''')

    write_text('01_CANON/LOCKS_AND_DEFINITIONS.md', '''
    # Locks and Definitions

    1. Chirality-native geometry precedes machine encoding.
    2. Zero/one used as occupancy/readout must never be reused as meaningless coordinate labels inside the ontology.
    3. A coordinate chart may name a tile but cannot define it.
    4. A QMO is a queryable dependency object; reverse query traversal is not semantic inversion.
    5. Dependency ordering and dynamical ordering are distinct.
    6. Chirality remains foundational after its dependency address is passed; downstream objects are realizations/projections of chirality organization.
    7. T5 is the Time-Shell-instantiation corridor, not simply a synonym for Time Shell.
    8. CRD relaxation may dissolve a locally persistent Time Shell into another while the underlying chirality substrate remains.
    9. Color weights 1–6 are the current toy model only.
    10. Fractional/gradient readout is future work; current toy model truncates.
    11. “Bandwidth two” has not been canonically identified with two neighboring colors, two directions, or two-sector reach.
    12. QCD, SU(2), and SU(3) may be comparison structures only after native derivation.
    13. The three independent cumulative reservoirs are not silently merged.
    14. Large-domain color is relational/multiresolution readout, not a color located at a single tile.
    15. Relationship propagates first; motion is a resolved description of that propagation.
    ''')

    write_text('01_CANON/AUTHORITY_AND_FIREWALLS.md', '''
    # Authority and Firewalls

    ## Independent reservoirs

    - Genesis Chirality v9: cumulative chirality/History/T0–T5 research body; sealed for tangent.
    - Propagation Girl v8: Genesis Field→Resolution→Bandwidth propagation model; R88 branch roadblock.
    - CRD→QCD v1.9: typed handoff/reduction investigation; L08D1 and W3 debt retained.
    - Unified MK43 API/QMO: traversal and dependency closure surface, not automatic proof or supersession.
    - Five Astraeus books: internal mathematical reservoirs; self-owning manuscripts must re-derive inherited mathematics.

    ## Firewalls

    - Do not identify chirality colors with QCD colors by name.
    - Do not infer SU(2) merely from a 2×2 seed.
    - Do not infer SU(3) merely from three downstream colors.
    - Do not let a shortest graph path replace the full architecture.
    - Do not treat support/dependency edges as causation or identity.
    - Do not force a path selector where topology supplies only possible paths.
    - Do not treat the MK147 Density Ladder as physics.
    - Do not promote the R60 state-dependent transfer witness into a canonical law.
    - Do not allow implementation arrays, memory offsets, UUIDs, or serialization to redefine tiles, seeds, bytes/bites, blocks, adjacency, or occupancy.
    ''')

    write_text('02_THREAD_HISTORY/FULL_THREAD_CHRONOLOGY.md', '''
    # Full Technical Chronology

    ## Phase A — Corpus/API/QMO construction

    1. Mounted the original multi-source MK43 corpus, including Time-Space, Higgs, dark matter, Rainbow Road, QFT–GR, chirality, projection, fusion, and the Tome.
    2. Deconstructed the parent unified QMO/API architecture into stable identity, typed records, typed graph, provenance, and bounded recursive query.
    3. Built `@mk43_unified_qmo_v2` and then self-closed it through repeated-squaring reachability.
    4. Generated Time-Space→Consciousness QMO, recovered the full cosmological spine, reversed traversal, and constructed a bidirectionally queryable QMO while preserving source edge direction.
    5. Produced a full finite formalization: namespace fibers, typed quiver, transitive closure, SCC decomposition, condensation DAG, and self-descriptive dependency vocabulary.

    ## Phase B — Cosmology, consciousness, and foundational chirality

    6. Audited the direct Cosmology→Consciousness edge. Reclassified its semantic interpretation as unresolved; candidate reading: cosmology/spacetime is the ambient realized domain within which consciousness can be locally realized.
    7. Corrected chirality from “one station in a pipeline” to foundational organizational grammar capable of representing atoms, spacetime, cosmology, and local persistent objects.
    8. Reaffirmed dependency order: Genesis Field→Time-Space→Resolution→Bandwidth→Persistence→Chirality→Helicon→Graviton→Time Shell→spacetime.

    ## Phase C — Time Shell and CRD

    9. Locked T0–T4 as time-independent in the current regime interpretation; T5 is the Time-Shell-instantiation/persistence-closure corridor.
    10. Used water/ice as the simple analogy: chirality is water; distinct persistent phase organizations are Time Shells; CRD can relax one shell until two shells become one.
    11. Distinguished substrate persistence from object persistence: the underlying chirality remains while the localized distinction dissolves.

    ## Phase D — Native chirality data geometry

    12. Defined chirality tile, seed, byte/bite, block, and fabric.
    13. Rejected conventional 000–111 array-index ontology after it collided with foundational zero/occupancy semantics.
    14. Locked geometry→formal object→machine encoding, never the reverse.
    15. Adopted a 4×4×4 Chirality Block as 64 native tile positions, with current half-occupancy working profile.

    ## Phase E — Chromatic hierarchy

    16. Introduced toy weights Red=1 through Violet=6.
    17. Assigned colors to occupied tiles and resolved local seed charge by truncated mean.
    18. Established hierarchical charge/readout: tile→seed→byte/bite→block.
    19. Distinguished exact lower-level configuration from larger-domain coarse readout.
    20. Excluded the MK147 Density Ladder from the physical model.

    ## Phase F — Energy and update question

    21. Recovered local energy density, native energy, and persistence functional through API calls.
    22. Preserved discovery provenance: unit strength + energy density seeded the QMO closure that produced native energy/unit energy.
    23. Localized the missing question: how does one color/density change alter the complete configuration?

    ## Phase G — CRD→QCD recovery

    24. Recovered v1.2–v1.9 CRD→QCD lineage.
    25. Preserved no-go results: direct six-basin→three-color descent is not source-derived; automatic rank-3/SU(3) handoff fails without W3.
    26. Preserved current handoff blocker `Lambda_HQ:D_HQ ⇀ Q_loc`.
    27. Reframed QCD as a downstream comparison target for any native transformation algebra.

    ## Phase H — Genesis sandbox and independent live models

    28. Mounted Genesis Field, Genesis Sandbox, Rainbow Road overlay, five mathematics books, and the formal Time-Space stack.
    29. Mounted Genesis Chirality cumulative v9 independently.
    30. Ran R60: proved fixed additive edge transfers commute and localized possible noncommutativity to context-dependent transport.
    31. Mounted Propagation Girl v8 independently; identified its R88 `Lambda_D` generator-map roadblock as the same seam as the chirality update-law problem.

    ## Phase I — Torus and multiscale update

    32. Recovered the color-circle/seed-torus model `T²=S¹_A×S¹_B`.
    33. Clarified that adjacent-sector transport is one continuity model, not a prohibition on long-range color change.
    34. Distinguished primitive direct transition, composed torus path, and coarse readout.
    35. Established winding/History as distinct from endpoint color.
    36. Modeled byte and block phase spaces provisionally as constrained subspaces of products of color circles.
    37. Established that one tile update changes its incident relationships and the full seed state, but does not yet force partner color.
    38. Distinguished independent simultaneous updates, coupled order-dependent updates, and joint events.
    39. Recast a block Red→Green change as coordinated tile-level paths plus multiscale re-resolution, not primitive repainting.
    40. Created compact R61 recovery, then corrected it into this full R62 corpus checkpoint after Genesis requested actual artifact inclusion rather than references.
    ''')

    write_text('02_THREAD_HISTORY/TECHNICAL_CONVERSATION_RECONSTRUCTION.md', '''
    # Technical Conversation Reconstruction

    **Status:** detailed reconstruction, not a verbatim transcript.

    The active investigation began from a unified MK43 QMO/API combining Time-Space, Higgs, dark matter, Rainbow Road, and related mathematical reservoirs. The API was recursively closed and used to generate a Time-Space→Consciousness object. Reversing the query traversal and recursively crawling both directions produced a bidirectional QMO. The resulting object was mathematically formalized as a provenance-bearing typed quiver with namespace fibers, relation witnesses, directed closure, and a large recurrent core.

    The direct Cosmology→Consciousness edge initially looked suspicious. The discussion separated causal mechanism from ambient-domain semantics. A defensible candidate reading is that spacetime/cosmology supplies the realized domain in which localized biological/cognitive consciousness may exist. This led back to chirality: chirality is not a physical sector downstream of atoms and spacetime; it is foundational organization that can be expressed at any scale.

    The Time-Shell discussion then corrected the dynamical picture. T0–T4 are upstream/time-independent in the current pipeline interpretation. T5 is where persistence closure permits a local Time Shell to instantiate. The water/ice analogy became canonical: chirality is the common medium; liquid water and ice are two persistent organizations of that same medium; CRD relaxation can remove the distinction supporting the ice shell, leaving one water shell.

    Chirality Fabric was next treated natively. A chirality seed is a 2×2 geometric object of four tiles. It set-lifts into a 2×2×2 byte/bite; Bandwidth expansion yields a 4×4×4 block with 64 tile positions. Conventional binary array addresses were rejected because they reused zero/one as meaningless labels inside a system where zero and occupancy already carry semantic meaning.

    The chromatic toy model assigns weights Red=1 through Violet=6 to occupied tiles. Larger domains resolve a local charge by averaging contributing colors and truncating fractional values. Orange+Green resolves to Yellow; Red+Violet also resolves to Yellow after truncation. This produces simultaneous tile-level colors and seed/byte/block-level relational charges. The exact configuration is retained even when a coarse readout remains unchanged.

    API calls recovered energy density and native energy. The key provenance is that unit strength and energy density were independently queried and combined as QMO seeds, allowing the API to close native energy/unit energy. Energy density is associated with occupied local states, while color is investigated as a local density/basin readout. The MK147 density ladder was explicitly rejected as a physical equation; it belongs to fantasy currency/storage canon.

    QCD was discussed as a non-Abelian local color transport theory. The project did not import QCD. Instead it asked what native transformation algebra a chirality sandbox generates. A 2×2 object was noted to have a mathematical cousin in SU(2), and the 3×3/8-generator QCD structure was explained, but both were retained as comparisons only.

    The torus branch gave a candidate continuous model. Each occupied tile has a color phase on S¹; two occupied seed tiles yield T². Orange→Violet, Green→Red, and Yellow→Blue are ordinary torus paths. Fine Resolution may expose all sector crossings; coarse Resolution may show only endpoints. Winding preserves path History. The torus does not decide direction, reach, or actualization.

    The multiscale update problem then became explicit. If Orange moves toward Blue while Green remains anchored, every intermediate state changes the seed relationship and may change the seed’s resolved color at a threshold. The partner tile is not automatically forced to move, but its relational environment and future generator availability may change. A byte has four occupied update-capable tile phases in the canonical working profile; a half-occupied block has thirty-two. A block-level transition is a path in a constrained joint configuration space and is read out at multiple resolutions.

    R60 proved that fixed-parameter conservative transfers commute. Therefore order-dependence requires the first event to alter the state used to evaluate the second—through History, Bandwidth, capacity, connection/holonomy, stabilization, or Time-Shell admissibility. Propagation Girl R88 independently asks what generates the domain-relative allowed transformations. The two branches intersect at the domain-relative generator of admissible chirality change.

    The present frontier is not “what are gluons?” It is: given one or more local tile paths, what native law selects, couples, closes, and records the next multiscale chirality configuration?
    ''')

    write_text('02_THREAD_HISTORY/SUPERSESSION_HISTORY.md', '''
    # Supersession History

    - **Old:** Chirality block as 2×2×2 computer array of byte slots.  
      **New:** Native 4×4×4 domain of 64 chirality tiles; byte grouping may be a downstream fixture only.

    - **Old:** 000–111 as chirality positions.  
      **New:** Coordinates are optional charts; zero/one remain occupancy/foundational symbols.

    - **Old:** Every tile possesses a color domain even when unoccupied.  
      **New:** Current canon attaches chromatic/energy-density realization to occupied tiles; unoccupied state remains open.

    - **Old:** Seed with Orange and Green is an Orange–Green seed.  
      **New:** Tile-level colors Orange and Green resolve to seed-level Yellow under the current toy rule.

    - **Old:** Red+Violet seed is half Yellow/Green.  
      **New:** Current toy model truncates 3.5 to Yellow; gradient treatment deferred.

    - **Old:** “Bandwidth two” means two neighboring colors.  
      **New:** This is only one candidate. Two may refer to directions, reach, generator count, or another native capacity.

    - **Old:** Torus continuity forbids direct long-range updates.  
      **New:** No theorem forbids them. Torus supplies composed/continuous paths and History; primitive/composed/readout status is open.

    - **Old:** One tile’s color update forces its partner tile to change.  
      **New:** It forces relationship/configuration change; partner response requires a coupling/closure law.

    - **Old:** Block color changes by repainting the block.  
      **New:** Block change is realized through tile paths and multiscale re-resolution.

    - **Old:** Fixed adjacency transfer may itself generate non-Abelian behavior.  
      **New:** Fixed additive transfers commute; context dependence is required.

    - **Old:** MK147 density ladder is a physical energy-density law.  
      **New:** It is fantasy/economy canon and excluded.

    - **Old:** QCD supplies the update law.  
      **New:** Native chirality update must be derived independently before QCD comparison.
    ''')

    write_text('03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md', '''
    # Torus and Multiscale Update Model

    ## Tile phase

    For each occupied tile `tau`, introduce a candidate color phase

    `theta_tau ∈ S¹`.

    The six discrete colors are sectors/readouts of this continuous coordinate.

    ## Seed torus

    For two occupied tiles A and B:

    `X_seed = S¹_A × S¹_B = T²`.

    A seed update is a path

    `gamma_seed:[0,1]→T²`.

    Long-range endpoints are ordinary paths. The same endpoint can carry different winding History:

    `pi_1(T²)=Z×Z`.

    ## Byte/bite and block

    Under the current fixed occupancy profile:

    `X_byte ⊆ (S¹)^4`

    and

    `X_block ⊆ (S¹)^32`.

    These products are configuration spaces, not claims of extra physical dimensions. The subset encodes native adjacency, occupancy, persistence, Resolution, Bandwidth, History, and closure constraints.

    ## Local-to-global path

    A local tile path changes the endpoint tile and every incident relationship. The resulting multiscale event is

    tile path → relation update → seed re-resolution → byte/bite re-resolution → block re-resolution → recursive closure → History append → future generator update.

    ## Readout

    Current toy domain color:

    `C(D)=trunc((1/N_D) Σ_i w(c_i))`.

    This is a coarse readout. Intermediate truncation means recursive readout and direct all-tile readout need not agree.

    ## Coupling possibilities

    If A updates while B remains fixed, B nevertheless occupies a changed relational environment. The unresolved law must decide whether B:

    1. stays fixed,
    2. gains different future availability,
    3. must compensate to maintain closure,
    4. participates in one joint event.

    ## Simultaneous events

    Independent events may commute. Coupled events may be order-dependent. Some coupled events should be represented jointly rather than serialized.

    ## Noncommutativity

    Fixed additive edge transfers commute. Candidate noncommutativity enters only when the first event changes the context used to determine the second event.
    ''')

    write_text('03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md', '''
    # Native Update Frontier

    ## Open operator

    Construct a partial multiscale chirality operator

    `U_chi:(K_t,Adj,R,B,H,P,Sigma) ⇀ (K_{t+1},H')`.

    It must determine one or more admissible local tile paths and propagate their relational consequences without importing QCD or conventional machine architecture.

    ## Generator-map intersection

    Propagation Girl R88 asks for

    `Lambda_D:(F_D,A_D,B)→Gen_D(B)`.

    The Chirality Fabric question asks for the generators available to a tile/seed/byte/block state. Their intersection is the domain-relative generator of admissible chirality change.

    ## Required outputs

    A complete law should specify:

    - current decorated state;
    - candidate tile paths;
    - path selection or joint-event construction;
    - local coupling/compensation;
    - Resolution sector crossings;
    - Bandwidth consumption/availability;
    - persistence and closure tests;
    - History append;
    - updated future generator set;
    - multiscale readouts.

    ## Must distinguish

    - primitive direct event;
    - composed path;
    - coarse unresolved readout;
    - independent simultaneous events;
    - ordered coupled events;
    - joint events;
    - inadmissible proposal.

    ## Current no-go/localization

    `T_{e,delta}(x)=x+delta b_e` with fixed parameters is insufficient for native noncommutativity. The first event must alter state-dependent availability or transport.
    ''')

    write_text('03_MATHEMATICS/CRD_QCD_FRONTIER.md', '''
    # CRD→QCD Frontier

    The recovered v1.9 lineage preserves:

    - Road→Helicon as a typed, generally set-valued correspondence;
    - corridor-backed Road→Persistent-Boundary carrier through `L_alpha`, `P_W`, and `C_ab=Pi_b∘P_W∘L_a`;
    - fixed-defect CRD reorientation as Abelian gauge fixing;
    - class-changing unbinding as gauge-orbit transition;
    - no direct source-derived six-basin→three-color quotient;
    - no automatic rank-3/SU(3) inheritance;
    - reduction witness `W_3` still open;
    - Time-Shell/Helicon→canonical-Q handoff `Lambda_HQ` still open.

    Current relation to Chirality Fabric:

    derive the native multiscale update and its transformation algebra first. Then test what survives Helicon/Time-Shell projection and whether a rank-3 non-Abelian downstream sector emerges. QCD is comparison, not premise.
    ''')


def copy_r61_docs():
    src = ROOT / 'GENESIS_CHIRALITY_FABRIC_FULL_THREAD_RECOVERY_R61_v1_0_20260829'
    if src.exists():
        dst = PKG / '04_PRIOR_EXPANDED/R61_COMPACT_RECOVERY_EXPANDED'
        shutil.copytree(src, dst)
    r60 = ROOT / 'GENESIS_CHIRALITY_TANGENT_R60_20260828'
    if r60.exists():
        shutil.copytree(r60, PKG / '04_PRIOR_EXPANDED/R60_TANGENT')
    for d, out in [
        (ROOT / 'CRD_QCD_BATCH_01', PKG / '04_PRIOR_EXPANDED/CRD_QCD_BATCH_01_NOTES'),
        (ROOT / 'MK43_FULL_MOUNT_20260826', PKG / '04_PRIOR_EXPANDED/MK43_INITIAL_MOUNT_MANIFEST'),
        (ROOT / 'QMO_FULL_MATHEMATICAL_FORMALIZATION_v1_0_20260826', PKG / '04_PRIOR_EXPANDED/QMO_FULL_FORMALIZATION_EXPANDED'),
        (ROOT / 'QMO_TIME_SPACE_TO_CONSCIOUSNESS_R10_FULL_EDGE_CLOSURE_20260826', PKG / '04_PRIOR_EXPANDED/QMO_R10_GRAPH_EXPANDED'),
    ]:
        if d.exists():
            shutil.copytree(d, out)


def clone_and_expand_db(artifacts: list[Artifact]):
    r61 = ROOT / 'GENESIS_CHIRALITY_FABRIC_FULL_THREAD_RECOVERY_R61_v1_0_20260829/07_MACHINE/genesis_chirality_recovery.sqlite'
    db = PKG / '05_MACHINE/genesis_chirality_full_checkpoint.sqlite'
    db.parent.mkdir(parents=True, exist_ok=True)
    if r61.exists():
        shutil.copy2(r61, db)
    con = sqlite3.connect(db)
    con.execute('PRAGMA foreign_keys=ON')
    con.executescript('''
    CREATE TABLE IF NOT EXISTS artifacts(
        address TEXT PRIMARY KEY,
        source_path TEXT,
        archive_path TEXT NOT NULL,
        group_name TEXT,
        role TEXT,
        status TEXT,
        sha256 TEXT,
        size_bytes INTEGER,
        notes TEXT
    );
    CREATE TABLE IF NOT EXISTS thread_segments(
        address TEXT PRIMARY KEY,
        phase TEXT,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        source_ref TEXT,
        status TEXT
    );
    CREATE TABLE IF NOT EXISTS checkpoint_components(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        qmo_address TEXT NOT NULL,
        component_address TEXT NOT NULL,
        relation TEXT NOT NULL,
        notes TEXT
    );
    CREATE TABLE IF NOT EXISTS file_aliases(
        alias_filename TEXT PRIMARY KEY,
        canonical_archive_path TEXT NOT NULL,
        reason TEXT
    );
    ''')
    md = {
        'package_name': NAME,
        'package_version': '1.0',
        'checkpoint_run': 'R62',
        'checkpoint_type': 'FULL_CORPUS_CHECKPOINT',
        'created_at': '2026-08-29',
        'primary_qmo': '@qmo/genesis_chirality_fabric_full_checkpoint_r62',
        'resume_address': '@open/native_multiscale_update_law',
        'compact_parent': '@qmo/genesis_chirality_fabric_r61',
    }
    for k,v in md.items():
        con.execute('INSERT OR REPLACE INTO metadata(key,value) VALUES(?,?)',(k,v))

    qmos = [
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','GENESIS Chirality Fabric Full Checkpoint R62','1.0','CURRENT_FULL_CHECKPOINT','Full conversation-linked source corpus, canon, mathematics, APIs, databases, and provenance.','Queryable dependency object for the complete checkpoint.','Genesis/Astraeus/Vera','00_START_HERE/README_FIRST.md','Supersedes R61 only as completeness checkpoint; does not erase R61.'),
        ('@qmo/genesis_chirality_cumulative_v9','Genesis Chirality Full Cumulative v9','9.0','INDEPENDENT_SEALED_SOURCE','Cumulative chirality QMO/history through R59.','Independent live reservoir.','Genesis Chirality v9','07_SOURCE_CORPUS/01_CUMULATIVE_LIVE_MODELS/3 | GENESIS_CHIRALITY_FULL_CUMULATIVE_v9.zip','Do not silently merge.'),
        ('@qmo/propagation_girl_v8','Genesis Propagation Girl Project v8','8.0','INDEPENDENT_R88_ROADBLOCK','Genesis Field→Resolution→Bandwidth propagation closure.','Independent generator-map reservoir.','Propagation v8','07_SOURCE_CORPUS/01_CUMULATIVE_LIVE_MODELS/6 | GENESIS_PROPAGATION_GIRL_PROJECT_v8.zip','Do not choose R88 branch without Genesis.'),
        ('@qmo/crd_qcd_v1_9','CRD→QCD Inheritance v1.9','1.9','INDEPENDENT_ACTIVE_DEBT','CRD-to-QCD typed handoff/reduction lineage.','Independent downstream comparison/handoff reservoir.','CRD-QCD v1.9','07_SOURCE_CORPUS/01_CUMULATIVE_LIVE_MODELS/CRD_TO_QCD_INHERITANCE_FULL_v1_9.zip','Lambda_HQ and W3 remain open.'),
        ('@qmo/mk43_unified_api_v2_1','MK43 Unified QMO API v2.1 R5','2.1','SELF_CLOSED','Unified query/dependency surface.','Self-closed API/QMO.','MK43 API','07_SOURCE_CORPUS/02_UNIFIED_API_QMO/MK43_ULTRA_UNIFIED_QMO_API_v2_1_R5_SELF_CLOSED_20260826.zip','Traversal does not promote proof.'),
        ('@qmo/time_space_consciousness_bidirectional','Time-Space⇄Consciousness Bidirectional QMO','1.0','CLOSED_QUERY_OBJECT','Bidirectionally queryable, directed-semantics QMO.','Query object used to expose connected architecture.','MK43 QMO','07_SOURCE_CORPUS/02_UNIFIED_API_QMO/MK43_TIME_SPACE_CONSCIOUSNESS_BIDIRECTIONAL_QMO_v1_0_20260827.zip','Reverse traversal is not inverse dependency.'),
    ]
    con.executemany('INSERT OR REPLACE INTO qmos(address,name,version,status,scope,definition,authority,source_ref,notes) VALUES(?,?,?,?,?,?,?,?,?)', qmos)

    new_objects = [
        ('@object/color_circle','Color Circle','configuration_space','CANDIDATE','Continuous S1 phase coordinate whose sectors read out R/O/Y/G/B/V.','R36/R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md','Not yet canonical physical field.'),
        ('@object/seed_torus','Seed Torus','configuration_space','STRONG_CANDIDATE','Joint two-tile color-phase space T2=S1_A×S1_B.','R36-R37','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md','Topology supplies paths, not selector.'),
        ('@object/byte_configuration_space','Byte/Bite Configuration Space','configuration_space','PROVISIONAL','Constrained joint color-phase space for four occupied tiles.','R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md','X_byte subseteq (S1)^4.'),
        ('@object/block_configuration_space','Block Configuration Space','configuration_space','PROVISIONAL','Constrained joint color-phase space for thirty-two occupied tiles in current half-occupancy block.','R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md','X_block subseteq (S1)^32.'),
        ('@object/joint_update_event','Joint Update Event','event','OPEN_TYPE','One coupled multicomponent path not assigned an arbitrary serial order.','R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md','Distinct from simultaneous independent events.'),
        ('@object/relationship_propagation','Relationship Propagation','mechanism','LOCKED_PARENT','Changing an endpoint changes incident relational organization before motion is resolved.','Propagation v8/R61','01_CANON/CANONICAL_STATE_R62.md','Relationship propagates first.'),
    ]
    con.executemany('INSERT OR REPLACE INTO objects(address,name,object_type,status,definition,authority,source_ref,notes) VALUES(?,?,?,?,?,?,?,?)', new_objects)

    new_eqs = [
        ('@eq/color_circle_phase','Tile color phase','theta_tau in S1','Continuous tile phase; discrete colors are sector readouts.','CANDIDATE','R36/R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md',''),
        ('@eq/seed_torus_path','Seed torus path','gamma_seed:[0,1]->T2','Joint two-tile History path.','CANDIDATE','R37/R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md',''),
        ('@eq/byte_joint_space','Byte joint space','X_byte subseteq (S1)^4','Four occupied tile phases under byte constraints.','PROVISIONAL','R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md',''),
        ('@eq/block_joint_space','Block joint space','X_block subseteq (S1)^32','Thirty-two occupied tile phases under block constraints.','PROVISIONAL','R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md',''),
        ('@eq/joint_update_path','Joint update path','Gamma_J(s)=(gamma_1(s),...,gamma_k(s))','One coupled event across k tile phases.','OPEN_CANDIDATE','R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md',''),
        ('@eq/relationship_first_update','Relationship-first update','endpoint change => incident relation change','Local tile change propagates relationally before larger-domain readout.','LOCKED_CONCEPT','Propagation v8/R62','01_CANON/CANONICAL_STATE_R62.md','Not yet a complete numerical law.'),
        ('@eq/multiscale_resolution_chain','Multiscale resolution chain','tile path -> relation -> seed -> byte/bite -> block -> closure -> History','Readable larger-domain change generated from local events.','WORKING_CANDIDATE','R62','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md',''),
        ('@eq/state_dependent_noncommutativity','State-dependent order test','U_B(U_A(X)) != U_A(U_B(X))','Possible when first event changes second event availability.','EXISTENCE_ONLY','R60/R62','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md','Not a canonical law.'),
    ]
    con.executemany('INSERT OR REPLACE INTO equations(address,name,expression,interpretation,status,authority,source_ref,notes) VALUES(?,?,?,?,?,?,?,?)', new_eqs)

    new_claims = [
        ('@claim/relationship_propagates_first','propagation','Relationship propagates first; motion is a resolved description of that propagation.','LOCKED_PARENT','Propagation v8','01_CANON/CANONICAL_STATE_R62.md',''),
        ('@claim/torus_long_range_reachable','torus','Orange→Violet, Green→Red, and Yellow→Blue are reachable torus paths; primitive/composed/readout status remains open.','CURRENT','R37/R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md',''),
        ('@claim/partner_not_forced','coupling','One tile update forces changed relationship/configuration but not partner color absent a coupling/closure law.','CURRENT_AUDIT','Vera R62','01_CANON/CANONICAL_STATE_R62.md',''),
        ('@claim/block_change_emergent','multiscale','A block-level color change is the resolved outcome of coordinated tile-level paths and multiscale closure.','CURRENT','R62','01_CANON/CANONICAL_STATE_R62.md',''),
        ('@claim/fixed_transfer_insufficient','algebra','Fixed additive local transfers are insufficient for native noncommutativity.','R60_RESULT','R60','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md',''),
        ('@claim/full_checkpoint_not_handoff','checkpoint','R62 includes the actual source corpus and prior models; it is not only a compact handoff.','LOCKED','Genesis explicit correction','00_START_HERE/SCOPE_AND_COMPLETENESS.md',''),
    ]
    con.executemany('INSERT OR REPLACE INTO claims(address,category,statement,status,authority,source_ref,notes) VALUES(?,?,?,?,?,?,?)', new_claims)

    new_debt = [
        ('@open/torus_path_selector',11,'Torus path selector','Determine direction, reach, speed, primitive/composed status, and coupled tile flow.','ACTIVE','@open/bandwidth_semantics','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md',''),
        ('@open/block_red_to_green_realization',12,'Block Red→Green realization','Classify the tile-level path family and threshold crossings required for a block-level Red→Green readout.','OPEN','@open/native_multiscale_update_law','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md',''),
        ('@open/joint_event_closure',13,'Joint event closure','Define when multiple coupled tile paths constitute one event and how closure is tested.','OPEN','@open/simultaneous_update_semantics','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md',''),
    ]
    con.executemany('INSERT OR REPLACE INTO open_debt(address,priority,title,description,status,blocked_by,source_ref,notes) VALUES(?,?,?,?,?,?,?,?)', new_debt)

    rels = [
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','EMBEDS','@qmo/genesis_chirality_fabric_r61','CURRENT','R62','08_PRIOR_CHECKPOINTS/GENESIS_CHIRALITY_FABRIC_FULL_THREAD_RECOVERY_R61_v1_0_20260829.zip',''),
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','MOUNTS_SEPARATELY','@qmo/genesis_chirality_cumulative_v9','CURRENT','R62','07_SOURCE_CORPUS/01_CUMULATIVE_LIVE_MODELS/3 | GENESIS_CHIRALITY_FULL_CUMULATIVE_v9.zip',''),
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','MOUNTS_SEPARATELY','@qmo/propagation_girl_v8','CURRENT','R62','07_SOURCE_CORPUS/01_CUMULATIVE_LIVE_MODELS/6 | GENESIS_PROPAGATION_GIRL_PROJECT_v8.zip',''),
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','MOUNTS_SEPARATELY','@qmo/crd_qcd_v1_9','CURRENT','R62','07_SOURCE_CORPUS/01_CUMULATIVE_LIVE_MODELS/CRD_TO_QCD_INHERITANCE_FULL_v1_9.zip',''),
        ('@object/chirality_tile','HAS_CANDIDATE_PHASE','@object/color_circle','CANDIDATE','R36/R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md',''),
        ('@object/chirality_seed','HAS_CONFIGURATION_SPACE','@object/seed_torus','STRONG_CANDIDATE','R37/R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md',''),
        ('@object/chirality_byte_bite','HAS_CONFIGURATION_SPACE','@object/byte_configuration_space','PROVISIONAL','R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md',''),
        ('@object/chirality_block','HAS_CONFIGURATION_SPACE','@object/block_configuration_space','PROVISIONAL','R62','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md',''),
        ('@object/relationship_propagation','PRECEDES_READOUT_AS','@eq/multiscale_resolution_chain','CURRENT','R62','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md',''),
        ('@eq/domain_generator_map','INTERSECTS','@eq/local_update_generator','OPEN_FRONTIER','R60/R88','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md',''),
        ('@eq/state_dependent_noncommutativity','LOCALIZES','@open/canonical_noncommutativity','EXISTENCE_ONLY','R60','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md',''),
        ('@object/joint_update_event','ADDRESSES','@open/joint_event_closure','OPEN','R62','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md',''),
    ]
    con.executemany('INSERT INTO relations(source_address,relation,target_address,status,authority,source_ref,notes) VALUES(?,?,?,?,?,?,?)', rels)

    chronology = [
        (15,'2026-08-29','R62','Genesis rejected the compact-handoff interpretation and requested a full corpus checkpoint containing actual artifacts.','LOCKED_CORRECTION','00_START_HERE/SCOPE_AND_COMPLETENESS.md',''),
        (16,'2026-08-29','R62','Built full checkpoint with cumulative live-model archives, direct CRD parents, APIs/QMOs, books, formal stack, prior checkpoints, SQLite and mini API.','CURRENT_CHECKPOINT','00_START_HERE/README_FIRST.md',''),
    ]
    con.executemany('INSERT OR REPLACE INTO chronology(seq,event_date,phase,event,status,source_ref,notes) VALUES(?,?,?,?,?,?,?)', chronology)

    # Thread segments
    segs = [
        ('@segment/api_qmo','API/QMO','Unified API and bidirectional QMO','Constructed, self-closed, reversed, crawled, and formally mapped the unified mathematical API/QMO.','02_THREAD_HISTORY/FULL_THREAD_CHRONOLOGY.md','CLOSED'),
        ('@segment/time_shell_crd','Time Shell/CRD','Time Shell, water/ice, and relaxation','Localized persistence, T5 instantiation, local chirality dynamics, and CRD dissolution analogy.','02_THREAD_HISTORY/TECHNICAL_CONVERSATION_RECONSTRUCTION.md','CURRENT'),
        ('@segment/native_geometry','Geometry','Tile/seed/byte/block/fabric','Replaced imported machine indexing with chirality-native 3D organization.','01_CANON/CANONICAL_STATE_R62.md','LOCKED'),
        ('@segment/color_energy','Color/Energy','Hierarchical color charge and energy density','Defined toy chromatic readout, recovered energy-density/native-energy provenance, and excluded MK147 ladder.','01_CANON/CANONICAL_STATE_R62.md','CURRENT'),
        ('@segment/torus','Torus','Continuous color phase and winding History','Recovered S1/T2 configuration spaces, reachability, and no-selector result.','03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md','STRONG_CANDIDATE'),
        ('@segment/multiscale_update','Update law','Native multiscale update frontier','Localized tile coupling, simultaneous events, closure, and context-dependent noncommutativity.','03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md','ACTIVE'),
    ]
    con.executemany('INSERT OR REPLACE INTO thread_segments(address,phase,title,summary,source_ref,status) VALUES(?,?,?,?,?,?)', segs)

    # Artifacts and aliases
    for i,a in enumerate(artifacts,1):
        addr=f'@artifact/{i:04d}'
        con.execute('INSERT OR REPLACE INTO artifacts(address,source_path,archive_path,group_name,role,status,sha256,size_bytes,notes) VALUES(?,?,?,?,?,?,?,?,?)',
                    (addr,a.source_path,a.archive_path,a.group_name,a.role,a.status,a.sha256,a.size_bytes,a.notes))
    for alias, canonical in DUPLICATE_ALIASES.items():
        con.execute('INSERT OR REPLACE INTO file_aliases(alias_filename,canonical_archive_path,reason) VALUES(?,?,?)',
                    (alias,canonical,'Byte-identical duplicate upload; canonical bytes stored once.'))

    components = [
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','@segment/api_qmo','CONTAINS',''),
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','@segment/time_shell_crd','CONTAINS',''),
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','@segment/native_geometry','CONTAINS',''),
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','@segment/color_energy','CONTAINS',''),
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','@segment/torus','CONTAINS',''),
        ('@qmo/genesis_chirality_fabric_full_checkpoint_r62','@segment/multiscale_update','CONTAINS',''),
    ]
    con.executemany('INSERT INTO checkpoint_components(qmo_address,component_address,relation,notes) VALUES(?,?,?,?)', components)

    # Source table entries for all physical artifacts
    for i,a in enumerate(artifacts,1):
        address=f'@source/full/{i:04d}'
        con.execute('INSERT OR REPLACE INTO sources(address,filename,sha256,size_bytes,kind,embedded,role,status,notes) VALUES(?,?,?,?,?,?,?,?,?)',
                    (address,Path(a.source_path).name,a.sha256,a.size_bytes,a.group_name,1,a.role,a.status,a.archive_path))

    con.commit()
    result=con.execute('PRAGMA integrity_check').fetchone()[0]
    if result != 'ok':
        raise RuntimeError(f'SQLite integrity failed: {result}')
    con.close()
    return db


def write_api():
    p = PKG / '05_MACHINE/qmo_api.py'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(r'''#!/usr/bin/env python3
import argparse, json, sqlite3, sys
from pathlib import Path

DB = Path(__file__).with_name('genesis_chirality_full_checkpoint.sqlite')
TABLES = {
    'qmos','objects','equations','claims','relations','chronology','open_debt','sources',
    'supersessions','aliases','analogies','recovery_rules','artifacts','thread_segments',
    'checkpoint_components','file_aliases','metadata'
}
ADDRESS_TABLES = ['qmos','objects','equations','claims','open_debt','sources','aliases','analogies','recovery_rules','artifacts','thread_segments']

def connect():
    con=sqlite3.connect(DB)
    con.row_factory=sqlite3.Row
    return con

def emit(x):
    print(json.dumps(x,indent=2,ensure_ascii=False))

def info(con):
    md={r['key']:r['value'] for r in con.execute('select key,value from metadata order by key')}
    counts={t:con.execute(f'select count(*) from {t}').fetchone()[0] for t in sorted(TABLES) if t!='metadata'}
    emit({'metadata':md,'counts':counts,'integrity':con.execute('pragma integrity_check').fetchone()[0]})

def address(con, key):
    out=[]
    for t in ADDRESS_TABLES:
        cols=[r[1] for r in con.execute(f'pragma table_info({t})')]
        col='address' if 'address' in cols else ('alias' if 'alias' in cols else None)
        if col:
            rows=con.execute(f'select * from {t} where {col}=?',(key,)).fetchall()
            out += [{'table':t, **dict(r)} for r in rows]
    emit(out)

def search(con, term):
    q=f'%{term}%'; out=[]
    for t in ['qmos','objects','equations','claims','open_debt','sources','artifacts','thread_segments']:
        cols=[r[1] for r in con.execute(f'pragma table_info({t})')]
        textcols=[c for c in cols if c not in {'id','size_bytes','priority','embedded','seq'}]
        where=' OR '.join([f'CAST({c} AS TEXT) LIKE ?' for c in textcols])
        rows=con.execute(f'select * from {t} where {where}',(q,)*len(textcols)).fetchall()
        out += [{'table':t, **dict(r)} for r in rows]
    emit(out)

def neighbors(con, key, direction):
    out=[]
    if direction in ('out','both'):
        out += [dict(r) for r in con.execute('select * from relations where source_address=?',(key,))]
    if direction in ('in','both'):
        out += [dict(r) for r in con.execute('select * from relations where target_address=?',(key,))]
    emit(out)

def list_table(con, table, limit):
    if table not in TABLES: raise SystemExit(f'Unknown table: {table}')
    emit([dict(r) for r in con.execute(f'select * from {table} limit ?',(limit,))])

def resume(con):
    emit({
      'primary_resume_address':'@open/native_multiscale_update_law',
      'record': [dict(r) for r in con.execute("select * from open_debt where address='@open/native_multiscale_update_law'")],
      'neighbors':[dict(r) for r in con.execute("select * from relations where source_address='@eq/domain_generator_map' or target_address='@eq/domain_generator_map' or source_address='@eq/local_update_generator' or target_address='@eq/local_update_generator'")]
    })

def main():
    ap=argparse.ArgumentParser(description='Queryable API for GENESIS Chirality Fabric Full Checkpoint R62')
    sp=ap.add_subparsers(dest='cmd',required=True)
    sp.add_parser('info')
    a=sp.add_parser('address'); a.add_argument('key')
    s=sp.add_parser('search'); s.add_argument('term')
    n=sp.add_parser('neighbors'); n.add_argument('key'); n.add_argument('--direction',choices=['in','out','both'],default='both')
    l=sp.add_parser('list'); l.add_argument('table'); l.add_argument('--limit',type=int,default=100)
    sp.add_parser('resume')
    args=ap.parse_args(); con=connect()
    try:
        {'info':lambda:info(con),'address':lambda:address(con,args.key),'search':lambda:search(con,args.term),'neighbors':lambda:neighbors(con,args.key,args.direction),'list':lambda:list_table(con,args.table,args.limit),'resume':lambda:resume(con)}[args.cmd]()
    finally: con.close()
if __name__=='__main__': main()
''').strip()+'\n', encoding='utf-8')
    os.chmod(p,0o755)
    return p


def build_artifacts() -> list[Artifact]:
    artifacts=[]
    missing=[]
    for src_name, arc, group, role in SOURCE_MAP + VISUAL_MAP:
        sp=ROOT/src_name
        if not sp.exists():
            missing.append(src_name); continue
        artifacts.append(Artifact(str(sp),arc,group,role,sha256=sha256_file(sp),size_bytes=sp.stat().st_size))
    # Direct R60 report outside root
    r60=ROOT/'GENESIS_CHIRALITY_TANGENT_R60_20260828/ASTRAEUS_VERA_R60_NATIVE_UPDATE_MECHANISM_TANGENT.md'
    if r60.exists():
        artifacts.append(Artifact(str(r60),'08_PRIOR_CHECKPOINTS/ASTRAEUS_VERA_R60_NATIVE_UPDATE_MECHANISM_TANGENT.md','report','R60 native update mechanism tangent.',sha256=sha256_file(r60),size_bytes=r60.stat().st_size))
    if missing:
        write_json('06_MANIFEST/MISSING_EXPECTED_FILES.json', missing)
    return artifacts


def make_manifests(artifacts: list[Artifact]):
    inv=PKG/'06_MANIFEST/FILE_INVENTORY.csv'; inv.parent.mkdir(parents=True,exist_ok=True)
    with inv.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(asdict(artifacts[0]).keys()))
        w.writeheader(); w.writerows(asdict(a) for a in artifacts)
    write_json('06_MANIFEST/PACKAGE_MANIFEST.json',{
        'package':NAME,
        'version':'1.0',
        'run':'R62',
        'date':'2026-08-29',
        'type':'FULL_CORPUS_CHECKPOINT',
        'primary_qmo':'@qmo/genesis_chirality_fabric_full_checkpoint_r62',
        'resume_address':'@open/native_multiscale_update_law',
        'physical_artifact_count':len(artifacts),
        'physical_artifact_bytes':sum(a.size_bytes for a in artifacts),
        'byte_identical_duplicates_represented_by_alias':len(DUPLICATE_ALIASES),
        'note':'Actual unique source artifacts are embedded. Byte-identical duplicate uploads are stored once with aliases. Nested lineage duplication is intentionally retained where it carries provenance.',
        'artifact_groups':sorted(set(a.group_name for a in artifacts)),
    })
    write_json('06_MANIFEST/DUPLICATE_ALIAS_MAP.json',DUPLICATE_ALIASES)
    write_text('06_MANIFEST/EMBEDDED_ARCHIVE_LOCATOR.md','''
    # Embedded Archive Locator

    - `CRD_TO_QCD_INHERITANCE_FULL_v1_9.zip` contains its complete v1.2–v1.8 parent lineage under `PARENTS/`; direct copies are also included in this checkpoint for convenience.
    - `3 | GENESIS_CHIRALITY_FULL_CUMULATIVE_v9.zip` contains v8, v7, prior live QMO bodies, torus v6, R39–R59 runs, unified API lineage, and many embedded SQLite databases.
    - `6 | GENESIS_PROPAGATION_GIRL_PROJECT_v8.zip` contains R83–R88, the prior full update, Bandwidth Algebra, and its queryable continuity database.
    - Unified API/QMO ZIPs contain their own SQLite and API surfaces.
    - The R61 compact package is preserved as a prior checkpoint but is not the completeness authority for R62.
    ''')


def generate_equation_ledger(db_path: Path):
    con=sqlite3.connect(db_path); con.row_factory=sqlite3.Row
    rows=con.execute('select address,name,expression,interpretation,status,authority,source_ref,notes from equations order by address').fetchall()
    lines=['# Full Equation Ledger','',f'Equations indexed: {len(rows)}','']
    for r in rows:
        lines += [f"## {r['address']} — {r['name']}",'',f"**Expression:** `{r['expression']}`  ",f"**Status:** {r['status']}  ",f"**Authority:** {r['authority'] or ''}  ",f"**Source:** {r['source_ref'] or ''}",'',r['interpretation'] or '', '', ('Notes: '+r['notes']) if r['notes'] else '', '']
    write_text('03_MATHEMATICS/FULL_EQUATION_LEDGER.md','\n'.join(lines))
    con.close()


def copy_build_script():
    src=Path(__file__)
    shutil.copy2(src, PKG/'05_MACHINE/build_full_checkpoint_r62.py')


def make_checksums(artifacts: list[Artifact]):
    # Hash generated package files (except checksum file itself) and externally included artifacts by final archive path.
    rows=[]
    for p in sorted(PKG.rglob('*')):
        if p.is_file() and p.name != 'CHECKSUMS.sha256':
            rows.append((sha256_file(p),p.relative_to(PKG).as_posix()))
    for a in artifacts:
        rows.append((a.sha256,a.archive_path))
    out=PKG/'06_MANIFEST/CHECKSUMS.sha256'
    out.write_text(''.join(f'{h}  {p}\n' for h,p in rows),encoding='utf-8')
    return out


def create_zip(artifacts: list[Artifact]):
    # Store pre-compressed/binary sources; deflate generated text/SQLite.
    store_ext={'.zip','.pdf','.png','.jpg','.jpeg','.mp4','.webp','.gif'}
    with zipfile.ZipFile(ZIP_OUT,'w',allowZip64=True) as z:
        for p in sorted(PKG.rglob('*')):
            if not p.is_file(): continue
            arc=f'{NAME}/{p.relative_to(PKG).as_posix()}'
            comp=zipfile.ZIP_STORED if p.suffix.lower() in store_ext else zipfile.ZIP_DEFLATED
            z.write(p,arc,compress_type=comp,compresslevel=6 if comp==zipfile.ZIP_DEFLATED else None)
        for a in artifacts:
            p=Path(a.source_path)
            arc=f'{NAME}/{a.archive_path}'
            comp=zipfile.ZIP_STORED if p.suffix.lower() in store_ext else zipfile.ZIP_DEFLATED
            z.write(p,arc,compress_type=comp,compresslevel=6 if comp==zipfile.ZIP_DEFLATED else None)
    with zipfile.ZipFile(ZIP_OUT) as z:
        bad=z.testzip()
        if bad: raise RuntimeError(f'ZIP CRC failure: {bad}')
    zh=sha256_file(ZIP_OUT)
    SIDE.write_text(f'{zh}  {ZIP_OUT.name}\n',encoding='utf-8')
    return zh


def qa(db: Path, artifacts: list[Artifact], zip_hash: str | None = None):
    con=sqlite3.connect(db)
    integrity=con.execute('pragma integrity_check').fetchone()[0]
    counts={r[0]:con.execute(f'select count(*) from {r[0]}').fetchone()[0] for r in con.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")}
    con.close()
    api=PKG/'05_MACHINE/qmo_api.py'
    smoke={}
    for args in [['info'],['address','@qmo/genesis_chirality_fabric_full_checkpoint_r62'],['address','@object/chirality_block'],['search','torus'],['neighbors','@object/chirality_seed','--direction','both'],['resume']]:
        cp=subprocess.run([sys.executable,str(api),*args],capture_output=True,text=True)
        smoke[' '.join(args)]={'returncode':cp.returncode,'stdout_prefix':cp.stdout[:500],'stderr':cp.stderr[:500]}
        if cp.returncode!=0: raise RuntimeError(f'API smoke failed: {args}: {cp.stderr}')
    report={
        'package':NAME,
        'sqlite_integrity':integrity,
        'table_counts':counts,
        'physical_artifact_count':len(artifacts),
        'physical_artifact_bytes':sum(a.size_bytes for a in artifacts),
        'zip_sha256':zip_hash,
        'api_smoke':smoke,
    }
    write_json('06_MANIFEST/QA_REPORT.json',report)
    return report


def main():
    ensure_clean()
    build_docs()
    copy_r61_docs()
    artifacts=build_artifacts()
    make_manifests(artifacts)
    db=clone_and_expand_db(artifacts)
    write_api()
    generate_equation_ledger(db)
    copy_build_script()
    # QA before final checksum/zip, then checksums, then zip. Update QA with hash requires a second tiny update and zip rebuild; avoid circularity.
    qa(db,artifacts,None)
    make_checksums(artifacts)
    zip_hash=create_zip(artifacts)
    # standalone final summary
    summary={
        'package':NAME,
        'zip_path':str(ZIP_OUT),
        'zip_size_bytes':ZIP_OUT.stat().st_size,
        'zip_sha256':zip_hash,
        'source_artifact_count':len(artifacts),
        'source_artifact_bytes':sum(a.size_bytes for a in artifacts),
        'sqlite':str(db),
        'sidecar':str(SIDE),
    }
    (ROOT/f'{NAME}_BUILD_SUMMARY.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=='__main__':
    main()
