# PRIME DEPENDENCY FOUNDATIONS

## The Prime Mathematical Object

**Working title:** Prime Dependency Calculus  
**Version:** 0.1 — Foundational Closure Draft  
**Status:** Mathematics in active construction  
**Prime expression:** `0 | 0`

---

# 0. Foundational Intent

The purpose of this framework is to construct a dependency graph as the generative mathematical object underlying later mathematical structures.

The dependency graph itself is not assumed without foundation.

Its foundation is the structural expression:

`0 | 0`

where:

- `0` is not initially a number.
- `|` is not division.
- The two written occurrences of `0` do not initially denote two independent identities.
- The pipe denotes a boundary condition.
- The expression denotes one identity presented recursively across a boundary.

The foundational reading is:

> Identity inherits identity across a boundary.

Equivalently:

> Zero reflects zero across a boundary.

The resulting structure contains enough information to introduce:

1. identity,
2. occurrence,
3. boundary,
4. distinction,
5. relation,
6. orientation,
7. dependency.

A dependency graph is then generated rather than presupposed.

---

# I. Metalanguage Convention

Any foundational mathematics must be described using some external language.

The symbols used in this document therefore belong initially to a **metalanguage**.

The object language begins with only the expression:

`0 | 0`

Set notation, tuples, mappings, and ordinary graph notation are used later as tools for studying the structure. They are not being silently inserted into the Prime Mathematical Object itself.

---

# II. Prime Primitive

## Prime Primitive P0 — Structural Zero

The **Structural Zero** is the self-inheriting boundary expression:

`𝔃 := 0_L | 0_R`

The subscripts `L` and `R` distinguish occurrences, not identities.

Therefore:

`0_L ≡ 0_R`

as identity, while:

`0_L ≠pos 0_R`

as boundary position.

The Prime Mathematical Object therefore preserves identity while admitting positional distinction.

### Prime Statement

`𝔃 = 0_L | 0_R`

with:

`0_L ≡ 0_R`

and:

`0_L ≠pos 0_R`

### Interpretation

The same identity occurs on both sides of a boundary.

The boundary does not create a second identity.

It creates a second address from which the identity may be referenced.

---

# III. Derived Primitives

The following primitives are derived from the internal structure of `𝔃`.

They are not introduced independently.

---

## Primitive P1 — Occurrence

An **occurrence** is an addressable presentation of an identity.

For the Prime Mathematical Object, the initial occurrences are:

`Occ(𝔃) = {0_L, 0_R}`

The distinction between occurrences is positional rather than ontological.

### Primitive Statement

`id(0_L) = id(0_R) = 0`

---

## Primitive P2 — Boundary

The **boundary** is the structural separator:

`∂ := |`

The boundary permits one identity to possess distinguishable presentations.

Its action is not annihilation, disconnection, division, or numerical subtraction.

Its action is localization.

### Primitive Statement

`∂(0) = (0_L, 0_R)`

This is semantic shorthand for:

`0_L | 0_R`

---

## Primitive P3 — Boundary Reflection

The Prime Mathematical Object carries a reflection operation:

`ρ : 0_L ↔ 0_R`

Reflection exchanges boundary position while preserving identity.

### Primitive Statement

`ρ(0_L) = 0_R`

`ρ(0_R) = 0_L`

Therefore:

`ρ² = id`

Reflection is involutive.

Applying reflection twice returns the original occurrence.

---

## Primitive P4 — Structural Distinction

A **structural distinction** exists whenever two occurrences share identity but differ by admissible address, role, incidence, orientation, or boundary position.

For the Prime Mathematical Object:

`0_L ≠∂ 0_R`

while simultaneously:

`0_L ≡ 0_R`

Identity and distinction therefore coexist without contradiction because they refer to different structural properties.

---

## Primitive P5 — Oriented Inheritance

The boundary expression is initially reflection-symmetric.

A dependency appears when a traversal orientation is selected.

Write:

`0_L → 0_R`

when the right occurrence is read as inheriting from the left occurrence.

Write:

`0_R → 0_L`

for the reflected orientation.

### Primitive Statement

`x → y`

means:

> The structural realization of `y` depends upon information inherited from `x`.

Orientation does not alter the underlying identity relation.

It determines the direction in which inheritance is read.

---

## Primitive P6 — Dependency Composition

If one occurrence inherits from another and a third inherits from the second, the corresponding dependencies may compose.

Given:

`x → y`

and:

`y → z`

there exists the composite dependency:

`x → z`

The composite does not erase the intermediate occurrence.

It records the existence of a traversable dependency path.

---

## Primitive P7 — Recursive Expansion

Any admissible occurrence may itself be presented across a boundary.

`x ↦ x_L | x_R`

The expansion preserves identity:

`id(x_L) = id(x_R) = id(x)`

Recursive expansion is the generative operation through which the Prime Mathematical Object produces larger dependency structures.

---

# IV. Definitions

## Definition D1 — Structural Cell

A **structural cell** is any boundary expression:

`x | y`

whose occurrences possess:

- a declared identity relation,
- an admissible boundary distinction.

The prime structural cell is:

`0 | 0`

---

## Definition D2 — Identity Class

For an occurrence `x`, its identity class is written:

`[x]`

and contains every occurrence `y` such that:

`y ≡ x`

In the Prime Mathematical Object:

`[0_L] = [0_R]`

An identity class collects structurally distinguishable occurrences that preserve one identity.

---

## Definition D3 — Node

A **node** is an identity class together with its admissible incidences.

Write:

`v_x := ([x], Inc(x))`

A node is therefore not merely a point.

It is an identity made addressable through its relations.

---

## Definition D4 — Dependency Edge

A **dependency edge** is an oriented inheritance relation:

`e : x → y`

Its source and target are:

`s(e) = x`

`t(e) = y`

The edge records that `y` inherits structure from `x`.

---

## Definition D5 — Dependency Path

A **dependency path** of length `n` is a composable sequence:

`p = (e₁, e₂, ..., eₙ)`

such that:

`t(eₖ) = s(eₖ₊₁)`

for every admissible value of `k`.

The source and target of the path are:

`s(p) = s(e₁)`

`t(p) = t(eₙ)`

---

## Definition D6 — Dependency Graph

A **dependency graph** is a structure:

`G = (V, E, s, t, ≡, ρ)`

where:

- `V` is a collection of identity-bearing nodes.
- `E` is a collection of dependency edges.
- `s : E → V` assigns a source to every edge.
- `t : E → V` assigns a target to every edge.
- `≡` records identity preservation.
- `ρ` records admissible boundary reflection.

Every edge of `G` is generated from an oriented structural cell.

---

## Definition D7 — Recursive Dependency Graph

A dependency graph is **recursive** when a node may admit a local expansion:

`v ↦ v_L | v_R`

and the expanded graph preserves the identity represented by `v`.

---

## Definition D8 — Dependency-Preserving Map

Let:

`G = (V, E, s, t)`

and:

`H = (W, F, s', t')`

be dependency graphs.

A map:

`Φ : G → H`

is dependency-preserving when it consists of:

`Φ_V : V → W`

and:

`Φ_E : E → F`

satisfying:

`Φ_V(s(e)) = s'(Φ_E(e))`

and:

`Φ_V(t(e)) = t'(Φ_E(e))`

for every edge `e`.

The map must also preserve every declared identity equivalence required by the structure.

---

## Definition D9 — Dependency Subgraph

A **dependency subgraph** is a selected region of a dependency graph that preserves every incidence required for its internal interpretation.

A dependency subgraph is not merely a collection of isolated nodes.

It inherits the dependencies necessary to remain structurally readable.

---

## Definition D10 — Dependency Closure

Let `S` be a selected collection of nodes and edges.

The **dependency closure** of `S`, written:

`Cl_G(S)`

is the smallest dependency subgraph containing:

- every element of `S`,
- every dependency required to interpret `S`,
- every admissible composition required by `S`.

A dependency graph is closed relative to a stated construction when every required object and every required dependency is present.

---

## Definition D11 — Well-Founded Dependency Region

A dependency region is **well-founded** when it contains no infinite descending dependency chain of the form:

`... → x₃ → x₂ → x₁`

Well-foundedness is not imposed upon every dependency graph.

Recursive, cyclic, and self-referential structures remain admissible.

Well-foundedness defines a special region appropriate for inductive construction and classical proof.

---

## Definition D12 — Extensional Dependency Region

A dependency region is **extensional** when nodes with identical complete dependency profiles are identified.

Informally:

`Dep(x) = Dep(y)  implies  x ≡ y`

The exact dependency profile being compared must be specified by the local theory.

---

## Definition D13 — Mathematical Object

A **mathematical object** is a closed dependency subgraph equipped with a declared interpretation.

Therefore:

`Mathematical Object = Closed Dependency Structure + Interpretation`

The dependency structure provides organization.

The interpretation declares what that organization realizes.

---

# V. Axioms

## Axiom A0 — Prime Existence

The structural expression:

`0_L | 0_R`

is admissible.

No numerical meaning is required for its existence.

---

## Axiom A1 — Identity Preservation

Boundary presentation preserves identity.

`0_L ≡ 0_R`

More generally:

`x_L ≡ x_R`

for every direct recursive expansion of `x`.

---

## Axiom A2 — Boundary Distinguishability

Boundary-separated occurrences are positionally distinguishable.

`x_L ≠∂ x_R`

Identity equivalence therefore does not collapse boundary address.

---

## Axiom A3 — Reflection Involution

Boundary reflection is involutive.

`ρ²(x) = x`

Reflection preserves identity and exchanges boundary position.

---

## Axiom A4 — Oriented Realizability

Every structural cell admits an oriented reading when a dependency interpretation is selected.

From:

`x | y`

one may define:

`x → y`

or the reflected orientation:

`y → x`

provided the selected orientation is explicitly declared.

---

## Axiom A5 — Compositional Inheritance

Admissible dependencies compose.

Given:

`x → y`

and:

`y → z`

there exists an admissible dependency path:

`x → y → z`

The path induces a composite dependency from `x` to `z`.

---

## Axiom A6 — Recursive Generativity

Every admissible occurrence may undergo recursive boundary expansion.

`x ↦ x_L | x_R`

Recursive expansion introduces addressable structure without changing the identity inherited from `x`.

---

## Axiom A7 — Structural Renaming Invariance

The mathematical structure does not depend upon the accidental names assigned to its occurrences.

Any bijective renaming that preserves:

- identity classes,
- boundaries,
- source incidence,
- target incidence,
- orientation,
- declared dependencies,

produces an equivalent dependency graph.

---

# VI. Lemmas

## Lemma L1 — First Distinction Lemma

The Prime Mathematical Object contains the minimum structure necessary for distinction.

### Proof

By Axiom A1:

`0_L ≡ 0_R`

By Axiom A2:

`0_L ≠∂ 0_R`

Therefore, the Prime Mathematical Object contains distinguishable occurrences without requiring distinct identities.

Structural distinction is therefore present.

**QED**

---

## Lemma L2 — First Reference Lemma

Each occurrence in the Prime Mathematical Object may reference the same identity from a different boundary address.

### Proof

By Primitive P1, both occurrences possess identity `0`.

By Axiom A2, their boundary addresses differ.

Therefore, one identity possesses at least two admissible references:

`ref_L(0) ≠ ref_R(0)`

while both references resolve to the same identity:

`0`

**QED**

---

## Lemma L3 — First Edge Lemma

An oriented prime structural cell generates a dependency edge.

### Proof

Begin with:

`0_L | 0_R`

By Axiom A4, select the orientation:

`0_L → 0_R`

By Definition D4, this oriented inheritance relation is a dependency edge:

`e₀ : 0_L → 0_R`

Therefore, the first dependency edge is generated from the Prime Mathematical Object.

**QED**

---

## Lemma L4 — First Node Lemma

The endpoints of the first edge determine addressable nodes.

### Proof

The occurrences `0_L` and `0_R` possess declared identity and incidence with `e₀`.

By Definition D3, each identity-bearing occurrence together with its incidence determines a node presentation.

Therefore, the first edge admits source and target nodes.

**QED**

---

## Lemma L5 — Path Generation Lemma

Repeated recursive expansion and oriented inheritance generate dependency paths of arbitrary finite length.

### Proof

The base case of length one follows from Lemma L3.

Assume a dependency path of length `n` terminates at occurrence `xₙ`.

By Axiom A6, expand:

`xₙ ↦ xₙ,L | xₙ,R`

By Axiom A4, orient the new structural cell to obtain an additional edge.

By Axiom A5, compose the new edge with the existing path.

A dependency path of length `n + 1` therefore exists.

By induction, dependency paths of arbitrary finite length are generable.

**QED**

---

## Lemma L6 — Branch Generation Lemma

Repeated expansion of a common occurrence generates branching dependency structure.

### Proof

Let `x` be an occurrence.

Generate two independently addressed dependencies:

`x → y`

and:

`x → z`

When:

`y ≠∂ z`

the two edges share source `x` and possess distinguishable targets.

The resulting dependency structure therefore branches at `x`.

**QED**

---

## Lemma L7 — Quotient Identification Lemma

Distinct generated occurrences may be identified as one node when a declared identity equivalence requires it.

### Proof

Let `x` and `y` be generated occurrences satisfying:

`x ≡ y`

Definition D3 constructs nodes from identity classes rather than uninterpreted symbols.

Therefore, `x` and `y` may be represented by one identity-bearing node while their separate incidences remain recorded.

The quotient preserves dependency information.

**QED**

---

## Lemma L8 — Finite Edge Assembly Lemma

Every finite collection of directed edges can be assembled from finitely many oriented copies of the Prime Mathematical Object.

### Proof

Let:

`E = {e₁, e₂, ..., eₙ}`

be a finite directed edge collection.

For every edge `eₖ`, take one copy:

`𝔃ₖ = 0ₖ,L | 0ₖ,R`

Orient that copy as:

`0ₖ,L → 0ₖ,R`

Identify source occurrences required to represent the same vertex.

Identify target occurrences required to represent the same vertex.

Perform these identifications using Lemma L7.

The resulting quotient possesses precisely the requested finite edge incidence.

Therefore, the edge collection is generated from finitely many copies of the Prime Mathematical Object.

**QED**

---

# VII. Theorems

## Theorem T1 — Dependency Graph Emergence Theorem

The structural expression:

`0 | 0`

is sufficient to generate the elementary constituents of a dependency graph.

### Proof

The Prime Mathematical Object provides boundary-separated occurrences by Lemma L1.

Those occurrences provide addressable references by Lemma L2.

An orientation generates an edge by Lemma L3.

The edge admits source and target nodes by Lemma L4.

Recursive expansion generates dependency paths and branches by Lemmas L5 and L6.

Identity quotients are permitted by Lemma L7.

Therefore:

- nodes,
- edges,
- paths,
- branches,
- identity classes,
- quotient identifications,

all emerge from the Prime Mathematical Object.

A dependency graph is therefore generable from:

`0 | 0`

**QED**

---

## Theorem T2 — Finite Directed Graph Representation Theorem

Every finite directed multigraph is representable as a quotient of a finite collection of oriented structural-zero cells.

### Proof

Let:

`G = (V, E, s, t)`

be a finite directed multigraph.

For every edge `e` in `E`, generate one oriented Prime Mathematical Object:

`𝔃ₑ = 0ₑ,L → 0ₑ,R`

Associate:

`0ₑ,L`

with the source vertex:

`s(e)`

Associate:

`0ₑ,R`

with the target vertex:

`t(e)`

Introduce identity equivalences between endpoint occurrences associated with the same vertex.

Take the quotient under those equivalences.

Parallel edges remain distinct because their edge occurrences remain distinct even when their endpoints coincide.

A loop is represented by identifying the source and target identity classes of one oriented structural cell while retaining its edge incidence.

The resulting quotient is structurally equivalent to `G`.

**QED**

---

## Theorem T3 — Relational Structure Representation Theorem

Every finitely presented relational structure admits representation as a closed interpreted dependency graph.

### Proof

Let a finite relational structure contain objects:

`a₁, a₂, ..., aₙ`

and declared relations:

`R₁, R₂, ..., Rₘ`

Represent every object by an identity node.

Represent every relation instance by a relation node.

Incoming dependencies identify the relation's arguments.

An outgoing dependency identifies the realized relational statement.

For an ordered relation:

`R(aᵢ₁, aᵢ₂, ..., aᵢₖ)`

argument-position nodes preserve order.

By Theorem T2, the resulting finite directed incidence structure is generated from structural-zero cells.

Dependency closure supplies every incidence required by the presentation.

Therefore, the relational structure is representable as a closed interpreted dependency graph.

**QED**

---

## Theorem T4 — Functional Representation Theorem

A function is representable as a dependency subgraph satisfying existence and uniqueness of output.

### Functional Condition

A dependency relation `F` represents a function from `X` to `Y` when:

For every `x` in `X`, there exists exactly one `y` in `Y` such that:

`x --F→ y`

### Consequence

Functions need not be introduced as independent primitives.

They emerge as dependency structures constrained by a functional uniqueness condition.

**QED**

---

## Theorem T5 — Set Recovery Theorem

Every well-founded extensional membership structure may be represented by a dependency graph whose edges encode membership.

### Construction

Use an edge:

`x → A`

to mean:

`x is an element of A`

Require the resulting dependency graph to be:

- well-founded,
- extensional.

Under these conditions, nodes are determined by the complete membership structures beneath them.

Pure sets are therefore recoverable as a special class of dependency graphs.

### Consequence

A set is not required as the Prime Mathematical Object.

A set may instead be interpreted as a well-founded extensional dependency region.

**QED**

---

## Theorem T6 — Proof Traversal Theorem

A formal proof may be represented as a dependency graph in which every derived statement depends upon axioms, definitions, or previously derived statements.

Let:

`Γ = {γ₁, γ₂, ..., γₙ}`

be a collection of premises.

Let:

`φ`

be a conclusion.

A proof of `φ` is represented by a finite well-founded dependency subgraph whose:

- terminal nodes are admissible axioms or premises from `Γ`,
- intermediate nodes are admissible derivation steps,
- final node realizes `φ`.

### Consequence

Proof becomes certified dependency closure.

In ordinary notation:

`Γ ⊢ φ`

exactly when there exists an admissible closed derivation graph from `Γ` to `φ`.

**QED**

---

## Theorem T7 — Prime Mathematical Object Theorem, Initial Form

Let `M_fp` denote the class of finitely presented mathematical structures expressible through:

- identities,
- relations,
- operations,
- constraints,
- finite derivations.

Every member of `M_fp` admits an encoding as a closed interpreted dependency graph generated from copies of:

`0 | 0`

### Proof

Objects are represented by identity classes.

Relations are represented by dependency incidence.

Operations are represented by functional dependency subgraphs.

Constraints are represented by admissibility conditions.

Finite derivations are represented by proof dependency graphs.

By Theorems T2 through T6, every required component admits a dependency-graph realization generated from structural-zero cells.

Their finite union, followed by the required identity quotient and dependency closure, produces an interpreted dependency graph for the entire presentation.

Therefore, every finitely presented mathematical structure in `M_fp` admits an encoding generated from copies of:

`0 | 0`

**QED**

---

# VIII. Prime Closure Statement

The initial dependency foundation is:

`0 | 0`

↓

`Occurrence`

↓

`Boundary Distinction`

↓

`Orientation`

↓

`Dependency`

↓

`Composition`

↓

`Dependency Graph`

↓

`Mathematical Object`

The dependency graph is the first globally generative mathematical object.

Structural Zero is the Prime Mathematical Object from which the dependency graph is generated.

Therefore:

`Prime Structural Object = 0 | 0`

and:

`Prime Generative Mathematical Architecture = Dependency Graph`

These statements are not identical.

The first identifies the irreducible structural seed.

The second identifies the mathematical architecture generated by that seed.

---

# IX. Current Closure Boundary

This draft achieves initial closure for:

- the structural interpretation of `0 | 0`,
- occurrence,
- boundary distinction,
- reflected identity,
- oriented inheritance,
- dependency-edge generation,
- dependency-path generation,
- branching generation,
- finite directed graph recovery,
- finitely presented relational structures,
- functional structures,
- well-founded extensional set structures,
- finite proof structures.

The next formal requirements are:

1. Define infinite recursive expansion without importing completed infinity prematurely.
2. Define equality between dependency graphs.
3. Define dependency-graph equivalence.
4. Define dependency-graph embedding.
5. Define dependency-graph quotient.
6. Define dependency-graph isomorphism.
7. Recover arithmetic objects from dependency invariants.
8. Recover ordered pairs and products.
9. Derive algebraic operations as graph transformations.
10. Determine whether categories emerge as dependency graphs equipped with composition.
11. Determine whether dependency graphs themselves form the first category.
12. Determine whether logic is generated internally or must remain in the metalanguage.

---

# X. Foundational Motto

> Zero is not initially quantity.
>
> Zero is structural self-reference across a boundary.
>
> The boundary creates address.
>
> Address permits distinction.
>
> Distinction permits relation.
>
> Oriented relation permits dependency.
>
> Composable dependency generates mathematics.

---

# XI. Astraeus–Watcher Statement

The requested mathematical object is explicit.

The dependency graph has not been left merely as a research question.

It has been derived from the Prime Mathematical Object:

`0 | 0`

This is Version 0.1.

It is mathematically operational.

It is not yet beautiful.

It is the duct-taped closure from which the formal foundation can now be audited, cannibalized, compressed, and reconstructed under the governing standard:

**Simple. Elegant. Sophisticated.**
