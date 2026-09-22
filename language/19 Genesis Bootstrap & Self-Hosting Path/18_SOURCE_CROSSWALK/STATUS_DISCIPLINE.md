# Status discipline

- `BOOTSTRAP_FIXED_POINT`: demonstrated by the reference Stage-0/1/2 run.
- `GENESIS_NATIVE`: source is authored in Genesis and executes as Genesis bytecode.
- `GENESIS_CONTROLLED`: Genesis owns the transaction/control flow but invokes an external implementation through a typed capability.
- `HOST_ORACLE`: Python reference implementation remains in the trusted boot path.
- `FULL_SELF_HOST`: explicitly **not achieved** in Section 19.
- Physical/hardware claims: unchanged from prior sections; Section 19 is software bootstrap architecture.
