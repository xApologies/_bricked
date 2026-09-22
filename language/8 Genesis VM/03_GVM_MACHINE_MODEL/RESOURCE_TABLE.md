# Resource table

Resource handles are machine-visible references to identity-bearing objects. They carry at minimum:

- `resource_id`;
- `kind`;
- `content_hash`;
- `parent_ids`;
- `sector` when applicable;
- `typestate` / closure state;
- provenance metadata;
- backend locator.

Copying a handle does not duplicate the underlying physical or semantic resource. For linear resources such as nonclassical `QSTATE`, even handle copying is verifier-restricted.
