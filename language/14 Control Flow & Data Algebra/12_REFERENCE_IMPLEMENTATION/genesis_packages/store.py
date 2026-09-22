from pathlib import Path
import shutil
from .manifest import hash_package
from .errors import StoreError

class ContentStore:
    def __init__(self,root): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def install(self,entry):
        actual=hash_package(entry.path)
        if actual!=entry.content_sha256: raise StoreError(f'registry package drift: {entry.name}@{entry.version}')
        dst=self.root/entry.content_sha256
        if not dst.exists(): shutil.copytree(entry.path,dst)
        if hash_package(dst)!=entry.content_sha256:
            shutil.rmtree(dst,ignore_errors=True); raise StoreError(f'store verification failed: {entry.name}@{entry.version}')
        return dst
    def verify(self,content_sha256):
        p=self.root/content_sha256
        return p.is_dir() and hash_package(p)==content_sha256
