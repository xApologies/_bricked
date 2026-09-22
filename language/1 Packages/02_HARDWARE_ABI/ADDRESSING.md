# Addressing Model

A Genesis address is layered:

```text
semantic object address
    -> region binding
    -> FabricAddress128
    -> backend physical locator
```

This lets an MMO/Geometric retain stable semantic identity even if a backend moves blocks for wear leveling or maps the same fabric image into RAM, GPU memory, or FPGA registers.

### Address stability

The `fabric_tag` derives from the fabric identity digest rather than a device serial number. A copied, byte-identical fabric image therefore presents the same logical fabric address space. Provenance still records the physical device occurrence separately.
