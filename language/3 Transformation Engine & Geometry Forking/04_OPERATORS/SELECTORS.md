# Selectors

Transformation operators never receive arbitrary host pointers. They receive selectors resolved against the inherited Geometric binding.

Supported selectors:

- `all`: entire Geometric region;
- `role`: one logical role offset (`control`, `chi_00`, etc.);
- `range`: local cell-index interval;
- `voxel_box`: rectangular object-local XYZ voxel interval plus optional roles.

Selectors resolve to sorted, deduplicated fabric cell indices. Address containment is verified before any operator executes.
