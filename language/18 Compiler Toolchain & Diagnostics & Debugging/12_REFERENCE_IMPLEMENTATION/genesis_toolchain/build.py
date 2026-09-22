from __future__ import annotations
import json,shutil,tempfile
from pathlib import Path
from genesis_system_io.compiler import compile_source
from genesis_system_io.bytecode import encode,decode
from genesis_system_io.disasm import disassemble
from genesis_system_io.errors import GenesisSystemError
from .model import BuildResult,BuildManifest,ArtifactDigest
from .diagnostics import from_exception
from .source_map import build_source_map
from .util import canonical_json,sha256_bytes,sha256_file,digest_obj,stable_write

TOOLCHAIN_VERSION="0.1.0"
DEFAULT_TARGET="gcm-system-v0.6"

class BuildDriver:
    def __init__(self,target:str=DEFAULT_TARGET,profile:str="debug",options:dict|None=None):
        self.target=target; self.profile=profile; self.options=dict(options or {})
    def check_text(self,text:str,source_name:str="<memory>")->BuildResult:
        try:
            p=compile_source(text,source_name)
            m=self._manifest_base(text,source_name,p)
            return BuildResult(True,m,[])
        except Exception as e:
            return BuildResult(False,None,[from_exception(e,text,source_name)])
    def build_text(self,text:str,out_dir:Path,source_name:str="main.gen")->BuildResult:
        out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
        try:
            p=compile_source(text,source_name)
            blob=encode(p); decoded=decode(blob)
            dis=disassemble(decoded)
            sm=[x.as_dict() for x in build_source_map(p,text,source_name)]
            proof=p.metadata.get("verification",{})
            # normalized build id excludes output path and wall clock
            base=self._manifest_base(text,source_name,p)
            semantic={
                "bytecode.gio":blob,
                "disassembly.txt":dis.encode(),
                "proof.json":canonical_json(proof),
                "source_map.json":canonical_json(sm),
            }
            paths={}
            for name,data in semantic.items():
                path=out/name; stable_write(path,data); paths[name]=str(path)
            arts=tuple(ArtifactDigest(name,sha256_bytes(data),len(data)) for name,data in sorted(semantic.items()))
            m=BuildManifest(base.build_id,base.toolchain_version,base.target,base.profile,base.source_name,base.source_digest,base.program_id,base.proof_root,base.instruction_count,base.options,arts)
            mp=out/"build_manifest.json"; stable_write(mp,canonical_json(m.as_dict())); paths["build_manifest.json"]=str(mp)
            return BuildResult(True,m,[],str(out),paths)
        except Exception as e:
            return BuildResult(False,None,[from_exception(e,text,source_name)],str(out),{})
    def build_file(self,source:Path,out_dir:Path)->BuildResult:
        source=Path(source); return self.build_text(source.read_text(encoding="utf-8"),out_dir,source.name)
    def _manifest_base(self,text,source_name,p):
        src=text.encode("utf-8"); source_digest=sha256_bytes(src)
        config={"toolchain_version":TOOLCHAIN_VERSION,"target":self.target,"profile":self.profile,"source_name":source_name,"source_digest":source_digest,"options":self.options}
        build_id="build:"+digest_obj(config)
        proof=p.metadata.get("verification",{})
        return BuildManifest(build_id,TOOLCHAIN_VERSION,self.target,self.profile,source_name,source_digest,p.metadata.get("program_id",""),proof.get("proof_root",""),len(p.instructions),dict(self.options),())

def compare_rebuilds(text:str,source_name:str="main.gen",driver:BuildDriver|None=None)->dict:
    d=driver or BuildDriver()
    with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
        ra=d.build_text(text,Path(a),source_name); rb=d.build_text(text,Path(b),source_name)
        if not ra.ok or not rb.ok: return {"ok":False,"diagnostics":[x.as_dict() for x in (ra.diagnostics+rb.diagnostics)]}
        names=sorted(set(ra.artifact_paths)&set(rb.artifact_paths))
        cmp={n:sha256_file(Path(ra.artifact_paths[n]))==sha256_file(Path(rb.artifact_paths[n])) for n in names}
        return {"ok":all(cmp.values()) and ra.manifest.build_id==rb.manifest.build_id,"build_id":ra.manifest.build_id,"artifacts":cmp}
