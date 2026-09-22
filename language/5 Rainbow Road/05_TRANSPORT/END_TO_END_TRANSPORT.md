# End-to-End Information Transportation

Each Portal leg performs Section-04 `RE_REALIZE` transport. The output Geometric becomes the source of the next leg.

For a lossless Road:

```text
content_root(source) == content_root(final)
residue_root(source) == residue_root(final)
canonical_mmo_id(source) == canonical_mmo_id(final)
```

when those fields are included in the preservation contract.

Intermediate physical fabric addresses are expected to change. Address change is transportation; logical invariant change is transformation and therefore requires a different contract/layer.
