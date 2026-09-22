# Genesis semantic-version profile v0.1

Supported requirement forms:

- exact: `1.2.3`
- caret: `^1.2.3`
- tilde: `~1.2.3`
- wildcard: `*`, `1.*`, `1.2.*`

Resolution chooses the highest version satisfying every accumulated constraint for a package name. Pre-release/build metadata are intentionally outside the Section 12 reference profile.
