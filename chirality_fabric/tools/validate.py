"""Validate the recovered R62 Git tree and optionally its complete local archive set."""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import sqlite3
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def validate(local_root=None):
    inventory = json.loads((ROOT / 'provenance/SOURCE_INVENTORY.json').read_text(encoding='utf-8'))
    included = [row for row in inventory['files'] if row['disposition'] == 'GIT_SOURCE']
    expected = {row['git_path'] for row in included}
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'R62').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    require(actual == expected, f'R62 file set differs: extra={actual-expected}, missing={expected-actual}')
    for row in included:
        path = ROOT / row['git_path']
        require(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], f'Source mismatch: {path}')
    for row in inventory['controls']:
        path = ROOT / row['path']
        require(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], f'Control mismatch: {path}')
    qa = json.loads((ROOT / 'R62/06_MANIFEST/QA_REPORT.json').read_text(encoding='utf-8'))
    prior = ROOT / 'R62/04_PRIOR_EXPANDED/R61_COMPACT_RECOVERY_EXPANDED'
    prior_qa = json.loads((prior / '12_AUDIT/QA_REPORT.json').read_text(encoding='utf-8'))
    databases = [(ROOT / 'R62/05_MACHINE/genesis_chirality_full_checkpoint.sqlite', qa['table_counts']),
                 (prior / '07_MACHINE/genesis_chirality_recovery.sqlite', prior_qa['row_counts'])]
    for path, counts in databases:
        with sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True) as con:
            require(con.execute('pragma integrity_check').fetchall() == [('ok',)], f'Database integrity failed: {path}')
            for table, count in counts.items():
                observed = con.execute('select count(*) from "' + table.replace('"', '""') + '"').fetchone()[0]
                require(observed == count, f'Table count mismatch: {path}: {table}')
    apis = [(ROOT / 'R62/05_MACHINE/qmo_api.py', [shlex.split(c) for c in qa['api_smoke']]),
            (prior / '07_MACHINE/qmo_api.py', [['info'], ['address', '@object/chirality_tile'], ['address', '@eq/torus_update'],
             ['neighbors', '@object/chirality_block', '--direction', 'both'], ['search', 'torus'], ['list', 'open_debt']])]
    smoke_count = 0
    for api, commands in apis:
        for command in commands:
            result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(api), *command], capture_output=True, text=True, encoding='utf-8', timeout=60)
            require(result.returncode == 0, f'API failed: {api} {command}: {result.stderr}')
            require(bool(json.loads(result.stdout)), f'Empty API result: {api} {command}')
            smoke_count += 1
    local_count = 0
    if local_root:
        for row in inventory['files']:
            path = local_root / row['local_path']
            require(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], f'Local source mismatch: {path}')
            if row['disposition'] == 'LOCAL_ARCHIVE':
                with zipfile.ZipFile(path) as archive:
                    require(archive.testzip() is None, f'ZIP CRC failed: {path}')
                local_count += 1
    # Querying must not mutate source databases or files.
    for row in included:
        require(sha(ROOT / row['git_path']) == row['sha256'], f'Source mutated during validation: {row["git_path"]}')
    result = {'status': 'PASS', 'recovered_files': len(included), 'control_files': len(inventory['controls']),
              'sqlite_databases': len(databases), 'api_smoke_commands': smoke_count, 'local_archives_checked': local_count}
    print(json.dumps(result, indent=2))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--local-root', type=Path, help='Complete reconstructed local R62 extraction')
    args = parser.parse_args()
    validate(args.local_root)
