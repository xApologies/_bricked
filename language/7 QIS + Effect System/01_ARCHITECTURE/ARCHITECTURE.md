# Section 07 architecture

```text
MMO / Geometric
      |
      | QFT readout / quantum-information attachment
      v
Quantum State Handle
      |
      +-- linear ownership / no cloning
      +-- superposition
      +-- entanglement graph
      +-- unitary / channel effects
      +-- measurement / classicalization
      |
      v
Portal<QFT> Quantum Effect Envelope
      |
      v
Corridor admission + Rainbow Road transport
      |
      +-- QFT -> QFT: quantum-preserving effects MAY be declared if the channel contract admits them
      |
      +-- QFT -> GR: Section 06 Bridge is representation transduction only;
                    quantum coherence/entanglement do not automatically cross
      v
Closure Receipt + History + Provenance + BRANE M5 effect lift
```

## Central rule
Genesis does not treat a quantum state as a copyable Python value. A nonclassical state is an owned resource with a lifecycle. Operations must declare what they preserve, consume, measure, decohere, or classicalize.

## Why this exists
The future Genesis language is Portal-native and information-transformational. Quantum programming languages already supply mature semantics for coherent state transformation, joint states, measurement, channels, and linear ownership. Section 07 inherits those semantics only where they solve an actual Genesis problem.
