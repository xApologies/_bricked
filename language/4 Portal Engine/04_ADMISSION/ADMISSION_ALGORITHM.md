# Admission Algorithm

1. Verify source instance and source segment chain.
2. Compute source `content_root` independent of physical address.
3. Compute requested invariant residue root.
4. Classify payload chirality envelope / color class.
5. Resolve source and target domains.
6. Enumerate graph paths under hop limit.
7. Reject paths with unsupported sector/chirality/residue/closure.
8. Reject paths below Resolution or Bandwidth thresholds.
9. Reject paths without sufficient currently available capacity.
10. Rank remaining paths by `(total_cost, hop_count, -min_bandwidth, path_id)`.
11. Reserve capacity atomically across the winning path.
12. Reserve a destination fabric region.
13. Emit `PortalPlan` and route witness.

Admission does not move data. It proves that the current transaction can be attempted under the declared software contracts.
