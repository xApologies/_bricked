# Genesis Chirality Machine — Section 01
## Hardware ABI + Immutable Chirality Fabric + Virtual Machine ISA

**Version:** 0.1.0  
**Date:** 2026-08-21  
**Status:** implementation baseline / emulated hardware contract  
**Parent:** Genesis Layer Zero Implementation v0.1.0

This section defines the bottom executable boundary of the Genesis stack.

The key engineering decision is:

> Genesis does not inherit CPU semantics as its language ontology. It targets a Chirality Machine whose persistent substrate is an immutable Chirality Fabric. Current CPUs, RAM, SSDs, GPUs, and future FPGA/custom devices are backends that realize that machine contract.

The package therefore defines:

- a stable 128-bit Fabric Address ABI;
- a 32-byte Chirality Cell ABI;
- an immutable fabric-image format;
- a sparse copy-on-write runtime overlay;
- physical-state codecs that map logical chirality/basin classes to backend-specific stored states;
- a boot and integrity protocol;
- a Genesis Chirality Machine ISA-0;
- a Python reference emulator;
- backend interfaces for memory, mmap/file, block devices, FPGA registers, and future custom hardware;
- explicit separation between the canonical chirality ontology and computer-science implementation analogies;
- tests proving that dynamic execution does not mutate the base fabric image.

## Recovery order

1. Read `01_ARCHITECTURE/ARCHITECTURE.md`.
2. Read `02_HARDWARE_ABI/HARDWARE_ABI.md`.
3. Read `03_FABRIC_IMAGE/FABRIC_IMAGE_FORMAT.md`.
4. Read `07_VM_ISA/GCM_ISA_0.md`.
5. Run `python -m unittest discover -s 12_TESTS -p 'test_*.py' -v` from the package root.
6. Use source capsules only for provenance or design reconciliation.

## Boundary discipline

The recovered MK43/API corpus explicitly excluded CPU, operating-system, scheduler, filesystem, SSD-controller, and memory-fabric analogies from canonical chirality ontology. This implementation preserves that ruling: those are **engineering realizations**, not foundational ontology.
