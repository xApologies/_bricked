import argparse,json,pathlib
from .linker import link_bundle
from .capabilities import reference_backend_capabilities
from .vendor.genesis_vm import disassemble, VM

def main():
    ap=argparse.ArgumentParser(prog='genesis_semantics'); sp=ap.add_subparsers(dest='cmd',required=True)
    l=sp.add_parser('link'); l.add_argument('bundle'); l.add_argument('-o','--out',required=True)
    c=sp.add_parser('check'); c.add_argument('bundle')
    a=ap.parse_args(); b=json.loads(pathlib.Path(a.bundle).read_text())
    r=link_bundle(b,reference_backend_capabilities())
    if a.cmd=='link':
        out=pathlib.Path(a.out); out.write_bytes(r.bytecode); print(json.dumps(r.receipt,indent=2,sort_keys=True))
    else: print(json.dumps({'receipt':r.receipt,'proofs':r.proofs,'check':r.check.as_dict()},indent=2,sort_keys=True))
if __name__=='__main__': main()
