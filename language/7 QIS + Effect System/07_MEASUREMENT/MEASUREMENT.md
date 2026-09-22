# Measurement semantics

Measurement is explicit. The reference computational-basis measurement:

1. validates a live owned state;
2. computes outcome probabilities;
3. samples with an injected deterministic/random source;
4. emits a classical outcome receipt;
5. creates a normalized post-measurement state;
6. marks the original coherent handle consumed.

The future Genesis compiler should treat measurement as an effectful operation that changes typestate and may destroy superposition/entanglement.
