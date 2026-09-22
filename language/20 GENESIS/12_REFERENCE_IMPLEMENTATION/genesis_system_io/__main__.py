from pathlib import Path
import sys,tempfile
from . import compile_source,disassemble,SystemRuntime
if len(sys.argv)<2: raise SystemExit("usage: python -m genesis_system_io FILE.gen")
p=compile_source(Path(sys.argv[1]).read_text(),sys.argv[1]); print(disassemble(p),end="")
with tempfile.TemporaryDirectory() as td:
    r=SystemRuntime(p,Path(td)); print("compiled:",p.metadata["program_id"],"(seed required for READ examples)")
