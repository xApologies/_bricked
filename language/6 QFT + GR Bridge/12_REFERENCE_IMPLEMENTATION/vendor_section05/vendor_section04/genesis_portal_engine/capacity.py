from pathlib import Path
import json,hashlib
from .util import digest_obj,stable_json,now_ns
from .errors import CapacityError

class CapacityLedger:
    def __init__(self,edge_capacities,ledger_path=None):
        self.capacity=dict(edge_capacities); self.reservations={}; self.ledger_path=Path(ledger_path) if ledger_path else None; self.prev='0'*64
        if self.ledger_path: self.ledger_path.parent.mkdir(parents=True,exist_ok=True)
    def used(self,eid): return sum(r['units'] for r in self.reservations.values() if r['state']=='RESERVED' and eid in r['edge_ids'])
    def available(self,eid): return self.capacity[eid]-self.used(eid)
    def _append(self,event):
        body={'prev_hash':self.prev,'event':event,'timestamp_ns':now_ns()}; h=hashlib.sha256(stable_json(body)).hexdigest(); body['entry_hash']=h; self.prev=h
        if self.ledger_path:
            with self.ledger_path.open('a',encoding='utf-8') as f:f.write(json.dumps(body,sort_keys=True,separators=(',',':'))+'\n')
        return body
    def reserve(self,edge_ids,units,owner):
        for eid in edge_ids:
            if self.available(eid)<units: raise CapacityError('capacity '+eid)
        rid=digest_obj({'owner':owner,'edges':list(edge_ids),'units':units,'ordinal':len(self.reservations)})[:24]
        self.reservations[rid]={'reservation_id':rid,'owner':owner,'edge_ids':list(edge_ids),'units':int(units),'state':'RESERVED'}; self._append({'kind':'ROUTE_CAPACITY_RESERVED',**self.reservations[rid]}); return rid
    def release(self,rid,reason='CLOSED'):
        if rid not in self.reservations: raise CapacityError('unknown reservation')
        r=self.reservations[rid]
        if r['state']!='RESERVED': return dict(r)
        r['state']='RELEASED'; r['release_reason']=reason; self._append({'kind':'ROUTE_CAPACITY_RELEASED',**r}); return dict(r)
