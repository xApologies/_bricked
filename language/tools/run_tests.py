"""Run preserved Genesis domain tests in isolated Python processes."""
import argparse
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]

def domains():
    return sorted((p for p in ROOT.iterdir() if p.is_dir() and p.name.split()[0].isdigit()), key=lambda p: int(p.name.split()[0]))

def run_one(number):
    domain = next(p for p in domains() if int(p.name.split()[0]) == number)
    for p in domain.iterdir():
        if p.is_dir() and (p.name.endswith('_REFERENCE_IMPLEMENTATION') or p.name == '09_EMULATOR'):
            sys.path.insert(0, str(p))
    suite = unittest.TestSuite()
    for path in sorted(domain.glob('*_TESTS/test*.py')):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)
        if number == 11:
            # Replace only the historical build-host fixture path, not source semantics.
            module.EX = next(p for p in domains() if p.name.startswith('10 ')) / '16_EXAMPLES'
        if number in (4, 5, 6):
            count = module.run()
            print(f'{count}/{count} PASS', flush=True)
            return 0
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    if suite.countTestCases() == 0:
        raise RuntimeError(f'No tests discovered for {domain.name}')
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', type=int, choices=range(1, 21))
    args = parser.parse_args()
    if args.domain:
        raise SystemExit(run_one(args.domain))
    failed = []
    for domain in domains():
        print(f'=== {domain.name} ===', flush=True)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
        result = subprocess.run([sys.executable, '-B', str(Path(__file__).resolve()), '--domain', domain.name.split()[0]], env=env, cwd=ROOT)
        if result.returncode:
            failed.append(domain.name)
    print('Failed domains:', failed, flush=True)
    raise SystemExit(bool(failed))

