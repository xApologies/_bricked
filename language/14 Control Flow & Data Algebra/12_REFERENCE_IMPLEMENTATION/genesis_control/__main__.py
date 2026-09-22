import argparse
from pathlib import Path
from . import compile_source,VM,encode,disassemble
p=argparse.ArgumentParser(); p.add_argument('source'); p.add_argument('--run',action='store_true'); p.add_argument('--out')
a=p.parse_args(); text=Path(a.source).read_text(); ast,prog=compile_source(text,a.source); print(disassemble(prog))
if a.out: Path(a.out).write_bytes(encode(prog))
if a.run: print(VM().run(prog).receipt)
