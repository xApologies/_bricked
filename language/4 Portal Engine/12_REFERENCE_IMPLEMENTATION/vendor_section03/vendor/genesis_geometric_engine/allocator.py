from dataclasses import dataclass, asdict
import hashlib, json
from .model import FabricRegion
from .errors import AllocationError

class RegionAllocator:
    def __init__(self, cell_count, alignment=128):
        self.cell_count=int(cell_count); self.alignment=max(1,int(alignment)); self.entries=[]
    def _align(self, x):
        a=self.alignment; return ((x+a-1)//a)*a
    def occupied(self):
        return sorted([e for e in self.entries if e['state'] in ('RESERVED','COMMITTED')], key=lambda e:e['start'])
    def reserve(self, count, owner, guard=0):
        count=int(count); guard=int(guard)
        if count <= 0: raise AllocationError('count')
        need=count+2*guard
        pos=0
        for e in self.occupied()+[{'start':self.cell_count,'count':0}]:
            candidate=self._align(pos+guard)-guard
            if candidate < 0: candidate=0
            if candidate+need <= e['start']:
                usable=self._align(candidate+guard)
                start=usable
                if start+count+guard > e['start']:
                    pos=e['start']+e['count']; continue
                rid=hashlib.sha256(f'{owner}:{start}:{count}:{len(self.entries)}'.encode()).hexdigest()[:24]
                self.entries.append({'reservation_id':rid,'owner':owner,'start':start,'count':count,'guard':guard,'state':'RESERVED'})
                return rid, FabricRegion(start,count,self.alignment,guard,guard)
            pos=max(pos,e['start']+e['count'])
        raise AllocationError(f'insufficient fabric: need {count} cells')
    def commit(self, reservation_id):
        for e in self.entries:
            if e['reservation_id']==reservation_id and e['state']=='RESERVED':
                e['state']='COMMITTED'; return dict(e)
        raise AllocationError('unknown or non-reserved reservation')
    def abort(self, reservation_id):
        for e in self.entries:
            if e['reservation_id']==reservation_id and e['state']=='RESERVED':
                e['state']='ABORTED'; return dict(e)
        raise AllocationError('unknown reservation')
    def release_owner(self, owner):
        changed=[]
        for e in self.entries:
            if e['owner']==owner and e['state']=='COMMITTED': e['state']='RELEASED'; changed.append(dict(e))
        return changed
    def snapshot(self): return {'cell_count':self.cell_count,'alignment':self.alignment,'entries':list(self.entries)}
