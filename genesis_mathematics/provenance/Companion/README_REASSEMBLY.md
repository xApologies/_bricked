# Genesis Manuscript v3.0 — Split Upload Set

Original:
`GENESIS_MANUSCRIPT_v3_0_MATHEMATICS_ONLY_20260828.zip`

Original SHA-256:
`8b9a92ac56ab71ece3880e47ef6f8d47bc6a69beaab7e67994ed87b36f330209`

Original size:
885094360 bytes

Split into 9 parts of at most 95 MiB so each remains comfortably below 100 MB.

## Upload/reassembly rule

Upload every `.part` file in alphabetical order together with `MANIFEST.json`.

The files are raw byte segments of the original ZIP. They are **not independently unzip-able**.
They must be concatenated in order A, B, C, ... to reconstruct the original archive exactly.

## Reassembly on macOS/Linux

```bash
cat GENESIS_v3_0_*.part > GENESIS_MANUSCRIPT_v3_0_MATHEMATICS_ONLY_20260828.zip
```

## Reassembly on Windows PowerShell

```powershell
$parts = Get-ChildItem GENESIS_v3_0_*.part | Sort-Object Name
$out = [System.IO.File]::Create("GENESIS_MANUSCRIPT_v3_0_MATHEMATICS_ONLY_20260828.zip")
foreach ($p in $parts) {
    $bytes = [System.IO.File]::ReadAllBytes($p.FullName)
    $out.Write($bytes, 0, $bytes.Length)
}
$out.Close()
```

After reassembly, verify SHA-256 equals:

`8b9a92ac56ab71ece3880e47ef6f8d47bc6a69beaab7e67994ed87b36f330209`

