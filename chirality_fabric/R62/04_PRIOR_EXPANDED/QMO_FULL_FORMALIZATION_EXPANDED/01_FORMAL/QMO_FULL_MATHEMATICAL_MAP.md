# QMO Full Mathematical Map and Formalization
## QMO-CONSCIOUSNESS-TO-TIME-SPACE-API-CRAWL-R8-001

**Formalization:** Astraeus-derived mathematical description  
**Audit role:** Vera provenance/status discipline  
**Date:** 2026-08-26  
**Basis database SHA-256:** `cf2dd5617d530ff4d03beb2b55f75f002b200bbe2aa6f856df40045f1cbb353b`  
**Root:** `@consciousness`  
**Terminal:** `@time_space`  
**Query view:** reverse-rooted / bidirectionally traversable  
**Source-edge orientation:** preserved

> This formalizes the finite QMO actually stored in the machine object. It does not promote graph adjacency, reachability, or recursive closure into physical causation, theorem entailment, identity, or final canon unless an underlying typed relation already carries that meaning.

# 1. Exact object

\[
\mathcal Q=(V,\widetilde V,\mathcal R,W,E_0,C,\mathcal F,\pi,\kappa,\omega,p,\sigma,A_0,B,\Gamma).
\]

| Symbol | Meaning | Cardinality |
|---|---|---:|
| \(V\) | canonical handles | 1,459 |
| \(\widetilde V\) | namespace-specific instances | 3,316 |
| \(\mathcal R\) | relation alphabet | 355 |
| \(W\) | provenance-bearing edge witnesses | 160,057 |
| \(E_0\) | canonical typed edge triples | 79,624 |
| \(A\) | distinct directed source-target pairs | 68,029 |
| \(C\) | derived non-reflexive closure pairs | 1,733,204 |
| \(A^+\) | total materialized non-reflexive reachable pairs | 1,801,233 |
| \(\mathcal F\) | equations | 163 |

There are no self-loops in the canonical typed-edge or self-closure tables.

# 2. Namespace-fibered identity

A materialized instance is

\[
\tilde v=(h,n,\nu,\tau,s,p)\in\widetilde V
\]

and canonicalization is

\[
\pi:\widetilde V\to V,\qquad \pi(\tilde v)=h.
\]

The instance table covers **1,457 of 1,459** canonical graph handles. The two edge-addressable handles with no instance row are:

- `@corridor`
- `@unit_string_configuration_algebra`

Thus canonical graph identity and source-instance identity are different layers.

Namespace multiplicity:

|   namespace_count |   handle_count |
|------------------:|---------------:|
|                 1 |            110 |
|                 2 |           1074 |
|                 3 |            100 |
|                 4 |            147 |
|                 5 |              4 |
|                 6 |             15 |
|                 7 |              3 |
|                 9 |              1 |
|                10 |              3 |

The maximum multiplicity is 10, attained by `@bandwidth`, `@chirality`, and `@resolution`.

# 3. Witnessed typed quiver

Each evidence edge is

\[
w=(u,r,v,\eta)\in W,
\]

with \(u,v\in V\), \(r\in\mathcal R\), and provenance payload \(\eta\). Witness canonicalization is

\[
\kappa:W\twoheadrightarrow E_0,\qquad
\kappa(u,r,v,\eta)=(u,r,v).
\]

Every canonical typed edge has at least one witness.

For each relation \(r\),

\[
(A_r)_{ij}=1\iff(v_i,r,v_j)\in E_0,
\]

and the unlabeled adjacency is

\[
A_0=\bigvee_{r\in\mathcal R}A_r.
\]

The QMO is therefore a **typed directed multirelational graph / quiver**, not a simple graph.

# 4. Relation algebra

A path is

\[
\gamma=v_0\xrightarrow{r_1}v_1\xrightarrow{r_2}\cdots\xrightarrow{r_k}v_k.
\]

Graph path composition does not automatically imply semantic relation composition:

\[
\operatorname{AdmissibleCompose}(\mathcal Q)\subseteq\operatorname{Path}(\mathcal Q).
\]

So the object should not be promoted wholesale to a category unless a relation-composition law is supplied. `COMPOSED_DEPENDENCY` is explicit; arbitrary label sequences are not silently composable.

Top relation labels:

| relation                           |   canonical_typed_edges |   witness_count |   source_handle_count |   target_handle_count | formalization_class                  |
|:-----------------------------------|------------------------:|----------------:|----------------------:|----------------------:|:-------------------------------------|
| COMPOSED_DEPENDENCY                |                   57872 |          118450 |                   453 |                   269 | dependency_ordering                  |
| SUPPORTS                           |                    8509 |           17022 |                   213 |                   319 | support_constraint_admissibility     |
| DEPENDS_ON                         |                    5965 |           11948 |                   347 |                   259 | dependency_ordering                  |
| CLASSIFIED_IN_PHYSICS_NEIGHBORHOOD |                    1091 |            1091 |                   851 |                    13 | other_or_source_specific             |
| INDEXES_RELATED_OBJECT             |                    1091 |            1091 |                    13 |                   851 | coupling_connectivity                |
| GLOBALLY_FEEDS_BLACK_HOLE          |                     445 |             890 |                   445 |                     1 | domain_specific_black_hole           |
| FEEDS_BLACK_HOLE_MODEL             |                     444 |             888 |                   444 |                     1 | domain_specific_black_hole           |
| BLACK_HOLE_CROSS_FAMILY_NODE       |                     435 |             870 |                   435 |                     1 | domain_specific_black_hole           |
| BLACK_HOLE_GLOBAL_REACHES          |                     370 |             740 |                     1 |                   370 | domain_specific_black_hole           |
| BLACK_HOLE_MODEL_REACHES           |                     370 |             740 |                     1 |                   370 | domain_specific_black_hole           |
| FAMILY_DEPENDS_ON                  |                     323 |             720 |                   323 |                    17 | dependency_ordering                  |
| SUPPORTS_FAMILY                    |                     323 |             646 |                    17 |                   323 | support_constraint_admissibility     |
| DIRECTED_TO                        |                     192 |             488 |                   122 |                   124 | dependency_ordering                  |
| FORMALLY_DEPENDS_ON                |                     156 |             405 |                   104 |                    98 | dependency_ordering                  |
| VERTICAL_CHAIN                     |                     155 |             383 |                   115 |                   119 | dependency_ordering                  |
| FORMALLY_SUPPORTS                  |                     153 |             306 |                    95 |                   102 | support_constraint_admissibility     |
| USED_BY                            |                     137 |             353 |                    91 |                   103 | other_or_source_specific             |
| DECLARES_PARENT                    |                     108 |             108 |                    33 |                    58 | provenance_recovery_history          |
| DEPENDS_TO                         |                     105 |             278 |                    81 |                    79 | dependency_ordering                  |
| EXPLICIT_ARROW                     |                     104 |             276 |                    80 |                    78 | other_or_source_specific             |
| RECOVERED_DEPENDENCY               |                     104 |             276 |                    80 |                    78 | dependency_ordering                  |
| LANGUAGE_COMPOSES                  |                      43 |              86 |                    14 |                    18 | composition_transformation_transport |
| RESOLVED_VERTICAL_CHAIN            |                      41 |              99 |                    32 |                    31 | dependency_ordering                  |
| GOVERNS                            |                      39 |              78 |                     4 |                    36 | support_constraint_admissibility     |
| REALIZES                           |                      33 |              83 |                    30 |                    27 | realization_representation_readout   |
| REQUIRES                           |                      33 |              35 |                    14 |                    21 | support_constraint_admissibility     |
| BINDS_NATIVE_HANDLE                |                      30 |              30 |                    10 |                    29 | other_or_source_specific             |
| GENERATES                          |                      29 |              60 |                    24 |                    28 | generation_causation                 |
| CONNECTS_TO                        |                      28 |              59 |                    10 |                    10 | coupling_connectivity                |
| GENERATED_BY                       |                      26 |              54 |                    25 |                    23 | provenance_recovery_history          |

Astraeus-derived relation-family grouping, for navigation only:

| formalization_class                  |   relation_types |   canonical_typed_edges |   witnesses |
|:-------------------------------------|-----------------:|------------------------:|------------:|
| dependency_ordering                  |               19 |                   64949 |      133105 |
| support_constraint_admissibility     |               52 |                    9167 |       18246 |
| domain_specific_black_hole           |                5 |                    2064 |        4128 |
| other_or_source_specific             |              109 |                    1648 |        2250 |
| coupling_connectivity                |               17 |                    1196 |        1286 |
| provenance_recovery_history          |               27 |                     196 |         240 |
| realization_representation_readout   |               54 |                     167 |         339 |
| composition_transformation_transport |               28 |                      85 |         163 |
| containment_typing_structure         |               23 |                      54 |         105 |
| generation_causation                 |               11 |                      51 |         104 |
| language_meta_formal                 |                4 |                      35 |          70 |
| validation_observation               |                6 |                      12 |          21 |

The exhaustive 355-label catalog is `RELATION_LEDGER.csv`.

# 5. Provenance and status

\[
p:W\cup\widetilde V\cup\mathcal F\to\mathcal P
\]

is the provenance map.

Object-instance status is product-valued:

\[
\sigma_V(\tilde v)=
(s_{general},s_{proof},s_{typing},s_{validation},s_{canon},s_{recovery},s_{publication}).
\]

Edge witnesses separately carry trust class, confidence, source ID, and source path. There is therefore no valid single Boolean “truth” map for the whole QMO without choosing a status dimension and an admissibility criterion.

# 6. Equations

\[
\mathcal F=\{f_1,\ldots,f_{163}\},
\qquad
\omega:\mathcal F\to V.
\]

All equations have owners. Most equation-dense owners:

| handle                            |   n_eq |
|:----------------------------------|-------:|
| @readable_graviton_projection     |     13 |
| @universal_coupling               |      9 |
| @strong_field_gravity             |      8 |
| @graviton_propagation             |      7 |
| @sw_electromagnetic_sector        |      7 |
| @cosmology                        |      6 |
| @dimensionality_audit             |      6 |
| @multiparticle_gravity            |      6 |
| @projected_gr_inheritance         |      6 |
| @radiative_stability              |      6 |
| @chirality_corridor               |      5 |
| @rainbow_road                     |      5 |
| @local_positive_stress_energy     |      4 |
| @bandwidth_algebra                |      3 |
| @gravity_audit_v2                 |      3 |
| @sw_fluid_sector                  |      3 |
| @sw_plasma_sector                 |      3 |
| @conditioned_lock_selector        |      2 |
| @finite_higgs_mass_coupling       |      2 |
| @genesis_field                    |      2 |
| @helicon_spectral_operator        |      2 |
| @higgs_field                      |      2 |
| @higgs_mass_matrix_correspondence |      2 |
| @higgs_order_excitation           |      2 |
| @local_component_match_spacelike  |      2 |

The dedicated `proof_status` field is `UNSPECIFIED` for all 163 equation rows, so proof force must remain attached to status/provenance rather than being inferred from row existence.

# 7. Distinguished structural spine

\[
\boxed{
@time\_space
\to @genesis\_field
\to @resolution
\to @bandwidth
\to @persistence
\to @chirality
\to @helicon
\to @graviton
\to @time\_shell
\to @spacetime
\to @black\_hole
\to @black\_hole\_cosmology
\to @cosmology
\to @consciousness
}.
\]

This is a distinguished route, not the shape of the whole QMO. Exact typed witnesses for each consecutive pair are in `CORE_SPINE_EDGE_WITNESSES.csv`.

# 8. Higgs and dark-matter branches

Recovered Higgs route:

\[
@time\_space\to @genesis\_field
\xrightarrow{CLASSIFIED\_IN\_PHYSICS\_NEIGHBORHOOD}
@sw\_qft\_sector
\xrightarrow{INDEXES\_RELATED\_OBJECT}
@higgs\_field.
\]

The QMO also contains

\[
@higgs\_field\xrightarrow{HAS\_ENVIRONMENTAL\_ANCESTRY}@genesis\_field.
\]

Recovered dark-matter route:

\[
@time\_space\to @graviton
\xrightarrow{SUPPORTS}@structure\_formation
\xrightarrow{RECEIVES\_CONTRIBUTION\_FROM}@dark\_matter\_geometry.
\]

Separately,

\[
@dark\_matter\_geometry\xrightarrow{CONTRIBUTES\_TO}@structure\_formation.
\]

That reciprocal-looking pair is source-typed independently; it is not created merely by graph reversal.

# 9. Bidirectional query

Forward reachability:

\[
R^+(x)=\{y:x\rightsquigarrow_G y\}.
\]

Reverse/predecessor reachability:

\[
R^-(x)=\{y:y\rightsquigarrow_Gx\}=R^+_{G^T}(x).
\]

The transpose is a query view:

\[
(u,v)\in G^T\iff(v,u)\in G.
\]

It does not rewrite source semantics.

\[
\boxed{\text{bidirectional in traversal; directed in semantics.}}
\]

# 10. Recursive bidirectional crawl

A single union \(R^+(S_0)\cup R^-(S_0)\) is insufficient for nodes requiring alternating edge orientation.

Define

\[
B=A_0\lor A_0^T
\]

and

\[
\mathcal N_B(S)=S\cup\{v:\exists u\in S,\ B_{uv}=1\}.
\]

Then

\[
S_{n+1}=\mathcal N_B(S_n).
\]

For the 14-handle seed, the exact shells are

\[
14\xrightarrow{+542}556\xrightarrow{+601}1157\xrightarrow{+256}1413
\xrightarrow{+20}1433\xrightarrow{+7}1440\xrightarrow{+17}1457
\xrightarrow{+2}1459.
\]

Hence the symmetrized seed radius is

\[
\boxed{7}
\]

and iteration 8 is the zero-growth witness:

\[
S_8=S_7=V,\qquad \mathcal N_B(V)=V.
\]

# 11. Directed self-closure

Directed reachability is independently materialized as

\[
A^+=\bigvee_{k\ge1}A_0^k.
\]

The QMO stores 1,733,204 new closure pairs disjoint from primitive adjacency, giving 1,801,233 reachable non-reflexive ordered pairs.

Repeated squaring:

\[
C_0=A_0,\qquad C_{j+1}=C_j\lor(C_j\circ C_j),
\]

with effective horizons

\[
1\to2\to4\to8\to16.
\]

Stored closure-pair shortest distances range from 2 through 15. The unique maximum-distance pair is

\[
\boxed{@intrinsic_path_measure\rightsquigarrow @Pi_QCD}.
\]

Closure by pass:

|   closure_pass |   pair_count |   min_distance |   max_distance |
|---------------:|-------------:|---------------:|---------------:|
|              1 |       354117 |              2 |              2 |
|              2 |      1167374 |              3 |              4 |
|              3 |       206213 |              5 |              8 |
|              4 |         5500 |              9 |             15 |

Because \(15<16\), the repeated-squaring horizon is sufficient for this finite graph.

# 12. Global topology

The unlabeled graph has

\[
\boxed{1\text{ weakly connected component}}
\]

and

\[
\boxed{176\text{ strongly connected components}}.
\]

The giant SCC contains

\[
\boxed{1,260=86.3605\%\text{ of all canonical handles}}.
\]

It contains the entire Time-Space→Consciousness spine plus `@higgs_field` and `@dark_matter_geometry`.

Therefore the core is not a tree and not a DAG. It is a large recurrent directed domain.

# 13. Condensation graph

Let \(u\sim_{SCC}v\) iff \(u,v\) are mutually reachable. The condensation is

\[
\Gamma=G/\!\sim_{SCC}.
\]

Measured:

\[
|V(\Gamma)|=176,\qquad |E(\Gamma)|=212.
\]

There are 69 source SCCs and 64 sink SCCs.

\[
\boxed{\Gamma\text{ is a DAG}.}
\]

So the coarse topology is:

\[
\boxed{\text{recurrent directed mathematical domains organized by a condensation DAG}.}
\]

# 14. Structural centrality

Highest total-degree handles:

| handle                   |   in_degree |   out_degree |   total_degree |   namespace_count |   equation_count |
|:-------------------------|------------:|-------------:|---------------:|------------------:|-----------------:|
| @black_hole              |         481 |          375 |            856 |                 4 |                0 |
| @graviton                |         443 |          315 |            758 |                 7 |                0 |
| @metric_perturbation     |         436 |          310 |            746 |                 4 |                0 |
| @spacetime               |         436 |          310 |            746 |                 4 |                0 |
| @readable_space_time     |         435 |          307 |            742 |                 4 |                0 |
| @time_shell_projection   |         435 |          307 |            742 |                 4 |                0 |
| @einstein_field_equation |         444 |          297 |            741 |                 6 |                0 |
| @stress_energy_tensor    |         452 |          286 |            738 |                 6 |                0 |
| @smooth_manifold         |         416 |          310 |            726 |                 2 |                0 |
| @matter_action           |         439 |          284 |            723 |                 6 |                0 |
| @einstein_hilbert_action |         437 |          282 |            719 |                 4 |                0 |
| @metric_variation        |         439 |          280 |            719 |                 4 |                0 |
| @matter_coupling         |         438 |          279 |            717 |                 6 |                0 |
| @einstein_tensor         |         439 |          278 |            717 |                 4 |                0 |
| @tensor_field            |         436 |          281 |            717 |                 4 |                0 |
| @metric_tensor           |         438 |          278 |            716 |                 4 |                0 |
| @tangent_space           |         415 |          285 |            700 |                 3 |                0 |
| @tangent_vector          |         414 |          285 |            699 |                 2 |                0 |
| @levi_civita_connection  |         416 |          282 |            698 |                 2 |                0 |
| @tangent_bundle          |         415 |          282 |            697 |                 2 |                0 |

Highest PageRank handles:

| handle                        |   pagerank |   in_degree |   out_degree |   scc_size |
|:------------------------------|-----------:|------------:|-------------:|-----------:|
| @sw_wave_resonance_sector     | 0.042789   |         248 |          245 |       1260 |
| @sw_qft_sector                | 0.0377023  |         252 |          248 |       1260 |
| @sw_gravity_geometry_sector   | 0.0204736  |         191 |          189 |       1260 |
| @black_hole                   | 0.0144713  |         481 |          375 |       1260 |
| @sw_transport_sector          | 0.0128513  |          70 |           65 |       1260 |
| @sw_matter_sector             | 0.0119106  |          89 |           87 |       1260 |
| @sw_chirality_sector          | 0.0105158  |          98 |           97 |       1260 |
| @sw_optics_sector             | 0.00739239 |          55 |           53 |       1260 |
| @sw_material_sector           | 0.00665584 |          47 |           44 |       1260 |
| @time_shell                   | 0.00494396 |         447 |          136 |       1260 |
| @propagation_operator         | 0.00473214 |         420 |            5 |       1260 |
| @white_state_core             | 0.00425832 |         417 |          133 |       1260 |
| @graviton_radiative_stability | 0.00424033 |         448 |            8 |       1260 |
| @dependency_graph             | 0.00421976 |          14 |           15 |         14 |
| @stress_energy_tensor         | 0.00418652 |         452 |          286 |       1260 |
| @geometry                     | 0.00415638 |         437 |          135 |       1260 |
| @graviton                     | 0.00400269 |         443 |          315 |       1260 |
| @total_action                 | 0.00395389 |         417 |          146 |       1260 |
| @pattern_recognition          | 0.00390921 |         416 |          131 |       1260 |
| @native_constraint_closure    | 0.0039     |         445 |           10 |       1260 |

These are connectivity metrics only; they do not establish physical fundamentality.

# 15. Federated namespace map

| namespace                        |   object_instances |   canonical_handles |   edge_witnesses |   source_handles |   target_handles |   equations |
|:---------------------------------|-------------------:|--------------------:|-----------------:|-----------------:|-----------------:|------------:|
| STONEWAKE::API43                 |               1205 |                1205 |            75387 |              647 |              682 |          72 |
| API43                            |               1205 |                1205 |                0 |                0 |                0 |           0 |
| TIME_SPACE_4_3                   |                262 |                 262 |                0 |                0 |                0 |           0 |
| STONEWAKE::DARK_MATTER           |                224 |                 224 |             5473 |              165 |              108 |           0 |
| STONEWAKE::HIGGS                 |                 74 |                  74 |              147 |               54 |               69 |          19 |
| HIGGS_WORK_LAYER_V1_1            |                 74 |                  74 |                0 |                0 |                0 |          19 |
| DARK_MATTER_2_2                  |                 38 |                  38 |                0 |                0 |                0 |           0 |
| DARK_MATTER_LIVE_E100            |                 35 |                  35 |                0 |                0 |                0 |           0 |
| DARK_MATTER_SOURCE_EFFECTIVE     |                 35 |                  35 |                0 |                0 |                0 |           0 |
| STONEWAKE::STONEWAKE_REALIZATION |                 32 |                  32 |             2313 |              876 |              883 |          35 |
| QMO_META                         |                 20 |                  20 |                0 |                0 |                0 |           0 |
| SOURCE_BACKFILL                  |                 19 |                  19 |               51 |               19 |               28 |           0 |
| STONEWAKE::QFT_GR                |                 16 |                  16 |               15 |                9 |               12 |           3 |
| ASTRAEUS_RAINBOW_ROAD            |                 12 |                  12 |                2 |                1 |                2 |           0 |
| VERA_LIVE_MODEL                  |                 12 |                  12 |                0 |                0 |                0 |           0 |
| CRD_QCD_INHERITANCE              |                 11 |                  11 |               11 |                9 |               10 |           0 |
| RAINBOW_ROAD_OVERLAY             |                 10 |                  10 |               30 |               10 |               29 |           5 |
| STONEWAKE::RAINBOW_ROAD          |                  9 |                   9 |                6 |                3 |                6 |           6 |
| STONEWAKE::STONEWAKE             |                  8 |                   8 |               12 |                5 |                6 |           0 |
| TRANSDUCTION_GEOMETRY            |                  7 |                   7 |                2 |                1 |                2 |           0 |
| PARENT_UNIFIED                   |                  6 |                   6 |                0 |                0 |                0 |           0 |
| BANDWIDTH_ALGEBRA                |                  1 |                   1 |                8 |                1 |                8 |           3 |
| SOURCE_ROOT_03                   |                  1 |                   1 |                0 |                0 |                0 |           0 |
| API43_TYPED                      |                  0 |                   0 |            75387 |              647 |              682 |           0 |

Schematic architecture:

\[
\widetilde V\xrightarrow{\pi}V\xrightarrow{E_0}V.
\]

Shared canonical handles therefore bridge provenance-distinct source domains without flattening them.

# 16. Meta-graph / self-description sector

The QMO contains

\[
\mathcal M\subset V
\]

with `@dependency_graph`, `@dependency_landscape`, `@dependency_closure`, `@dependency_composition`, `@dependency_preserving_map`, `@dependency_subgraph`, `@mathematical_graph`, `@ontological_graph`, `@representation_graph`, `@realization_graph`, `@proof_dependency_graph`, `@theorem_graph`, `@source_graph`, `@semantic_graph`, `@audit_graph`, and `@observational_graph`.

This is a self-descriptive vocabulary inside the QMO. It does not by itself prove a complete internal self-model.

# 17. Canonical definition

**Bidirectional Recursive QMO.** The current QMO is a finite provenance-bearing typed quiver with canonical-handle space \(V\), namespace-instance space \(\widetilde V\), witness family \(W\), canonical typed relation family \(E_0\), equation family \(\mathcal F\), provenance/status maps, source-preserving adjacency \(A_0\), reverse-query operator \(A_0^T\), bidirectional neighborhood operator \(\mathcal N_{A_0\lor A_0^T}\), and materialized non-reflexive directed reachability closure \(A^+\).

# 18. Dataset-level propositions

These propositions are about the stored finite QMO, not physical nature.

**Q1 — Witness completeness.** Every canonical typed edge has at least one provenance witness.

**Q2 — Weak connectedness.** The underlying undirected canonical graph is connected.

**Q3 — R8 fixed point.**
\[
\mathcal N_B^7(S_0)=V,\qquad \mathcal N_B^8(S_0)=V.
\]

**Q4 — Giant recurrent core.** A 1,260-handle SCC contains the full principal spine plus Higgs and dark-matter anchors.

**Q5 — Condensation acyclicity.** The SCC quotient is a DAG.

**Q6 — Directed closure radius.** Every stored derived closure pair has primitive directed shortest distance at most 15.

**Q7 — Traversal/semantics separation.** Reverse traversal is represented by \(A_0^T\) without inserting inverse source relations into \(E_0\).

# 19. One-equation compression

\[
\boxed{
\mathcal Q=
\operatorname{Fix}\left(
S\mapsto S\cup N_{A_0\lor A_0^T}(S)
\right)
}
\]

together with independent directed reachability

\[
\boxed{
A^+=\bigvee_{k\ge1}A_0^k.
}
\]

For this realization,

\[
\boxed{
|V|=1,459,\quad
|\widetilde V|=3,316,\quad
|\mathcal R|=355,\quad
|E_0|=79,624,\quad
|W|=160,057,\quad
|A^+|=1,801,233,\quad
|\mathcal F|=163.
}
\]

The first closure answers: **what belongs to the bidirectionally connected QMO generated by the seed?**

The second answers: **what is downstream-reachable through directed dependency structure?**

They are distinct operators over the same mathematical object.

# 20. Exhaustive finite map

The complete object is carried by:

- `NODE_LEDGER.csv` — every canonical handle with graph metrics, SCC, seed distance, namespace multiplicity, and equation count.
- `RELATION_LEDGER.csv` — every relation label and its edge/witness counts.
- `NAMESPACE_LEDGER.csv` — every namespace population.
- `EQUATION_LEDGER.csv` — every equation.
- `SCC_LEDGER.csv` and `SCC_MEMBERSHIP.csv` — every SCC and every member.
- `CANONICAL_TYPED_EDGES.tsv.gz` — all canonical typed edges.
- `SELF_CLOSURE_PAIRS.tsv.gz` — all derived reachability pairs.
- `CANONICAL_TYPED_GRAPH.graphml` — the full typed canonical graph.
- `CONDENSATION_DAG.graphml` — the SCC quotient.
- `FORMAL_MODEL.json` — machine-readable formal model.

Nothing in this formalization mutates the parent API or QMO.
