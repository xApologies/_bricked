# Recovery order

1. Read `01_ARCHITECTURE/ARCHITECTURE.md`.
2. Read `02_PACKAGE_CONSTITUTION/PACKAGE_CONSTITUTION.md`.
3. Mount `17_STANDARD_LIBRARY/REGISTRY/` as the reference local registry.
4. Add `12_REFERENCE_IMPLEMENTATION/` to `PYTHONPATH`.
5. Run `python -m unittest discover -s 15_TESTS -v` from the Section 12 root.
6. Use `genesis_packages.PackageRuntime` to resolve/build a project.
7. Treat Section 11 and earlier semantics as authoritative beneath this package layer.
