#!/usr/bin/env python3
"""Reassemble the exact GENESIS Chirality Fabric R62 checkpoint from ZIP_A... volumes."""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

EXPECTED_ORIGINAL_NAME = 'GENESIS_CHIRALITY_FABRIC_FULL_CHECKPOINT_R62_v1_0_20260829.zip'
EXPECTED_ORIGINAL_SHA256 = 'f0c63cabf18ad856f10dc2ffd57669ae02106a561d2c9af06a5ecf83bf79d65e'
MANIFEST_MEMBER = 'R62_SPLIT_PART_MANIFEST.json'


def sha256_file(path: Path, block: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            data = f.read(block)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def main() -> int:
    root = Path.cwd()
    volume_glob = 'GENESIS_CHIRALITY_FABRIC_FULL_CHECKPOINT_R62_v1_0_20260829' + '_ZIP_*.zip'
    volumes = sorted(root.glob(volume_glob))
    if not volumes:
        print(f'ERROR: No volume ZIPs matching {volume_glob} found in {root}', file=sys.stderr)
        return 2

    with zipfile.ZipFile(volumes[0], 'r') as zf:
        manifest = json.loads(zf.read(MANIFEST_MEMBER).decode('utf-8'))

    expected = manifest['parts']
    expected_names = [p['volume_name'] for p in expected]
    actual_names = [p.name for p in volumes]
    missing = [n for n in expected_names if n not in actual_names]
    extra = [n for n in actual_names if n not in expected_names]
    if missing:
        print('ERROR: Missing volumes:', ', '.join(missing), file=sys.stderr)
        return 3
    if extra:
        print('WARNING: Extra matching files ignored:', ', '.join(extra), file=sys.stderr)

    output = root / manifest['original_filename']
    if output.exists():
        print(f'ERROR: Output already exists: {output}', file=sys.stderr)
        return 4

    full_hash = hashlib.sha256()
    total_written = 0
    with output.open('wb') as out:
        for p in expected:
            volume_path = root / p['volume_name']
            print(f"Reading {volume_path.name} ...")
            with zipfile.ZipFile(volume_path, 'r') as zf:
                member = p['part_name']
                part_hash = hashlib.sha256()
                part_written = 0
                with zf.open(member, 'r') as src:
                    while True:
                        block = src.read(8 * 1024 * 1024)
                        if not block:
                            break
                        out.write(block)
                        full_hash.update(block)
                        part_hash.update(block)
                        part_written += len(block)
                        total_written += len(block)
                if part_written != p['part_size_bytes']:
                    output.unlink(missing_ok=True)
                    print(f"ERROR: Size mismatch for {member}", file=sys.stderr)
                    return 5
                if part_hash.hexdigest() != p['part_sha256']:
                    output.unlink(missing_ok=True)
                    print(f"ERROR: SHA-256 mismatch for {member}", file=sys.stderr)
                    return 6

    digest = full_hash.hexdigest()
    if total_written != manifest['original_size_bytes']:
        output.unlink(missing_ok=True)
        print('ERROR: Final byte count mismatch', file=sys.stderr)
        return 7
    if digest != manifest['original_sha256'] or digest != EXPECTED_ORIGINAL_SHA256:
        output.unlink(missing_ok=True)
        print('ERROR: Final SHA-256 mismatch', file=sys.stderr)
        return 8

    print()
    print('SUCCESS')
    print(f'Output:  {output}')
    print(f'Bytes:   {total_written:,}')
    print(f'SHA-256: {digest}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
