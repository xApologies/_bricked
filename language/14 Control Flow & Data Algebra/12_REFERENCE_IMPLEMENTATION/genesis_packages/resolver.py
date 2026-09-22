from copy import deepcopy
from .semver import Requirement,Version
from .errors import ResolutionError,PackageError

class Resolver:
    def __init__(self,registry): self.registry=registry
    def resolve(self,root_manifest):
        req={n:[str(r)] for n,r in root_manifest.dependencies.items()}
        selected=self._solve(req,{})
        if selected is None:
            detail=', '.join(f'{n}:{" & ".join(v)}' for n,v in sorted(req.items()))
            raise ResolutionError('no compatible dependency solution for '+detail)
        order=self._topological(selected)
        return {'selected':selected,'order':order,'requirements':req}
    def _compatible_selected(self,req,selected):
        for n,e in selected.items():
            for r in req.get(n,[]):
                if not Requirement(r).matches(Version.parse(e.version)): return False
        return True
    def _solve(self,req,selected):
        if not self._compatible_selected(req,selected): return None
        unresolved=sorted(n for n in req if n not in selected)
        if not unresolved: return selected
        # deterministic smallest candidate set, then name
        ranked=[]
        for n in unresolved:
            c=[e for e in self.registry.versions(n) if all(Requirement(r).matches(Version.parse(e.version)) for r in req[n])]
            if not c: return None
            ranked.append((len(c),n,c))
        _,name,cands=sorted(ranked,key=lambda x:(x[0],x[1]))[0]
        for e in cands:
            s2=dict(selected); s2[name]=e; r2=deepcopy(req)
            for dn,dr in sorted(e.manifest.dependencies.items()): r2.setdefault(dn,[]).append(str(dr))
            ans=self._solve(r2,s2)
            if ans is not None: return ans
        return None
    def _topological(self,selected):
        names=set(selected); deps={n:set(selected[n].manifest.dependencies) & names for n in names}
        out=[]; ready=sorted(n for n,d in deps.items() if not d)
        while ready:
            n=ready.pop(0); out.append(n)
            for x in sorted(names-set(out)):
                if n in deps[x]:
                    deps[x].remove(n)
                    if not deps[x] and x not in ready: ready.append(x); ready.sort()
        if len(out)!=len(names): raise ResolutionError('package dependency cycle: '+','.join(sorted(names-set(out))),'DEPENDENCY_CYCLE')
        return out
