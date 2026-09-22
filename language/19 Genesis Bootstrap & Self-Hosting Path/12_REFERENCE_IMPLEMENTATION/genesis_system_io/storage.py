from __future__ import annotations
from pathlib import Path
import os
from .errors import fail
from .util import object_ref, sha256_bytes

class SandboxFS:
    def __init__(self, roots: dict[str,Path]):
        self.roots={k:Path(v).resolve() for k,v in roots.items()}
        for p in self.roots.values(): p.mkdir(parents=True,exist_ok=True)
    def _path(self,root_name:str,rel:str)->Path:
        if root_name not in self.roots: fail("SYSTEM_ENDPOINT_ROOT",root_name)
        root=self.roots[root_name]
        p=(root/rel).resolve()
        try: p.relative_to(root)
        except ValueError: fail("SYSTEM_PATH_ESCAPE",rel)
        return p
    def read(self,root:str,rel:str)->bytes:
        p=self._path(root,rel)
        if not p.is_file(): fail("SYSTEM_FILE_MISSING",rel)
        return p.read_bytes()
    def write_derived(self,root:str,rel:str,data:bytes)->str:
        p=self._path(root,rel); p.parent.mkdir(parents=True,exist_ok=True)
        tmp=p.with_name(p.name+".tmp")
        tmp.write_bytes(data); os.replace(tmp,p)
        return object_ref(data)
    def append_audit(self,root:str,rel:str,data:bytes)->str:
        p=self._path(root,rel); p.parent.mkdir(parents=True,exist_ok=True)
        with p.open("ab") as f: f.write(data)
        return "sha256:"+sha256_bytes(p.read_bytes())

class CASStore:
    def __init__(self,root:Path): self.root=Path(root).resolve(); self.root.mkdir(parents=True,exist_ok=True)
    def _path(self,ref:str)->Path:
        if not ref.startswith("sha256:") or len(ref)!=71: fail("CAS_REF_INVALID",ref)
        h=ref.split(":",1)[1]
        if any(c not in "0123456789abcdef" for c in h): fail("CAS_REF_INVALID",ref)
        return self.root/h[:2]/h
    def put(self,data:bytes)->str:
        ref=object_ref(data); p=self._path(ref); p.parent.mkdir(parents=True,exist_ok=True)
        if p.exists():
            if p.read_bytes()!=data: fail("CAS_INTEGRITY_FAILURE",ref)
        else:
            tmp=p.with_name(p.name+".tmp"); tmp.write_bytes(data); os.replace(tmp,p)
        return ref
    def get(self,ref:str)->bytes:
        p=self._path(ref)
        if not p.is_file(): fail("CAS_OBJECT_MISSING",ref)
        data=p.read_bytes()
        if object_ref(data)!=ref: fail("CAS_INTEGRITY_FAILURE",ref)
        return data
