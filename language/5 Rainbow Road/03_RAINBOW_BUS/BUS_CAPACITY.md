# Rainbow Bus Capacity Manager

The **Rainbow Bus** is the implementation capacity fabric available to Portal/Road scheduling.

Section 05 adds a Road-level lease:

1. preflight every Portal leg;
2. compute the maximum sequential capacity required for each Corridor edge;
3. reserve those units in the underlying Section-04 capacity ledger;
4. expose the reserved pool to each Portal leg;
5. let Portal sub-reservations consume/release units inside the Road pool;
6. release the Road lease only after Road closure/failure.

This prevents a Road from passing preflight and then losing a required Corridor to an unrelated transaction mid-run.

**Important:** scheduling capacity is intentionally distinct from mathematical Bandwidth. A Road must pass both.
