import sys,json
from pathlib import Path
from . import compile_source,DeterministicScheduler,disassemble,encode
if len(sys.argv)<2: raise SystemExit('usage: python -m genesis_concurrency FILE.gen [--disasm] [--bytecode OUT]')
p=compile_source(Path(sys.argv[1]).read_text(),sys.argv[1])
if '--disasm' in sys.argv: print(disassemble(p),end='')
if '--bytecode' in sys.argv:
    i=sys.argv.index('--bytecode');Path(sys.argv[i+1]).write_bytes(encode(p))
r=DeterministicScheduler(p).run();print(json.dumps({'status':r.status,'receipt':r.receipt,'tasks':r.tasks},indent=2,sort_keys=True))
