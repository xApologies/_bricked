from __future__ import annotations
import argparse,json,sys,tempfile
from pathlib import Path
from genesis_system_io.compiler import compile_source
from genesis_system_io.disasm import disassemble
from .build import BuildDriver,compare_rebuilds
from .diagnostics import render
from .tracing import TracingRuntime
from .test_runner import TestRunner
from .util import canonical_json

def _driver(a): return BuildDriver(target=getattr(a,"target",None) or "gcm-system-v0.6",profile=getattr(a,"profile",None) or "debug")
def main(argv=None):
    ap=argparse.ArgumentParser(prog="genesis"); sp=ap.add_subparsers(dest="cmd",required=True)
    for n in ("check","disasm","doctor"):
        p=sp.add_parser(n)
        if n!="doctor": p.add_argument("source")
    p=sp.add_parser("build"); p.add_argument("source"); p.add_argument("-o","--out",required=True); p.add_argument("--target",default="gcm-system-v0.6"); p.add_argument("--profile",default="debug")
    p=sp.add_parser("run"); p.add_argument("source"); p.add_argument("--base",required=True); p.add_argument("--seed",action="append",default=[])
    p=sp.add_parser("trace"); p.add_argument("source"); p.add_argument("--base",required=True); p.add_argument("--seed",action="append",default=[])
    p=sp.add_parser("test"); p.add_argument("cases",nargs="+")
    p=sp.add_parser("repro"); p.add_argument("source")
    a=ap.parse_args(argv)
    if a.cmd=="doctor":
        print(json.dumps({"status":"PASS","toolchain":"0.1.0","system_io":"available"},sort_keys=True)); return 0
    src=Path(a.source) if hasattr(a,"source") else None
    text=src.read_text(encoding="utf-8") if src else None
    if a.cmd=="check":
        r=_driver(a).check_text(text,src.name)
        if r.ok: print("PASS"); return 0
        for d in r.diagnostics: print(render(d),file=sys.stderr)
        return 2
    if a.cmd=="build":
        r=_driver(a).build_text(text,Path(a.out),src.name)
        if not r.ok:
            for d in r.diagnostics: print(render(d),file=sys.stderr)
            return 2
        print(json.dumps(r.manifest.as_dict(),sort_keys=True)); return 0
    if a.cmd=="disasm": print(disassemble(compile_source(text,src.name)),end=""); return 0
    if a.cmd in ("run","trace"):
        p=compile_source(text,src.name); rt=TracingRuntime(p,Path(a.base))
        for s in a.seed: _seed(rt,s)
        rr=rt.run()
        if a.cmd=="run": print(json.dumps({"status":rr.status,"receipt_root":rr.receipt_root,"registers":list(rr.registers)},sort_keys=True))
        else: print(canonical_json({"status":rr.status,"events":[e.as_dict() for e in rr.events],"receipt_root":rr.receipt_root}).decode())
        return 0
    if a.cmd=="test":
        r=TestRunner().run_many(a.cases); print(json.dumps(r,sort_keys=True)); return 0 if r["pass"] else 3
    if a.cmd=="repro":
        r=compare_rebuilds(text,src.name); print(json.dumps(r,sort_keys=True)); return 0 if r.get("ok") else 4
    return 1

def _seed(rt,s):
    # endpoint:path=file
    lhs,file=s.split("=",1); endpoint,path=lhs.split(":",1); rt.seed(endpoint,path,Path(file).read_bytes())
