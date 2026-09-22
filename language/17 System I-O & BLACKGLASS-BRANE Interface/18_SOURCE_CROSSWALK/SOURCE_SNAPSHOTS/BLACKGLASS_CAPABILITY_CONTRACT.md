# Capability Contract

A body capability is a typed service declaration, e.g.:

```json
{
  "name": "translate.request",
  "version": "1",
  "input": {"dx":"float","dy":"float","dz":"float"},
  "safety_class": "MOTION",
  "local_authority_required": true
}
```

High-level cognition requests capabilities; body-local controllers determine feasible/safe execution.
