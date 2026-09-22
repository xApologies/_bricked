# Genesis Chirality Machine ISA-0

ISA-0 is a semantic machine ISA. It is not a CPU microarchitecture.

## Register classes

- `G0..G15` — Geometric/object handles
- `A0..A15` — Fabric addresses
- `C0..C7` — Chirality state/constraint handles
- `R0..R7` — Relationship handles
- `P0..P7` — Portal handles
- `S` — status/effect register

## Core opcodes

### Fabric / object
- `FIDENT dst` — load mounted fabric identity
- `FADDR dst, page, cell, lane` — construct FabricAddress
- `FREAD dstG, srcA` — read operative cell view
- `GREGION dstG, startA, count` — bind Geometric region
- `GSTAGE dstA, srcG` — stage dynamic cell into overlay
- `GCOMMIT dstG` — commit overlay transaction and return receipt

### Relationship / chirality
- `RELATE dstR, srcG1, srcG2`
- `CHI_LOAD dstC, srcG`
- `CHI_COMPARE dstS, srcC1, srcC2`
- `ADMIT dstS, srcR, srcC`
- `INHERIT dstG, srcG, history_ref`

### Transformation
- `XFORM dstG, srcG, transform_id`
- `PROJECT dstG, srcG, projector_id`
- `TRANSDUCE dstG, srcG, transducer_id`

### Portal / transport
- `POPEN dstP, sourceG, destinationG, sector`
- `PXFER dstG, portalP, payloadG`
- `PCLOSE dstG, portalP`
- `RECEIPT dstG, portalP`

### Realization
- `BRANE dstG, srcG, request_context`
- `HALT`

## Fabric write prohibition

No ISA-0 opcode writes to base Fabric ROM. `GSTAGE/GCOMMIT` operate on the runtime overlay. A separate privileged `CHECKPOINT` tool can materialize a new derived fabric artifact.
