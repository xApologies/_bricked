# Recovery validation

- All 20 numbered domains and `_lang` recovered.
- All 19 Section 01–19 selected package SHA-256 values match the Section 20 freeze lock.
- All seven `_lang` PDFs match the source manifest.
- All 1,740 recovered files match selected source entry lengths and SHA-256.
- All 20 domain suites pass on Python 3.12; Sections 04–06 use native assertion runners (27, 49, 51 checks), other domains use unittest. The Section 11 fixture path is redirected by the new launcher.
- Section 20 conformance: 63/63 tests pass; partial-self-host status and the S0 gate remain enforced.
- No ZIP or Python bytecode cache is included. No source file exceeds 100 MiB.

Existing package test logs are historical release evidence. These recovery checks are separate from those logs. Repository bootstrap validation and exact staged-tree verification are recorded after final staging.

The repository bootstrap validator passed all nine checks. Validation-created .genesis/ package-store files are ignored and excluded from the staged tree.

Final staged review passed: 1,751 files; exact expected file set, no case-insensitive collisions, no ZIP/bytecode files, every staged blob equals its working-tree bytes, and every recovered source hash matches the selected archive. The largest file is the required reference fabric fixture at 2,101,248 bytes. Original Genesis ZIP SHA-256 was rechecked unchanged. Existing project paths have no staged changes.
