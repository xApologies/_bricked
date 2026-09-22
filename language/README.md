# Genesis Language

This is the recovered working source tree for the corpus's Genesis 1.0 frozen reference release. All 20 numbered domains and `_lang` contain actual source files. Start with [Section 20](20%20GENESIS/00_START_HERE/README.md) for the release freeze, then each domain's `00_START_HERE/README.md`.

Genesis-native terminology, domain boundaries, source-language/computational-language distinction, and software-oracle scope are preserved. Python implements the supplied reference semantics; it does not redefine Genesis ontology. The release remains **PARTIAL_SELF_HOST**, and BLACKGLASS migration remains a later phase.

## Domains

| Recovered domain | Source files |
| --- | ---: |
| [1 Packages](1%20Packages/00_START_HERE/README.md) | 46 |
| [2 Instantiation & Memory](2%20Instantiation%20%26%20Memory/00_START_HERE/README.md) | 76 |
| [3 Transformation Engine & Geometry Forking](3%20Transformation%20Engine%20%26%20Geometry%20Forking/00_START_HERE/README.md) | 101 |
| [4 Portal Engine](4%20Portal%20Engine/00_START_HERE/README.md) | 86 |
| [5 Rainbow Road](5%20Rainbow%20Road/00_START_HERE/README.md) | 98 |
| [6 QFT + GR Bridge](6%20QFT%20%2B%20GR%20Bridge/00_START_HERE/README.md) | 114 |
| [7 QIS + Effect System](7%20QIS%20%2B%20Effect%20System/00_START_HERE/README.md) | 139 |
| [8 Genesis VM](8%20Genesis%20VM/00_START_HERE/README.md) | 67 |
| [9 Semantic Linker](9%20Semantic%20Linker/00_START_HERE/README.md) | 78 |
| [10 Genesis Surface Language](10%20Genesis%20Surface%20Language/00_START_HERE/README.md) | 76 |
| [11 Genesis Optimization & Backend](11%20Genesis%20Optimization%20%26%20Backend/00_START_HERE/README.md) | 84 |
| [12 Genesis Library](12%20Genesis%20Library/00_START_HERE/README.md) | 115 |
| [13 Callable Abstractions, Functions & Generics](13%20Callable%20Abstractions%2C%20Functions%20%26%20Generics/00_START_HERE/README.md) | 148 |
| [14 Control Flow & Data Algebra](14%20Control%20Flow%20%26%20Data%20Algebra/00_START_HERE/README.md) | 116 |
| [15 Recursion & Recursive Topology Execution](15%20Recursion%20%26%20Recursive%20Topology%20Execution/00_START_HERE/README.md) | 50 |
| [16 Concurrency & Scheduling & Resource Coordination](16%20Concurrency%20%26%20Scheduling%20%26%20Resource%20Coordination/00_START_HERE/README.md) | 51 |
| [17 System I-O & BLACKGLASS-BRANE Interface](17%20System%20I-O%20%26%20BLACKGLASS-BRANE%20Interface/00_START_HERE/README.md) | 69 |
| [18 Compiler Toolchain & Diagnostics & Debugging](18%20Compiler%20Toolchain%20%26%20Diagnostics%20%26%20Debugging/00_START_HERE/README.md) | 72 |
| [19 Genesis Bootstrap & Self-Hosting Path](19%20Genesis%20Bootstrap%20%26%20Self-Hosting%20Path/00_START_HERE/README.md) | 69 |
| [20 GENESIS](20%20GENESIS/00_START_HERE/README.md) | 77 |
| [_lang](_lang/GENESIS_LANGUAGE_SOURCESET_v0.1_MANIFEST.json) | 8 |

## Working with the source

Each numbered domain retains its internal architecture, contracts, schemas, examples, tests, and reference implementation. `_lang` retains Rules, Grammar, Domains, Structure, Root Family, Rosetta, and Phonology PDFs plus their source manifest. Domain versions are layers of the frozen release, not interchangeable historical snapshots. Vendored implementation dependencies remain at the import locations supplied by the release.

From the repository root with Python 3.12, run:

```text
python -B language/tools/run_tests.py
python -B language/tools/run_tests.py --domain 20
node tools/validators/validate-bootstrap.mjs
```

The test launcher runs each domain in a separate process and redirects Section 11's historical `/mnt/data` fixture location to the recovered Section 10 examples. Recovered source bytes are unchanged. Historical `98_BUILD` assembly scripts retain their original host-specific paths and are not portable entry points; do not run them as the project build command. For compiler commands, use each domain's reference-implementation README and add that domain's implementation directory to `PYTHONPATH`.

Generated reference runs/builds and historical ZIP capsules are deliberately absent. Existing `99_RELEASE` records describe the original packages and are preserved as historical release evidence; they are not manifests of this filtered working tree. [RECOVERED_FILES.json](provenance/RECOVERED_FILES.json) records the actual recovered file paths and hashes.

## Recovery and open issues

- [Source recovery and selection authority](provenance/SOURCE_RECOVERY.md)
- [Every exclusion and its scope](provenance/EXCLUDED_ARTIFACTS.md)
- [Physical path normalization](provenance/PATH_NORMALIZATION.md)
- [Source conflicts and inherited semantic gates](provenance/CONFLICTS.md)
- [Validation](provenance/VALIDATION.md)

The inherited `S0_STRUCTURAL_ZERO_VS_EXISTENCE_CONFLICT` remains unresolved exactly as declared in the release; this recovery does not reconcile it.

On Windows, enable Git long-path support when cloning or checking out this tree (git -c core.longpaths=true clone ...); the original nested vendor structure is preserved.
