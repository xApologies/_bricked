import argparse,json
from pathlib import Path
from .registry import LocalRegistry
from .store import ContentStore
from .runtime import PackageRuntime

def main():
    ap=argparse.ArgumentParser(prog='genesis-pkg')
    ap.add_argument('project'); ap.add_argument('--registry',required=True); ap.add_argument('--store',default='.genesis/store'); ap.add_argument('--out',default='build')
    ap.add_argument('--frozen-lock'); ap.add_argument('-O',dest='opt',default='O1',choices=['O0','OAUDIT','O1']); ap.add_argument('--profile',default='audit',choices=['audit','reference','compact'])
    a=ap.parse_args(); rt=PackageRuntime(LocalRegistry(a.registry),ContentStore(a.store)); r=rt.build(a.project,a.frozen_lock,a.opt,a.profile,True); rt.write_build(r,a.out); print(json.dumps(r.receipt,indent=2,sort_keys=True))
if __name__=='__main__': main()
