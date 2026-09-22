# Capability Model

Capabilities are named, versioned authority declarations. They are not advisory labels.

Initial Section-17 capabilities:

```text
io.source.read
io.derived.read
io.derived.write
io.audit.append
cas.put
cas.get
brane.mount
brane.realize
blackglass.commit.propose
blackglass.commit.admit
device.request
```

A program must declare each capability it uses. Backends may further restrict a declared capability. Declaration is necessary, not sufficient, for physical authority.

No wildcard/ambient capability exists in v0.1.0.
