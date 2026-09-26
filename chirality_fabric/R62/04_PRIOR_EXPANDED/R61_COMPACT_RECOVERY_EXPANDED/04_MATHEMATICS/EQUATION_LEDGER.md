# EQUATION LEDGER

| Address | Expression | Status |
|---|---|---|
| `@eq/right_seed_profile` | `[[0,1],[1,0]]` | working structural profile |
| `@eq/left_seed_profile` | `[[1,0],[0,1]]` | working mirror profile; chromatic branch open |
| `@eq/color_weights` | `R=1,O=2,Y=3,G=4,B=5,V=6` | current toy model |
| `@eq/domain_color_readout` | `C(D)=trunc((1/N) sum_i w(c_i))` | current toy readout |
| `@eq/torus_seed_space` | `T2=S1_A x S1_B` | strong local continuity model |
| `@eq/torus_update` | `(theta_A,theta_B)->(theta_A+Delta_A,theta_B+Delta_B) mod 2pi` | candidate transport form |
| `@eq/torus_winding` | `pi_1(T2)=Z x Z` | standard topological result applied locally |
| `@eq/byte_phase_space` | `X_byte subseteq (S1)^4` | provisional fixed-occupancy model |
| `@eq/block_phase_space` | `X_block subseteq (S1)^32` | provisional half-occupancy model |
| `@eq/block_path` | `Gamma:[0,1]->X_block` | candidate evolution object |
| `@eq/block_direct_readout` | `C_block=trunc((1/32) sum_tau w(c_tau))` | toy direct readout |
| `@eq/fixed_transfer` | `T_e,delta(x)=x+delta b_e` | R16 source-derived transfer family |
| `@eq/fixed_transfer_commutes` | `T_f,eps o T_e,delta = T_e,delta o T_f,eps` | R60 result under fixed admissible parameters |
| `@eq/decorated_transfer` | `T_e(X)=x+delta_e(X)b_e` | candidate context-dependent form |
| `@eq/commutator` | `[A,B]=AB-BA` | inherited comparison tool |
| `@eq/recursive_closure` | `Psi_(n+1)=R_c(O(Psi_n tensor T))` | interface-layer recursive skeleton |
| `@eq/closure_idempotence` | `R_c(R_c(Psi))=R_c(Psi)` | formal stack |
| `@eq/chirality_transport` | `chi(I^n(xi))=tau^n(chi(xi))` | proved lemma in uploaded formal stack |
| `@eq/persistence_locus` | `Xi={xi in E | exists n>=1: I^n(xi)~xi}` | formal stack |
| `@eq/corridor_operator` | `C_ab=Pi_b o P_W o L_a` | Chirality Corridor working definition |
| `@eq/crd_constraint` | `delta x=f` over `Z_2` | CRD candidate closure diagnostic |
| `@eq/crd_relaxation` | `Phi_chi(x;f)=sum_e c_e [x_u xor x_v != f_e]` | CRD candidate relaxation functional |
| `@eq/native_energy` | `epsilon_MK=Delta Pi_min` | recovered API object |
| `@eq/persistence_functional` | `Pi=sum_d I_d B_d R_d O_d C_d` | recovered API relation |
| `@eq/energy_density` | `rho_E=RT/V` | recovered API relation; symbol meanings source-specific |
| `@eq/domain_generator_map` | `Lambda_D:(F_D,A_D,B)->Gen_D(B)` | Propagation R88 open map |
| `@eq/local_update_generator` | `K_chi:(state,Adj,R,B,H,P,Sigma)->Gen_local` | R61 active target |
| `@eq/helicon_q_handoff` | `Lambda_HQ:D_HQ ⇀ Q_loc` | CRD->QCD v1.8 principal blocker |
| `@eq/su3_dimension` | `dim SU(3)=3^2-1=8` | external comparison only |
| `@eq/qcd_commutator` | `[T^a,T^b]=i f^{abc}T^c` | external comparison only |
