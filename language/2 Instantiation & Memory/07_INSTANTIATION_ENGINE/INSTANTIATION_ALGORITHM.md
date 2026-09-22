# Instantiation Algorithm

```text
INPUT: MMO source, selected representation, mounted fabric, allocation registry

1. LOAD and hash source representation.
2. NORMALIZE source into a RepresentationBundle.
3. SELECT explicit MappingProfile.
4. COMPUTE grid shape, roles, cells_per_voxel, total cells.
5. PLAN deterministic binding formula.
6. RESERVE non-overlapping fabric region.
7. STREAM voxels:
      encode role cells
      write sorted .gos records
8. FINALIZE .gos superblock and payload hash.
9. VERIFY segment hash and address bounds.
10. READ BACK declared verification sample/full set.
11. COMMIT reservation and create immutable GeometricInstance manifest.
12. EMIT M^5 descriptor for BRANE.
13. MARK instance LIVE only after all receipts are sealed.

ON FAILURE:
    delete temporary segment;
    release reservation;
    emit failure receipt;
    do not modify base fabric.
```
