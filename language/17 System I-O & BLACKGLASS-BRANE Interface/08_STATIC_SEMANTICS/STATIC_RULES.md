# Static Rules

The Section-17 verifier checks before execution:

- source language version is `0.6.0` for this standalone reference dialect;
- every used system operation has its required declared capability;
- endpoint mode/kind admits the operation;
- registers are defined before use;
- output registers are not silently overwritten;
- BRANE ports satisfy the 5D contract and required policy fields;
- a BRANE requested capability is declared by the mounted port;
- BLACKGLASS admission requires both proposal and admission capabilities;
- every program closes exactly once at the end;
- no operation occurs after `close`.

These checks supplement, rather than replace, the Section 09 type/effect checker and Section 16 resource scheduler.
