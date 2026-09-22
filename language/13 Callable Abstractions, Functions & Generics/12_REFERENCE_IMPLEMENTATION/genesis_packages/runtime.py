from dataclasses import dataclass
from pathlib import Path
from .manifest import load_manifest,hash_package
from .resolver import Resolver
from .lockfile import Lockfile,lock_from_resolution
from .store import ContentStore
from .errors import PackageError
from .semver import Requirement,Version
from .util import sha256_obj,sha256_bytes,write_json
from genesis_frontend import parse_source
from genesis_frontend.lower import lower_module
from genesis_optimizer import optimize_sources
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import VM,decode,disassemble

@dataclass
class PackageBuildResult:
    manifest:object; lockfile:Lockfile; toolchain:dict; execution:object; receipt:dict; package_sources:list

class PackageRuntime:
    def __init__(self,registry,store=None):
        self.registry=registry; self.store=store or ContentStore(Path('.genesis/store'))
    def _resolution_from_lock(self,root,lock):
        d=lock.data
        if d.get('lock')!='GENESIS-LOCK' or d.get('version')!='0.1.0': raise PackageError('invalid lockfile','LOCK_DRIFT')
        if d.get('root',{}).get('name')!=root.name or d['root'].get('version')!=root.version: raise PackageError('root coordinate differs from lock','LOCK_DRIFT')
        if d['root'].get('content_sha256')!=hash_package(root.root): raise PackageError('root content differs from lock','LOCK_DRIFT')
        selected={}
        for x in d.get('packages',[]):
            e=self.registry.get(x['name'],x['version'])
            if e.content_sha256!=x['content_sha256']: raise PackageError(f'locked content drift: {x["name"]}@{x["version"]}','LOCK_DRIFT')
            selected[x['name']]=e
        # Verify all root/direct and package constraints against exactly locked versions.
        for n,r in root.dependencies.items():
            if n not in selected or not Requirement(r).matches(Version.parse(selected[n].version)): raise PackageError(f'lock does not satisfy root dependency {n} {r}','LOCK_DRIFT')
        for n,e in selected.items():
            for dn,dr in e.manifest.dependencies.items():
                if dn not in selected or not Requirement(dr).matches(Version.parse(selected[dn].version)): raise PackageError(f'lock does not satisfy {n} -> {dn} {dr}','LOCK_DRIFT')
        # Verify order and cycle using resolver helper.
        order=Resolver(self.registry)._topological(selected)
        if order!=d.get('order'): raise PackageError('lock order drift','LOCK_DRIFT')
        return {'selected':selected,'order':order,'requirements':{}}
    def resolve(self,project_path,frozen_lock=None):
        root=load_manifest(Path(project_path)/'genesis.pkg.json')
        if root.kind!='application': raise PackageError('root build target must be kind=application','MANIFEST_INVALID')
        if frozen_lock:
            lock=Lockfile.read(frozen_lock) if not isinstance(frozen_lock,Lockfile) else frozen_lock
            res=self._resolution_from_lock(root,lock)
            return root,res,lock
        res=Resolver(self.registry).resolve(root); lock=lock_from_resolution(root,res); return root,res,lock
    def _packages(self,root,res):
        return [(n,res['selected'][n].manifest) for n in res['order']]+[(root.name,root)]
    def audit(self,root,res):
        packs=self._packages(root,res); module_owner={}; modules={}
        for pn,m in packs:
            for md in m.modules:
                mn=md['name']
                if mn in module_owner: raise PackageError(f'module {mn} owned by both {module_owner[mn]} and {pn}','MODULE_DUPLICATE')
                module_owner[mn]=pn; modules[mn]=(m,m.root/md['path'])
        package_effects={}; package_caps={pn:sorted(set(m.backend_capabilities)) for pn,m in packs}
        for pn,m in packs:
            used=set()
            for md in m.modules:
                p=m.root/md['path']; ast=parse_source(p.read_text(encoding='utf-8'),str(p))
                if ast.module!=md['name']: raise PackageError(f'module declaration {ast.module} differs from manifest {md["name"]}','MANIFEST_INVALID')
                # direct dependency discipline
                allowed=set(m.dependencies)
                for imp in ast.imports:
                    owner=module_owner.get(imp.module)
                    if owner is None: raise PackageError(f'{pn} imports unknown module {imp.module}','MODULE_UNRESOLVED')
                    if owner!=pn and owner not in allowed: raise PackageError(f'{pn} imports transitive/non-direct module {imp.module} owned by {owner}','DIRECT_DEPENDENCY_REQUIRED')
                mod,_=lower_module(ast); used |= set(mod.get('effects',[]))
            extra=used-set(m.effects)
            if extra: raise PackageError(f'{pn} undeclared effects: '+','.join(sorted(extra)),'EFFECT_BUDGET_EXCEEDED')
            package_effects[pn]=sorted(used)
        return {'module_owner':module_owner,'effects':package_effects,'capabilities':package_caps}
    def build(self,project_path,frozen_lock=None,optimization='O1',profile='audit',execute=True):
        project_path=Path(project_path); root,res,lock=self.resolve(project_path,frozen_lock)
        installed={n:str(self.store.install(res['selected'][n])) for n in res['order']}
        audit=self.audit(root,res)
        sources=[]; source_packages=[]
        for pn,m in self._packages(root,res):
            for md in m.modules:
                p=m.root/md['path']; sources.append((str(p),p.read_text(encoding='utf-8'))); source_packages.append({'package':pn,'module':md['name'],'path':str(p)})
        tool=optimize_sources(sources,exports=root.entry_exports or None,name=root.name,level=optimization,profile=profile)
        if tool['equivalence']['status']!='PASS': raise PackageError('optimizer differential equivalence failed','TOOLCHAIN_FAILURE')
        execution=VM().run(decode(tool['artifact'].bytecode)) if execute else None
        if execute and not execution.halted: raise PackageError('reference VM did not halt','TOOLCHAIN_FAILURE')
        pre={'kind':'GENESIS_PACKAGE_BUILD_RECEIPT','version':'0.1.0','package':root.name,'package_version':root.version,'root_content_sha256':hash_package(root.root),'resolution_root':lock.resolution_root,'dependency_order':res['order'],'installed_content':installed,'source_modules':source_packages,'effect_audit':audit['effects'],'capability_declarations':audit['capabilities'],'frontend_id':tool['frontend'].receipt['frontend_id'],'optimization_id':tool['artifact'].optimization_receipt['optimization_id'],'codegen_id':tool['artifact'].codegen_receipt['codegen_id'],'gvm_sha256':tool['artifact'].codegen_receipt['gvm_sha256'],'equivalence':tool['equivalence']['status'],'halted':bool(execution.halted) if execution else None}
        receipt=dict(pre); receipt['package_build_id']='gpkg-'+sha256_obj(pre)[:24]
        return PackageBuildResult(root,lock,tool,execution,receipt,source_packages)
    def write_build(self,result,outdir):
        out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
        result.lockfile.write(out/'genesis.lock.json')
        (out/'program.gvm').write_bytes(result.toolchain['artifact'].bytecode)
        write_json(out/'PACKAGE_BUILD_RECEIPT.json',result.receipt)
        write_json(out/'OPTIMIZATION_RECEIPT.json',result.toolchain['artifact'].optimization_receipt)
        write_json(out/'CODEGEN_RECEIPT.json',result.toolchain['artifact'].codegen_receipt)
        write_json(out/'EXECUTION_SUMMARY.json',{'halted':result.execution.halted if result.execution else None,'steps':result.execution.receipt.get('steps') if result.execution else None,'receipt_id':result.execution.receipt.get('resource_id') if result.execution else None})
        (out/'program.disasm.txt').write_text(disassemble(decode(result.toolchain['artifact'].bytecode))+'\n',encoding='utf-8')
        return out

PackageError=PackageError
