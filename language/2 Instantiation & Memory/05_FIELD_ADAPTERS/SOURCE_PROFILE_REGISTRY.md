# Source Profile Registry

Version 0.1 contains adapters for the currently mounted reference formats:

- `HSV1_V028`: `(32,32,32,2,2)` chirality field + scalar + occupancy + persistence + resolution + mass density.
- `HYDROGEN_V2`: signed scalar chirality + explicit environment admissibility and closure/topology fields.
- `OXYGEN_PHASE5_V1`: signed chirality scalar + source/setlift representations.
- `BLANK_MANIFOLD_V0_1`: state-code scaffold with no atomic topology.
- `GENERIC_3P1P1`: generic `(X,Y,Z,2,2)` source with optional support arrays.

Adapter names describe file-layout compatibility, not biological or physical validation.
