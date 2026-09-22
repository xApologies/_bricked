# Deterministic linkage

Normalized content hashes cover:

- module interfaces and GIR content;
- link-bundle export selection;
- backend capability manifest;
- alpha-renaming map;
- unified GIR graph;
- compiled GVM bytes.

Input file order does not define link order. The dependency DAG plus lexical tie-breaking does.
