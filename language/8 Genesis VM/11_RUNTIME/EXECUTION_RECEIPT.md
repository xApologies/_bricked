# Execution receipt

Every completed VM run emits a receipt containing:

- program name/version/hash;
- bytecode hash;
- backend identity/version;
- executed instruction count;
- exported register/resource hashes;
- append-only operation ledger root;
- open transaction count at halt;
- verifier status;
- deterministic execution root.

This is the bridge from language execution to BLACKGLASS provenance/recovery.
