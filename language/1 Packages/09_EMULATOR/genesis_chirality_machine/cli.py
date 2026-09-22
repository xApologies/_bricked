import argparse, json
from .boot import boot
from .image import FabricImageBuilder
from .fixture import deterministic_cells

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest='cmd', required=True)
    b=sub.add_parser('build-fixture'); b.add_argument('path'); b.add_argument('--cells',type=int,default=65536)
    i=sub.add_parser('inspect'); i.add_argument('path')
    args=ap.parse_args()
    if args.cmd=='build-fixture':
        tag=FabricImageBuilder.build(args.path, deterministic_cells(args.cells))
        print(json.dumps({'path':args.path,'cells':args.cells,'fabric_tag':tag},indent=2))
    elif args.cmd=='inspect':
        m,r=boot(args.path); print(json.dumps(r,indent=2)); m.fabric.close()

if __name__=='__main__': main()
