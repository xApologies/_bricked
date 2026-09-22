from dataclasses import dataclass
from pathlib import Path
from .manifest import load_manifest,hash_package
from .semver import Version
from .errors import PackageError

@dataclass(frozen=True)
class RegistryEntry:
    name:str; version:str; path:Path; content_sha256:str; manifest:object

class LocalRegistry:
    def __init__(self,root): self.root=Path(root); self._entries=None
    def scan(self,force=False):
        if self._entries is not None and not force: return self._entries
        out={}
        if not self.root.exists(): self._entries={}; return self._entries
        for mf in sorted(self.root.glob('*/*/genesis.pkg.json')):
            m=load_manifest(mf); expected_name=mf.parent.parent.name; expected_version=mf.parent.name
            if m.name!=expected_name or m.version!=expected_version: raise PackageError(f'registry coordinate mismatch for {mf}','MANIFEST_INVALID')
            e=RegistryEntry(m.name,m.version,m.root,hash_package(m.root),m)
            out[(m.name,m.version)]=e
        self._entries=out; return out
    def versions(self,name):
        es=[e for (n,_),e in self.scan().items() if n==name]
        return sorted(es,key=lambda e:Version.parse(e.version),reverse=True)
    def get(self,name,version):
        e=self.scan().get((name,version))
        if e is None: raise PackageError(f'package not found: {name}@{version}','DEPENDENCY_MISSING')
        return e
    def names(self): return sorted({n for n,_ in self.scan()})
