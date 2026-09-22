# Boot Protocol

1. Open fabric backend read-only.
2. Read and validate superblock.
3. Recompute cell-data SHA-256.
4. Verify `fabric_tag` against the digest.
5. Mount empty or recovered overlay.
6. Load physical codec calibration profile.
7. Register region/object catalogs.
8. Initialize GCM registers.
9. Expose BRANE/Trinity realization adapter.
10. Emit `FABRIC_MOUNT_RECEIPT`.

A failed integrity check prevents the fabric from becoming the authoritative substrate.
