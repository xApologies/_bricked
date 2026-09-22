# Physical State Codec

The hardware interface intentionally separates a semantic class from its physical carrier.

```text
StateClass -> EncodedLevel -> physical storage -> ReadLevel -> StateClass
```

A codec declares:

- codebook version;
- number of stable levels;
- write tolerance;
- read thresholds;
- calibration provenance;
- ECC/readback policy;
- whether the carrier is volatile or nonvolatile.

### Emulator codec

The reference emulator provides a normalized 8-level codebook in `[0,1]`. It is a model of multilevel storage, not a claim about a particular commercial SSD's raw voltages.

### Custom hardware codec

A future FPGA/analog backend may map classes to DAC/ADC targets, resistive states, magnetic states, optical levels, charge windows, or another physical mechanism.
