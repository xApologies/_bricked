from pathlib import Path
from .parser import parse_source
from .lower import lower_module
from .util import sha256_obj,sha256_text
from .vendor.genesis_semantics import link_bundle
from .vendor.genesis_semantics.capabilities import reference_backend_capabilities
from .vendor.genesis_semantics.vendor.genesis_vm import VM,decode,disassemble

class BuildResult:
    def __init__(self,asts,modules,link,receipt): self.asts=asts; self.modules=modules; self.link=link; self.receipt=receipt

def compile_sources(sources, exports=None, name='genesis_program', backend=None):
    # sources: iterable[(filename,text)]
    asts=[]; modules=[]; src_hashes={}
    for file,text in sources:
        ast=parse_source(text,file); mod,_=lower_module(ast); asts.append(ast); modules.append(mod); src_hashes[file]=sha256_text(text)
    if exports is None:
        exports=[f'{m["module"]}::{e["symbol"]}' for m in modules for e in m.get('exports',[])]
    bundle={'link':'GENESIS-LINK','version':'0.1.0','name':name,'modules':modules,'exports':exports}
    lr=link_bundle(bundle,backend or reference_backend_capabilities())
    pre={'kind':'GENESIS_FRONTEND_RECEIPT','version':'0.1.0','name':name,'sources':src_hashes,'ast_hashes':{a.module:sha256_obj(a.as_dict()) for a in asts},'module_hashes':{m['module']:sha256_obj(m) for m in modules},'link_id':lr.receipt['link_id'],'gir_hash':lr.receipt['gir_hash'],'gvm_sha256':lr.receipt['gvm_sha256'],'exports':exports}
    receipt=dict(pre); receipt['frontend_id']='gfront-'+sha256_obj(pre)[:24]
    return BuildResult(asts,modules,lr,receipt)

def compile_files(paths,exports=None,name='genesis_program',backend=None):
    return compile_sources([(str(Path(p)),Path(p).read_text(encoding='utf-8')) for p in paths],exports,name,backend)

def run_build(br): return VM().run(decode(br.link.bytecode))
