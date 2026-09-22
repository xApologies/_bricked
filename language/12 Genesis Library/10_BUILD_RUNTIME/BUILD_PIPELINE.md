# Package build pipeline

1. Load root manifest.
2. Resolve dependencies or validate a frozen lockfile.
3. Verify registry content roots.
4. Install dependencies into the local content-addressed store.
5. Build the package/module ownership table.
6. Audit direct-import discipline.
7. Lower each source module and audit its manifest effect budget.
8. Collect dependency sources in dependency-first order, followed by root sources.
9. Run the Section 11 optimized compiler path.
10. Execute optional reference VM validation.
11. Emit package build/provenance receipt and lockfile.
