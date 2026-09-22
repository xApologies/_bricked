import argparse,json
from pathlib import Path
from .compiler import compile_sources,run_callable_build
p=argparse.ArgumentParser(prog='genesis-callables')
p.add_argument('sources',nargs='+'); p.add_argument('--name',default='genesis_callable_program'); p.add_argument('--run',action='store_true'); p.add_argument('--expanded-dir')
a=p.parse_args(); src=[(x,Path(x).read_text(encoding='utf-8')) for x in a.sources]
r=compile_sources(src,name=a.name)
if a.expanded_dir:
    d=Path(a.expanded_dir); d.mkdir(parents=True,exist_ok=True)
    for f,t in r.expanded_sources: (d/Path(f).name).write_text(t,encoding='utf-8')
out={'receipt':r.callable_receipt,'proofs':r.callable_proofs,'calls':[x.as_dict() for x in r.expansion_records]}
if a.run: out['execution']=run_callable_build(r).receipt
print(json.dumps(out,indent=2,sort_keys=True))
