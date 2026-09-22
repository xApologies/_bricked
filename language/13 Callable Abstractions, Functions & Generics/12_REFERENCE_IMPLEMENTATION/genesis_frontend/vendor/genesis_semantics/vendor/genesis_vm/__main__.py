import argparse, json, pathlib
from . import compile_gir, encode, decode, verify, VM, disassemble

def main():
    ap=argparse.ArgumentParser(prog='genesis_vm')
    sp=ap.add_subparsers(dest='cmd',required=True)
    c=sp.add_parser('compile'); c.add_argument('gir'); c.add_argument('-o','--out',required=True)
    d=sp.add_parser('disasm'); d.add_argument('gvm')
    v=sp.add_parser('verify'); v.add_argument('gvm')
    r=sp.add_parser('run'); r.add_argument('gvm')
    a=ap.parse_args()
    if a.cmd=='compile':
        gir=json.loads(pathlib.Path(a.gir).read_text()); p=compile_gir(gir); verify(p); pathlib.Path(a.out).write_bytes(encode(p))
    elif a.cmd=='disasm': print(disassemble(decode(pathlib.Path(a.gvm).read_bytes())),end='')
    elif a.cmd=='verify': print(json.dumps(verify(decode(pathlib.Path(a.gvm).read_bytes())),indent=2))
    elif a.cmd=='run':
        res=VM().run(decode(pathlib.Path(a.gvm).read_bytes())); print(json.dumps(res.receipt,indent=2,sort_keys=True))
if __name__=='__main__': main()
