# Bootstrap runtime image

A `.gboot` image is a deterministic ZIP container with fixed timestamps and canonical file order. It contains:

- bootstrap controller source;
- Stage-0 encoded bytecode;
- self-host frontier;
- seed/port identities;
- bootstrap receipt;
- SHA-256 manifest.

The image is a recovery/bootstrap object, not a new executable format. The executable payload remains the Section-17 GIO bytecode contract.
