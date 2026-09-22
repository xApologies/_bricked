# Scientific 3+1+1 Adapter

Current mapped molecular packages may expose a chirality field shaped:

`(X, Y, Z, 2, 2)`

This section treats it as a scientific representation with explicit axes. It does not declare the last two axes to be BRANE dimensions or a 2x2x2 mote.

## Loss-aware execution projection

The default `MMO_3P1P1_DENSE_V1` profile maps one spatial voxel to five hardware cells:

```text
role 0 : chi[0,0]
role 1 : chi[0,1]
role 2 : chi[1,0]
role 3 : chi[1,1]
role 4 : control summary
```

The four component values are quantized to Q0.16 in the hardware cell chirality-magnitude field. Their role offset remains explicit in the binding manifest.

The control summary may encode only source-supported values:

- signed chirality scalar -> handedness + chirality magnitude;
- admissibility array -> sigma;
- persistence array -> rho;
- resolution array -> tau **only when the selected adapter profile explicitly declares resolution-as-readout-readiness**;
- unknown values remain zero/unknown and are flagged.

The original scientific arrays remain hash-addressed and are the authority for exact numerical analysis. The hardware projection is an execution representation.
