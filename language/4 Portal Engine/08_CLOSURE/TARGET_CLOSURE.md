# Target Closure

A Portal closes only when all checks pass:

```text
destination segment CRC/hash verified
destination record count equals source logical cell count
destination content_root satisfies preservation contract
canonical MMO identity policy passes
route witness terminates at requested target domain
requested sector remains valid
minimum R/B ledger remains valid
route reservation existed for the transaction
source and base fabric hashes remain unchanged
provenance contains route and transaction receipts
```

The destination's physical address changes. Therefore an address-inclusive state hash may change even when all information content is preserved.
