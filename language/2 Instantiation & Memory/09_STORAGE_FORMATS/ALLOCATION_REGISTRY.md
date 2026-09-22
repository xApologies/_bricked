# Allocation Registry

The allocation registry is operational metadata, not fabric state. It records:

- free/reserved/committed spans;
- owning instance/reservation;
- read/write/shared mode;
- timestamps/receipts;
- released tombstones.

For recovery, committed instance manifests are the authority; the registry can be rebuilt by replaying manifests and receipts.
