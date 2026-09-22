# Content-addressed package store

Resolved packages are copied under:

```text
STORE/<sha256>/
```

The store verifies package content before installation and after installation. A changed file produces a different identity rather than silently mutating an installed package.
