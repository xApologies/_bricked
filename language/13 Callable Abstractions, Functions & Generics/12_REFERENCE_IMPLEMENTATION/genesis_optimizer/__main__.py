import argparse,json
from pathlib import Path
from .frontend import optimize_files
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import disassemble

def main():
    ap=argparse.ArgumentParser(prog='genesis-opt')
    ap.add_argument('sources',nargs='+'); ap.add_argument('-o','--out',required=True); ap.add_argument('-O','--level',default='O1',choices=['O0','OAUDIT','O1']); ap.add_argument('--profile',default='audit',choices=['reference','audit','compact']); ap.add_argument('--name',default='genesis_program')
    a=ap.parse_args(); r=optimize_files(a.sources,name=a.name,level=a.level,profile=a.profile); out=Path(a.out); out.mkdir(parents=True,exist_ok=True); art=r['artifact']
    (out/(a.name+'.optimized.gir.json')).write_text(json.dumps(art.gir,indent=2,sort_keys=True)+'
')
    (out/(a.name+'.gvm')).write_bytes(art.bytecode)
    (out/(a.name+'.disasm.txt')).write_text(disassemble(art.program)+'
')
    (out/(a.name+'.optimization.json')).write_text(json.dumps(art.optimization_receipt,indent=2,sort_keys=True)+'
')
    (out/(a.name+'.codegen.json')).write_text(json.dumps(art.codegen_receipt,indent=2,sort_keys=True)+'
')
    (out/(a.name+'.equivalence.json')).write_text(json.dumps(r['equivalence'],indent=2,sort_keys=True)+'
')
    if r['equivalence']['status']!='PASS': raise SystemExit(2)
if __name__=='__main__': main()
