from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .model import ResourceSpec, ClaimMode
from .errors import ConcurrencyError
from .util import sha256_obj

@dataclass
class ResourceRuntime:
    spec: ResourceSpec
    holders: dict[str, dict[str, Any]] = field(default_factory=dict)
    waiters: list[tuple[int, str, str, int]] = field(default_factory=list)  # seq, task, mode, units

class ResourceManager:
    def __init__(self, specs: dict[str, ResourceSpec]):
        self.resources={k:ResourceRuntime(v) for k,v in specs.items()}
    def _get(self,name):
        if name not in self.resources: raise ConcurrencyError(f'unknown resource {name}','RESOURCE_UNKNOWN')
        return self.resources[name]
    def available(self,name):
        rr=self._get(name); used=sum(int(v['units']) for v in rr.holders.values()); return rr.spec.capacity-used
    def can_acquire(self,task_id,name,mode,units=1):
        rr=self._get(name); mode=ClaimMode(mode)
        if units<1 or units>rr.spec.capacity: return False
        if task_id in rr.holders: return False
        if mode is ClaimMode.EXCLUSIVE: return not rr.holders and units==rr.spec.capacity
        if any(v['mode']==ClaimMode.EXCLUSIVE.value for v in rr.holders.values()): return False
        return self.available(name)>=units
    def acquire(self,task_id,name,mode,units=1):
        rr=self._get(name); mode=ClaimMode(mode)
        if mode is ClaimMode.EXCLUSIVE: units=rr.spec.capacity
        if not self.can_acquire(task_id,name,mode,units): return None
        lease={'resource':name,'task_id':task_id,'mode':mode.value,'units':units}
        lease['lease_id']='lease-'+sha256_obj(lease)[:24]
        rr.holders[task_id]=lease
        rr.waiters=[x for x in rr.waiters if x[1]!=task_id]
        return lease
    def enqueue_waiter(self,task_id,name,mode,units,seq):
        rr=self._get(name)
        if not any(x[1]==task_id for x in rr.waiters): rr.waiters.append((int(seq),task_id,ClaimMode(mode).value,int(units)))
        rr.waiters.sort(key=lambda x:(x[0],x[1]))
    def release(self,task_id,name):
        rr=self._get(name)
        if task_id not in rr.holders: raise ConcurrencyError(f'{task_id} does not hold {name}','RESOURCE_NOT_HELD')
        return rr.holders.pop(task_id)
    def release_all(self,task_id):
        out=[]
        for name,rr in self.resources.items():
            if task_id in rr.holders: out.append(rr.holders.pop(task_id))
            rr.waiters=[x for x in rr.waiters if x[1]!=task_id]
        return out
    def holders(self,name): return dict(self._get(name).holders)
    def waiting(self,name): return list(self._get(name).waiters)
    def snapshot(self):
        return {n:{'capacity':r.spec.capacity,'kind':r.spec.kind,'holders':dict(sorted(r.holders.items())),'waiters':list(r.waiters)} for n,r in sorted(self.resources.items())}
