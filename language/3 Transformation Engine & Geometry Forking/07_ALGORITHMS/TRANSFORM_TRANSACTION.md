# Transformation transaction algorithm

1. Resolve the parent instance and ordered segment chain.
2. Reconstruct the operative parent view.
3. Compute `pre_state_root` over the inherited region.
4. Verify the request's expected parent root, if provided.
5. Resolve all selectors.
6. Union operator effects.
7. Admit effects under the capability profile.
8. Build deterministic `plan_id` from canonical request + parent root.
9. Execute operators against a staged child view; later operators observe earlier staged changes.
10. Produce sparse ChangeSet by removing writes equal to the parent operative cell.
11. Verify invariant contract.
12. Compute prospective `post_state_root` from parent view + staged ChangeSet.
13. Write immutable `.gtd` to a temporary path.
14. Atomically rename into place.
15. Reopen and verify header, payload hash and records.
16. Reconstruct the child view and independently recompute `post_state_root`.
17. Verify base-fabric and parent-segment hashes have not changed.
18. Emit closure receipt, append lineage ledger, and create child instance manifest.
19. Re-lift child to BRANE M^5; BRANE still owns realization Z.
