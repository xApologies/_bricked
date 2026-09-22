# Section 17 Architecture

Execution path:

```text
Genesis source
  -> frontend / GIR
  -> static semantics / linker
  -> optimizer / GVM
  -> Section 16 scheduler
  -> Section 17 system-call boundary
       |-- sandboxed source / derived / audit I/O
       |-- content-addressed immutable object store
       |-- BRANE port validation + request realization
       |-- BLACKGLASS persistence proposal boundary
       `-- device capability intents
  -> Section 01-16 services / backend realization
```

Section 17 introduces five system objects:

1. `Capability` — explicit authority to request an operation.
2. `Endpoint` — typed system boundary address.
3. `SystemRequest` — immutable requested action.
4. `BoundaryReceipt` — deterministic result/provenance record.
5. `ObjectRef` — durable content-addressed reference independent of host path.

BLACKGLASS and BRANE are separate architectural roles. BLACKGLASS supplies durable system services and hosts BRANE. BRANE validates/mounts modules and supplies request-relative realization. The Genesis language targets their contracts rather than Python/Windows filesystem semantics.
