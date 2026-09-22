# BRANE⁶ Live Model v0.1.0

Status: **ACTIVE — SEPARATE LIVE MODEL**  
Mount: `/mnt/data/BRANE6_ACTIVE_MOUNT_20260821/`

## 1. Model boundary

This live model is intentionally separate from:

1. the general BLACKGLASS corpus-driven programming-language model; and
2. the Computational Genesis Language handoff model.

No semantic claim or implementation decision is automatically promoted across model boundaries. Cross-model promotion requires an explicit reconciliation pass with provenance retained.

## 2. Recovered BRANE architecture

The supplied BRANE source defines the host as a typed six-coordinate organizational space:

```text
B^6 = I × D × Χ × R × P × Z
```

with:

- `I` — identity
- `D` — dependency
- `Χ` — chirality / admissibility
- `R` — recursive depth
- `P` — provenance
- `Z` — request-relative realization

A pluggable module is five-dimensional:

```text
M^5 = I × D × Χ × R × P
```

BRANE supplies the sixth coordinate at request time:

```text
ι_M : M^5 → B^6
ι_M(m) = (m1,m2,m3,m4,m5,z_M(q))
```

This is an organizational type model, not an assertion that every implementation object must be a rank-5 numerical array.

## 3. Canonical host/module separation

The recovered host boundary is explicit:

```text
BRANE host
├── private QMO⁶
├── port registry
├── contract/integrity validation
├── request-local composition
├── module lifecycle / replacement
└── artifact boundary

External ports
├── AI⁵
├── API⁵
└── Library⁵
```

BRANE does not own the domain payloads of AI/API/Library. It mounts external modules through validated ports. The modules need not share a domain as long as their contracts are compatible.

## 4. Active executable component candidates

### BRANE host — CORE ACTIVE

Bundle: `A_3.1_161051`  
Package: `mk43_brane`  
Module identity: `mk43.brane`  
Active manifest version: `2.3.3`

Primary responsibilities:

- five-dimensional module validation;
- private QMO⁶ realization;
- request isolation;
- chirality lift / admissibility mediation;
- module replacement and rollback;
- artifact/receipt egress;
- security and trust-boundary enforcement.

### API⁵ — CORE ACTIVE

Bundle: `G_2.0_161222`  
Package: `mk43_api1b`  
Version: `1.B.0`

Declared capabilities include:

- `resolve`
- `neighbors`
- `recover_closure`
- `recover_equations`
- `recover_provenance`
- `resolve_chirality`
- `admissible`
- `probe_subject`
- `validate_graph`

Policy: canonical state `READ_ONLY`; rewrites `DERIVED_ONLY`.

### Library⁵ — CORE ACTIVE

Bundle: `E_3.0_10`  
Package: `mk43_library`  
Version: `1.D.0`

Library owns recoverable content beneath mathematical/QMO addresses. It includes recovery, package population, provenance, transactions, rollback, and purge semantics.

Policy: canonical state `READ_ONLY`; rewrites `DERIVED_ONLY` during ordinary BRANE execution.

### AI⁵ — DEFERRED ACTIVE

Bundle: `D_2.1_161141`  
Package: `mk43_ai1c`  
Version: `1.C.1`

This is a complete executable AI⁵ / collapse-intelligence module, but it is intentionally lower priority for the present programming-language work. Keep available without allowing AI policy to define the language kernel.

## 5. Specification/reference bundles

### BRANE implementation spine

Bundle `B_1.0_161125` is architecture/contracts/schemas/pseudocode/roadmap and explicitly non-production. It is retained as a design-reference layer for checking whether executable BRANE behavior drifted from the original specification.

### Library implementation spine

Bundle `F_1.0_161159` is the Library 1.0 Alpha architecture/contracts/SQL/algorithms/pseudocode package. Bundle `E` is the later executable realization.

### API implementation spine

Bundle `H_1.0_161220` is the API 5.0 Alpha implementation architecture with preserved API 4.3 canon. It is intentionally non-executable. Bundle `G` is an executable API⁵ realization with preserved 4.3 canon.

### Earlier collapse-intelligence port

Bundle `C_1.0_161141` is a smaller earlier standalone AI port implementation. Preserve for lineage and interface archaeology; it is not the primary AI⁵ candidate.

## 6. 5D contract invariant

All active external module manifests agree on:

```text
internal_dimension     = 5
contract_version       = 2.0
canonical_state_policy = READ_ONLY
rewrite_policy         = DERIVED_ONLY
```

The host embedding contract rejects wrong role, wrong dimension, absent required methods, missing chirality/provenance support, incompatible contract versions, or canonical mutation capability.

This makes `dimension = 5` a validated module capability contract, not merely documentation.

## 7. BRANE implications for the programming language

Do not yet merge these into language canon; treat them as target/runtime constraints.

High-value candidates:

1. **Capability-typed modules.** A language module may eventually declare dimensional/role/capability contracts that BRANE validates before mounting.
2. **Request-relative realization.** The sixth coordinate `Z` is not owned by the module; it is created by the host during execution. This is a strong candidate for a runtime notion distinct from source identity.
3. **Read-only canonical state + derived-only transformations.** This aligns naturally with provenance-aware, inheritance-based language semantics.
4. **Private QMO⁶.** Intermediate execution topology can remain private while artifacts are projected across the public boundary.
5. **Chirality/admissibility as contract data.** Chirality is already a required module declaration and participates in host lifting/validation.
6. **Role independence.** API, Library, and AI can be replaced independently without re-owning one another's state.

## 8. Important dimensional distinction

There are two different meanings of "five-dimensional" present in the mounted corpus:

### BRANE module dimension

```text
M^5 = I × D × Χ × R × P
```

This is a typed organizational coordinate model.

### 3+1+1 field topology

The biomedical side package contains arrays such as:

```text
chirality_field shape = (32,32,32,2,2)
```

This is numerical/topological field data. It is useful as a possible payload or application fixture, but its ndarray rank must not be used as proof that it satisfies the BRANE `M^5` module contract. A BRANE module must satisfy the semantic contract and port manifest.

## 9. Integrity state

- Uploaded archives: **9/9 CRC PASS**.
- Extracted files: **708**.
- Extracted bytes: **312,393,247**.
- Python source files: **50**.
- Python AST parse: **50/50 PASS** (syntax-only; code not executed).
- JSON parsing: no malformed JSON detected in this ingest.
- No nested archives were present inside these nine ZIPs.

Final/current checksum layers used for integrity are preserved in `META/CHECKSUM_VERIFICATION.json`. Several legacy/incremental checksum lists no longer describe later additive overlays; they are retained as historical records rather than silently rewritten.

## 10. Provenance / conflict locks

### BRANE host version drift

Source metadata is not perfectly synchronized:

- `brane_module.json`, package manifest, and official manifest identify **2.3.3**;
- root `README.md` and `pyproject.toml` still carry **2.3.2** labels.

Working rule: treat `2.3.3` as the active packaged module identity while preserving the 2.3.2 text as source metadata drift. Do not rewrite source files.

### Acceptance-count drift

The root README states an expected **23 passed**, while later changelog/release-validation material records **24 passed** for later closure work. No user code was executed during this ingest, so neither number is independently re-certified here.

### API naming lineage

The API corpus contains multiple versioning schemes (`4.3` canon, `5.0 Alpha` implementation spine, `1.B` executable module). Preserve this as lineage until an explicit version-normalization pass establishes the intended mapping.

## 11. Side/application model

Bundle `I_VIRUS_UTERINE_v0_28` is not promoted into BRANE core. It is an application/reference model containing 3+1+1 chirality-field datasets for five model classes. Its own boundary explicitly limits interpretation to computational organizational projections and geometry-only overlap probes; physical coupling and biomedical validation remain unresolved.

It is retained as a potentially valuable stress-test payload for future 5D/3+1+1 data handling, not as a source of BRANE host semantics.

## 12. Current development rule

```text
SOURCE ARCHIVES      immutable
EXTRACTED            source-preserving expansion
LIVE                 active BRANE⁶ model
SIDE_MODEL           useful but non-core / unresolved material
META                 hashes, registries, integrity and lineage
```

Promotion from BRANE⁶ into either BLACKGLASS language model is explicit and provenance-preserving.
