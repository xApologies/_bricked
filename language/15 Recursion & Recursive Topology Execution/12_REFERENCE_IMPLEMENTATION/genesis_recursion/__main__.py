import argparse,json
from pathlib import Path
from . import compile_source,RecursiveVM,encode,disassemble

def main():
    ap=argparse.ArgumentParser(prog='genesis-recursion'); ap.add_argument('source'); ap.add_argument('--emit-bytecode'); ap.add_argument('--disasm',action='store_true'); a=ap.parse_args()
    p=compile_source(Path(a.source).read_text(),a.source)
    if a.emit_bytecode: Path(a.emit_bytecode).write_bytes(encode(p))
    if a.disasm: print(disassemble(p))
    r=RecursiveVM().run(p); print(json.dumps({'exports':r.exports,'receipt':r.receipt},indent=2,sort_keys=True))
if __name__=='__main__': main()
