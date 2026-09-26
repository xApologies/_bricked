# Full Equation Ledger

Equations indexed: 39

## @eq/block_direct_readout — Direct block readout

**Expression:** `C_block=trunc((1/32) sum_tau w(c_tau))`  
**Status:** CURRENT_TOY  
**Authority:** R61  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

Fine-grained direct toy average.

Notes: Compare to recursive readout.

## @eq/block_joint_space — Block joint space

**Expression:** `X_block subseteq (S1)^32`  
**Status:** PROVISIONAL  
**Authority:** R62  
**Source:** 03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md

Thirty-two occupied tile phases under block constraints.



## @eq/block_path — Block path

**Expression:** `Gamma:[0,1]->X_block`  
**Status:** CANDIDATE  
**Authority:** R61  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

Joint multiscale path.



## @eq/block_phase_space — Block phase space

**Expression:** `X_block subseteq (S1)^32`  
**Status:** PROVISIONAL_MODEL  
**Authority:** R61  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

Thirty-two occupied tile phases in half-occupied block.

Notes: Not physical dimension count.

## @eq/byte_joint_space — Byte joint space

**Expression:** `X_byte subseteq (S1)^4`  
**Status:** PROVISIONAL  
**Authority:** R62  
**Source:** 03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md

Four occupied tile phases under byte constraints.



## @eq/byte_phase_space — Byte phase space

**Expression:** `X_byte subseteq (S1)^4`  
**Status:** PROVISIONAL_MODEL  
**Authority:** R61  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

Four occupied tile phases under fixed occupancy.

Notes: Constrained domain.

## @eq/chirality_transport — Chirality transport

**Expression:** `chi(I^n(xi))=tau^n(chi(xi))`  
**Status:** PROVED_LEMMA  
**Authority:** Time-Space formal stack  
**Source:** 09_SOURCE_SNAPSHOTS/TIMESPACE_FORMAL_STACK/03_Lemmas.md

Inherited chirality transport.



## @eq/closure_idempotence — Closure idempotence

**Expression:** `R_c(R_c(Psi))=R_c(Psi)`  
**Status:** FORMAL_STACK  
**Authority:** Time-Space formal stack  
**Source:** 09_SOURCE_SNAPSHOTS/TIMESPACE_FORMAL_STACK/05_Interface_Definitions.md

Closure-stabilized condition.



## @eq/color_circle_phase — Tile color phase

**Expression:** `theta_tau in S1`  
**Status:** CANDIDATE  
**Authority:** R36/R62  
**Source:** 03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md

Continuous tile phase; discrete colors are sector readouts.



## @eq/color_weights — Color weights

**Expression:** `R=1,O=2,Y=3,G=4,B=5,V=6`  
**Status:** CURRENT_TOY  
**Authority:** Genesis live  
**Source:** 01_CANON/CANONICAL_CURRENT_STATE.md

Discrete toy weights.



## @eq/commutator — Commutator

**Expression:** `[A,B]=AB-BA`  
**Status:** INHERITED_TOOL  
**Authority:** standard algebra  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

Measures order dependence.



## @eq/corridor_operator — Chirality Corridor operator

**Expression:** `C_ab=Pi_b o P_W o L_a`  
**Status:** WORKING_FORMALIZATION  
**Authority:** Chirality Corridor  
**Source:** 09_SOURCE_SNAPSHOTS/TIMESPACE_FORMAL_STACK/corridor(1).md

Time-Shell lift, transport, target projection.



## @eq/crd_constraint — CRD local constraint

**Expression:** `delta x=f over Z_2`  
**Status:** CANDIDATE  
**Authority:** CRD source  
**Source:** @source/crd_relaxation

Candidate seam/backreaction closure condition.



## @eq/crd_relaxation — CRD relaxation functional

**Expression:** `Phi_chi(x;f)=sum_e c_e [x_u xor x_v != f_e]`  
**Status:** CANDIDATE  
**Authority:** CRD source  
**Source:** @source/crd_relaxation

Candidate local relaxation cost.



## @eq/decorated_transfer — Decorated transfer

**Expression:** `T_e(X)=x+delta_e(X)b_e`  
**Status:** CANDIDATE  
**Authority:** R60  
**Source:** 09_SOURCE_SNAPSHOTS/CURRENT_TANGENT/R60_NATIVE_UPDATE_MECHANISM_TANGENT.md

State/History-dependent transfer.

Notes: May be order-dependent.

## @eq/domain_color_readout — Domain color readout

**Expression:** `C(D)=trunc((1/N_D) sum_i w(c_i))`  
**Status:** CURRENT_TOY  
**Authority:** Genesis live  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

Current discrete coarse readout.

Notes: Continuous gradient later.

## @eq/domain_generator_map — Domain generator map

**Expression:** `Lambda_D:(F_D,A_D,B)->Gen_D(B)`  
**Status:** OPEN  
**Authority:** Propagation v8  
**Source:** 09_SOURCE_SNAPSHOTS/PROPAGATION_v8/CANONICAL_FULL_CONTINUITY_v8.md

Domain-relative generator construction.

Notes: Branch A/B unresolved.

## @eq/energy_density — Energy density

**Expression:** `rho_E=RT/V`  
**Status:** RECOVERED_API  
**Authority:** Unified API  
**Source:** 01_CANON/CANONICAL_CURRENT_STATE.md

Recovered API relation.

Notes: Do not merge with MK147 ladder.

## @eq/fixed_transfer — Fixed local transfer

**Expression:** `T_e,delta(x)=x+delta b_e`  
**Status:** SOURCE_DERIVED  
**Authority:** R16  
**Source:** 09_SOURCE_SNAPSHOTS/GENESIS_CHIRALITY_v9/R16_LOCAL_TILE_REDISTRIBUTION_KERNEL.md

R16 conservative edge redistribution.

Notes: White/midpoint working realization.

## @eq/fixed_transfer_commutes — Fixed-transfer commutativity

**Expression:** `T_f,eps o T_e,delta = T_e,delta o T_f,eps`  
**Status:** R60_RESULT  
**Authority:** R60  
**Source:** 09_SOURCE_SNAPSHOTS/CURRENT_TANGENT/R60_NATIVE_UPDATE_MECHANISM_TANGENT.md

Fixed additive transfers commute when both compositions admissible.



## @eq/helicon_q_handoff — Helicon-Q handoff

**Expression:** `Lambda_HQ:D_HQ ⇀ Q_loc`  
**Status:** OPEN_BLOCKER  
**Authority:** CRD->QCD v1.8  
**Source:** 09_SOURCE_SNAPSHOTS/CRD_QCD_v1_8/README.md

Source-respecting handoff target.



## @eq/joint_update_path — Joint update path

**Expression:** `Gamma_J(s)=(gamma_1(s),...,gamma_k(s))`  
**Status:** OPEN_CANDIDATE  
**Authority:** R62  
**Source:** 03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md

One coupled event across k tile phases.



## @eq/left_seed_profile — Left-handed seed profile

**Expression:** `[[1,0],[0,1]]`  
**Status:** WORKING  
**Authority:** Genesis live  
**Source:** 01_CANON/CANONICAL_CURRENT_STATE.md

Mirror occupancy profile.

Notes: Chromatic branch open.

## @eq/local_update_generator — Local chirality generator

**Expression:** `K_chi:(state,Adj,R,B,H,P,Sigma)->Gen_local`  
**Status:** OPEN  
**Authority:** R61  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

Active update-law target.



## @eq/multiscale_resolution_chain — Multiscale resolution chain

**Expression:** `tile path -> relation -> seed -> byte/bite -> block -> closure -> History`  
**Status:** WORKING_CANDIDATE  
**Authority:** R62  
**Source:** 03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md

Readable larger-domain change generated from local events.



## @eq/multiscale_update — Multiscale update

**Expression:** `U_chi:(K_t,Adj,R,B,H,P,Sigma) ⇀ (K_t+1,H_prime)`  
**Status:** WORKING_CANDIDATE  
**Authority:** R61  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

Partial decorated update operator.



## @eq/native_energy — Native energy unit

**Expression:** `epsilon_MK=Delta Pi_min`  
**Status:** RECOVERED_API  
**Authority:** Unified API  
**Source:** 01_CANON/CANONICAL_CURRENT_STATE.md

Minimum admissible persistence difference.



## @eq/persistence_functional — Persistence functional

**Expression:** `Pi=sum_d I_d B_d R_d O_d C_d`  
**Status:** RECOVERED_API  
**Authority:** Unified API  
**Source:** 01_CANON/CANONICAL_CURRENT_STATE.md

Organizational persistence accounting.

Notes: Symbol roles source-specific.

## @eq/persistence_locus — Persistence locus

**Expression:** `Xi={xi in E | exists n>=1: I^n(xi)~xi}`  
**Status:** FORMAL_STACK  
**Authority:** Time-Space formal stack  
**Source:** 09_SOURCE_SNAPSHOTS/TIMESPACE_FORMAL_STACK/02_Axioms.md

Recoverable organizational identity.



## @eq/qcd_commutator — QCD Lie algebra commutator

**Expression:** `[T^a,T^b]=i f^{abc}T^c`  
**Status:** EXTERNAL_COMPARISON  
**Authority:** standard QCD  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

External comparison fact.



## @eq/recursive_closure — Recursive continuity update

**Expression:** `Psi_(n+1)=R_c(O(Psi_n tensor T))`  
**Status:** FORMAL_STACK  
**Authority:** Time-Space formal stack  
**Source:** 09_SOURCE_SNAPSHOTS/TIMESPACE_FORMAL_STACK/05_Interface_Definitions.md

Interface recursive skeleton.

Notes: Not a specific tile update law.

## @eq/relationship_first_update — Relationship-first update

**Expression:** `endpoint change => incident relation change`  
**Status:** LOCKED_CONCEPT  
**Authority:** Propagation v8/R62  
**Source:** 01_CANON/CANONICAL_STATE_R62.md

Local tile change propagates relationally before larger-domain readout.

Notes: Not yet a complete numerical law.

## @eq/right_seed_profile — Right-handed seed profile

**Expression:** `[[0,1],[1,0]]`  
**Status:** WORKING  
**Authority:** Genesis live  
**Source:** 01_CANON/CANONICAL_CURRENT_STATE.md

Toy occupancy profile.



## @eq/seed_torus_path — Seed torus path

**Expression:** `gamma_seed:[0,1]->T2`  
**Status:** CANDIDATE  
**Authority:** R37/R62  
**Source:** 03_MATHEMATICS/TORUS_AND_MULTISCALE_UPDATE_MODEL.md

Joint two-tile History path.



## @eq/state_dependent_noncommutativity — State-dependent order test

**Expression:** `U_B(U_A(X)) != U_A(U_B(X))`  
**Status:** EXISTENCE_ONLY  
**Authority:** R60/R62  
**Source:** 03_MATHEMATICS/NATIVE_UPDATE_FRONTIER.md

Possible when first event changes second event availability.

Notes: Not a canonical law.

## @eq/su3_dimension — SU3 generator dimension

**Expression:** `dim SU(3)=3^2-1=8`  
**Status:** EXTERNAL_COMPARISON  
**Authority:** standard QCD  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

External comparison fact.

Notes: No derivation claim.

## @eq/torus_seed_space — Seed torus

**Expression:** `T2=S1_A x S1_B`  
**Status:** STRONG_CANDIDATE  
**Authority:** R36-R37  
**Source:** 09_SOURCE_SNAPSHOTS/GENESIS_CHIRALITY_v9/R37_T2_LOCAL_CONTINUITY.md

Two occupied tile color phases.

Notes: Local only.

## @eq/torus_update — Torus transport

**Expression:** `(theta_A,theta_B)->(theta_A+Delta_A,theta_B+Delta_B) mod 2pi`  
**Status:** CANDIDATE  
**Authority:** R61  
**Source:** 04_MATHEMATICS/R61_MULTISCALE_TORUS_UPDATE_FORMALIZATION.md

General local phase displacement.

Notes: Selector open.

## @eq/torus_winding — Torus winding

**Expression:** `pi_1(T2)=Z x Z`  
**Status:** PROVED_INHERITED_MATH  
**Authority:** R37  
**Source:** 09_SOURCE_SNAPSHOTS/GENESIS_CHIRALITY_v9/R37_T2_LOCAL_CONTINUITY.md

Winding History carrier.

Notes: Not complete History.
