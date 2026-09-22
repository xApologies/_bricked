# Portal Lowering Sketch

A future Genesis statement:

```text
portal P from MMO_A to MMO_B
    preserve identity provenance
    transform field
    close
```

may lower through Layer Zero to GCM operations approximately as:

```text
GREGION G0, MMO_A_REGION
GREGION G1, MMO_B_REGION
RELATE R0, G0, G1
CHI_LOAD C0, G0
ADMIT S, R0, C0
POPEN P0, G0, G1, SECTOR
PXFER G2, P0, G0
PCLOSE G3, P0
RECEIPT G4, P0
```

The hardware layer does not decide the scientific meaning of the Portal; it provides the execution substrate and immutable fabric identity.
