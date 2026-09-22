# Reference implementation

Run with package root on `PYTHONPATH` so the bundled `vendor` package is importable.

The implementation uses NumPy only for scientific array ingestion. Runtime `.gos` readback is mmap/binary-search based and does not require NumPy.
