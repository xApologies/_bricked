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
