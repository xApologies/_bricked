import argparse,json,pathlib
from . import parse_source,lower_module,compile_files,run_build,format_source
from .vendor.genesis_semantics.vendor.genesis_vm import disassemble

def main():
    ap=argparse.ArgumentParser(prog='genesis_frontend'); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('parse'); p.add_argument('source')
    l=sp.add_parser('lower'); l.add_argument('source')
    b=sp.add_parser('build'); b.add_argument('sources',nargs='+'); b.add_argument('-o','--out',required=True); b.add_argument('--export',action='append')
    r=sp.add_parser('run'); r.add_argument('sources',nargs='+'); r.add_argument('--export',action='append')
    f=sp.add_parser('fmt'); f.add_argument('source')
    a=ap.parse_args()
    if a.cmd=='parse':
        path=pathlib.Path(a.source); print(json.dumps(parse_source(path.read_text(),str(path)).as_dict(),indent=2,sort_keys=True))
    elif a.cmd=='lower':
        path=pathlib.Path(a.source); mod,_=lower_module(parse_source(path.read_text(),str(path))); print(json.dumps(mod,indent=2,sort_keys=True))
    elif a.cmd=='build':
        br=compile_files(a.sources,a.export); pathlib.Path(a.out).write_bytes(br.link.bytecode); print(json.dumps(br.receipt,indent=2,sort_keys=True))
    elif a.cmd=='run':
        br=compile_files(a.sources,a.export); rr=run_build(br); print(json.dumps({'frontend':br.receipt,'execution':rr.receipt,'exports':{str(k):v.value for k,v in rr.exports.items()}},indent=2,sort_keys=True,default=str))
    else:
        p=pathlib.Path(a.source); p.write_text(format_source(p.read_text()),encoding='utf-8')
if __name__=='__main__': main()
