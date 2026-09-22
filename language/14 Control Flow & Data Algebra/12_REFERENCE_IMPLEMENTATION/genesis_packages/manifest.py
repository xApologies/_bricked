from dataclasses import dataclass,field
from pathlib import Path
import re
from .semver import Version,Requirement
from .errors import ManifestError
from .util import read_json,package_file_hashes,sha256_obj

NAME_RX=re.compile(r'^[A-Za-z][A-Za-z0-9_.-]*$')
SUPPORTED_SCHEMA='0.1.0'; SUPPORTED_GENESIS='0.1.0'
@dataclass
class PackageManifest:
    path:Path; name:str; version:str; genesis:str; kind:str
    modules:list=field(default_factory=list); dependencies:dict=field(default_factory=dict)
    effects:list=field(default_factory=list); backend_capabilities:list=field(default_factory=list)
    entry_exports:list=field(default_factory=list); description:str=''
    raw:dict=field(default_factory=dict)
    @property
    def root(self): return self.path.parent
    def module_names(self): return [m['name'] for m in self.modules]

def _validate_module(m,root):
    if not isinstance(m,dict) or not NAME_RX.fullmatch(str(m.get('name',''))): raise ManifestError(f'invalid module declaration {m!r}')
    rel=m.get('path')
    if not isinstance(rel,str) or not rel or Path(rel).is_absolute() or '..' in Path(rel).parts: raise ManifestError(f'invalid module path {rel!r}')
    p=root/rel
    if not p.is_file(): raise ManifestError(f'source file missing: {rel}','SOURCE_MISSING')

def load_manifest(path):
    p=Path(path); d=read_json(p)
    if d.get('manifest')!='GENESIS-PACKAGE': raise ManifestError('manifest marker must be GENESIS-PACKAGE')
    if d.get('schema_version')!=SUPPORTED_SCHEMA: raise ManifestError(f'unsupported schema {d.get("schema_version")}')
    name=d.get('name','')
    if not NAME_RX.fullmatch(name): raise ManifestError(f'invalid package name {name!r}')
    Version.parse(d.get('version',''))
    if d.get('genesis')!=SUPPORTED_GENESIS: raise ManifestError(f'unsupported Genesis version {d.get("genesis")!r}','GENESIS_VERSION_UNSUPPORTED')
    kind=d.get('kind')
    if kind not in {'library','contract','application'}: raise ManifestError(f'invalid package kind {kind!r}')
    mods=d.get('modules',[])
    if not isinstance(mods,list): raise ManifestError('modules must be a list')
    seen=set()
    for m in mods:
        _validate_module(m,p.parent)
        if m['name'] in seen: raise ManifestError(f'duplicate module {m["name"]}','MODULE_DUPLICATE')
        seen.add(m['name'])
    deps=d.get('dependencies',{})
    if not isinstance(deps,dict): raise ManifestError('dependencies must be an object')
    for n,r in deps.items():
        if not NAME_RX.fullmatch(n): raise ManifestError(f'invalid dependency name {n!r}')
        Requirement(str(r)) # syntax checked on match/resolve; force basic object
    effects=d.get('effects',[]); caps=d.get('backend_capabilities',[]); ex=d.get('entry_exports',[])
    if not all(isinstance(x,str) for x in effects+caps+ex): raise ManifestError('effects/capabilities/entry_exports must be string lists')
    return PackageManifest(p,name,d['version'],d['genesis'],kind,mods,deps,effects,caps,ex,d.get('description',''),d)

def hash_package(path):
    root=Path(path)
    return sha256_obj({'files':package_file_hashes(root)})
