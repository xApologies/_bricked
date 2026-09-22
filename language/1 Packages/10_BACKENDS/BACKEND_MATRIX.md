# Backend Matrix

| Backend | Status | Fabric | Overlay | Raw physical-level control |
|---|---|---|---|---|
| In-memory | implemented | bytes | dict | simulated |
| mmap `.gcf` file | implemented | read-only mmap | sparse overlay | simulated |
| block-device logical LBA | interface/stub | read-only blocks | separate log | controller-mediated |
| GPU buffer | design contract | immutable buffer | mutable overlay buffer | digital |
| FPGA register/RAM | interface/stub | ROM/BRAM | RAM/log | implementation-defined |
| custom multilevel memory | future ABI target | device-specific | device/log | potentially calibrated |

The interface does not assume commodity storage provides direct per-cell voltage programming.
