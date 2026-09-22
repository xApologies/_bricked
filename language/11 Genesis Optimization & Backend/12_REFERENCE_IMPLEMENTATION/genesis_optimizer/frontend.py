from pathlib import Path
from genesis_frontend import compile_sources
from .codegen import codegen_gir
from .equivalence import compare_execution

def optimize_sources(sources,exports=None,name='genesis_program',level='O1',profile='audit',backend=None):
    br=compile_sources(sources,exports,name,backend)
    art=codegen_gir(br.link.gir,level,profile,backend)
    eq=compare_execution(br.link.gir,art)
    return {'frontend':br,'artifact':art,'equivalence':eq}

def optimize_files(paths,exports=None,name='genesis_program',level='O1',profile='audit',backend=None):
    src=[(str(Path(p)),Path(p).read_text(encoding='utf-8')) for p in paths]
    return optimize_sources(src,exports,name,level,profile,backend)
