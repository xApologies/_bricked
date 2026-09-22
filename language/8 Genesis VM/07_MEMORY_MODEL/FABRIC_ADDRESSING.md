# Fabric addressing

GVM treats a fabric address as a typed `FABRIC_ADDR`, not an integer with implicit meaning. The backend maps it to the Section 01 Fabric Address ABI.

No normal `MOVE`, `CONST`, or control-flow instruction can create authority to write a fabric cell. Only an admitted backend call carrying the `WRITE_OVERLAY` effect can produce a fabric write receipt.
