from dataclasses import dataclass
from .util import sha256_obj,read_json,write_json

@dataclass
class Lockfile:
    data:dict
    @property
    def resolution_root(self): return self.data['resolution_root']
    def write(self,path): write_json(path,self.data)
    @classmethod
    def read(cls,path): return cls(read_json(path))

def lock_from_resolution(root_manifest,resolution,resolver_version='section12-v0.1.0'):
    packages=[]
    for n in resolution['order']:
        e=resolution['selected'][n]
        packages.append({'name':n,'version':e.version,'content_sha256':e.content_sha256,'dependencies':dict(sorted(e.manifest.dependencies.items())),'modules':e.manifest.module_names()})
    root={'name':root_manifest.name,'version':root_manifest.version,'content_sha256':__import__('genesis_packages.manifest',fromlist=['hash_package']).hash_package(root_manifest.root),'dependencies':dict(sorted(root_manifest.dependencies.items()))}
    pre={'lock':'GENESIS-LOCK','version':'0.1.0','resolver':resolver_version,'root':root,'packages':packages,'order':resolution['order']}
    data=dict(pre); data['resolution_root']=sha256_obj(pre)
    return Lockfile(data)
