# Mainframe Host

v0.1 target: one local workstation with substantial SSD capacity and GPU compute.

Host responsibilities:
- filesystem durability;
- database services;
- model inference/training processes;
- device USB/network endpoints;
- process isolation;
- backup/export;
- hardware monitoring.

The host is replaceable. BLACKGLASS must be exportable and recoverable without hardware identity dependence.

Recommended storage invariant:

```text
irreplaceable source > durable Hangar state > rebuildable indexes > scratch/checkpoints
```

Keep at least 20% disk headroom during heavy extraction/training/index work.
