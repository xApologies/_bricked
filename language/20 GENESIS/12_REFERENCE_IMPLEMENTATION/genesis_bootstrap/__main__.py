from __future__ import annotations
import argparse,json
from pathlib import Path
from .bootstrap import BootstrapHarness
from .frontier import load_frontier,verify_frontier
from .image import build_gboot,verify_gboot
from .util import canonical_json

def main(argv=None):
    ap=argparse.ArgumentParser(prog="genesis-bootstrap"); sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("run"); p.add_argument("controller"); p.add_argument("frontier"); p.add_argument("--out")
    p=sp.add_parser("frontier"); p.add_argument("frontier")
    p=sp.add_parser("verify-image"); p.add_argument("image")
    a=ap.parse_args(argv)
    if a.cmd=="frontier": print(json.dumps(verify_frontier(load_frontier(Path(a.frontier))),sort_keys=True)); return 0
    if a.cmd=="verify-image": print(json.dumps(verify_gboot(Path(a.image)),sort_keys=True)); return 0
    r=BootstrapHarness(Path(a.controller),Path(a.frontier)).run()
    print(json.dumps(r.as_dict(),sort_keys=True))
    if a.out:
        c=Path(a.controller).read_bytes(); f=Path(a.frontier).read_bytes(); b=__import__('genesis_system_io.compiler',fromlist=['compile_source']).compile_source(c.decode(),a.controller); enc=__import__('genesis_system_io.bytecode',fromlist=['encode']).encode(b)
        build_gboot(Path(a.out),{"bootstrap/bootstrap_controller.gen":c,"bootstrap/self_host_frontier.json":f,"bootstrap/stage0.gio":enc,"bootstrap/bootstrap_receipt.json":canonical_json(r.as_dict())})
    return 0
if __name__=="__main__": raise SystemExit(main())
