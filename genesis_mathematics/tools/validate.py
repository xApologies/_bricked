"""Check recovered source integrity; this does not validate mathematical claims."""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT.parent / 'provenance/sources/GENESIS_MATHEMATICS_RECEIPT.json'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def check_file(path, row):
    require(path.is_file(), f'Missing: {path}')
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    require(path.stat().st_size == row['bytes'] and digest == row['sha256'], f'Source mismatch: {path}')

def validate(local_root=None):
    receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
    selected = [r for r in receipt['files'] if r['disposition'] == 'GIT_SOURCE']
    actual = {p.relative_to(ROOT / 'v3.0').as_posix() for p in (ROOT / 'v3.0').rglob('*') if p.is_file()}
    require(actual == {r['path'] for r in selected}, 'Source file set differs from receipt')
    for row in selected:
        check_file(ROOT / 'v3.0' / row['path'], row)
    for row in receipt['controls']:
        check_file(ROOT / row['path'], row)
    db = ROOT / 'v3.0/MACHINE/genesis_manuscript_v3_0.sqlite'
    with sqlite3.connect(db.resolve().as_uri() + '?mode=ro', uri=True) as con:
        require(con.execute('pragma integrity_check').fetchall() == [('ok',)], 'SQLite integrity failed')
        for table, count in receipt['sqlite_counts'].items():
            quoted = table.replace('"', '""')
            require(con.execute(f'SELECT count(*) FROM "{quoted}"').fetchone()[0] == count, f'Count mismatch: {table}')
        for path, in con.execute('select path from chapters'):
            require((ROOT / 'v3.0' / path).is_file(), f'Missing chapter: {path}')
    if local_root:
        for row in receipt['files']:
            check_file(local_root / row['path'], row)
            if row['disposition'] == 'LOCAL_HISTORICAL_ARCHIVE':
                with zipfile.ZipFile(local_root / row['path']) as archive:
                    require(archive.testzip() is None, f'Archive CRC failed: {row["path"]}')
        manifest = json.loads((local_root / 'MACHINE/MANIFEST.json').read_text(encoding='utf-8'))
        for row in manifest:
            check_file(local_root / row['path'], row)
        for line in (local_root / 'MACHINE/SHA256SUMS.txt').read_text().splitlines():
            digest, path = line.split('  ', 1)
            check_file(local_root / path, {'sha256': digest, 'bytes': (local_root / path).stat().st_size})
    print(json.dumps({'status': 'PASS', 'source_files': len(selected), 'controls': len(receipt['controls']), 'sqlite': 'ok', 'full_local_source_verified': bool(local_root)}, indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-root', type=Path)
    validate(parser.parse_args().local_root)
