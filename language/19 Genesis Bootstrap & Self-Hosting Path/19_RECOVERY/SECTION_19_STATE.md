# Section 19 recovery state

Canonical title: **Genesis Bootstrap + Self-Hosting Path**.

Recovery order:
1. Read `00_START_HERE/README.md` and architecture/invariants.
2. Restore `12_REFERENCE_IMPLEMENTATION` to PYTHONPATH.
3. Run `14_TESTS/test_section19.py`.
4. Verify `16_REFERENCE_RUNS/REFERENCE_BOOTSTRAP_SUMMARY.json` reports `BOOTSTRAP_FIXED_POINT` and `self_hosted=false`.
5. Verify `GENESIS_BOOTSTRAP_STAGE0.gboot` with `python -m genesis_bootstrap verify-image ...`.
6. Preserve the self-host frontier. Do not silently relabel HOST_ORACLE components as GENESIS_NATIVE.

Next target: Section 20 — Genesis v1.0 Conformance + Freeze.
