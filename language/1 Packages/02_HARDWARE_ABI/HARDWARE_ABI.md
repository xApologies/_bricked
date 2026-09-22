# Genesis Chirality Hardware Interface (GCHI) v0.1

GCHI is the stable interface between the Genesis Chirality Machine and any physical/emulated substrate.

## ABI objects

- `FabricIdentity`
- `FabricAddress`
- `ChiralityCell32`
- `PhysicalStateCodec`
- `FabricBackend`
- `OverlayBackend`
- `FabricMount`
- `FabricReceipt`

## FabricAddress128

128-bit logical physical-address token:

```text
bits 127..64 : fabric_tag  (u64; first 64 bits of immutable fabric identity digest)
bits  63..32 : page        (u32)
bits  31..16 : cell        (u16; cell index within page)
bits  15.. 8 : lane        (u8; subcell/channel selector)
bits   7.. 0 : flags       (u8)
```

It is intentionally not claimed to be a raw NAND page or disk-platter sector. Backends map it to their own physical address mechanism.

## Access classes

- `READ_FABRIC`: read immutable substrate state.
- `READ_OVERLAY`: read runtime override if present.
- `STAGE_OVERLAY`: stage a new dynamic state.
- `COMMIT_OVERLAY`: append receipt and make staged state visible.
- `CHECKPOINT`: construct a *new* immutable fabric image from parent + overlay.
- `CALIBRATE`: backend-specific physical-codec calibration.

There is deliberately no ordinary `WRITE_FABRIC` operation.
