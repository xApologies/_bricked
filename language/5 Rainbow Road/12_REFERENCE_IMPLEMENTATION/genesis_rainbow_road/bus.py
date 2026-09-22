from .util import digest_obj,now_ns
from .errors import RoadCapacityError

class RoadCapacityManager:
    """Road-level capacity lease over the Section-04 CapacityLedger interface."""
    def __init__(self,base,ledger=None):
        self.base=base; self.ledger=ledger; self.active=None; self.holds={}; self.subreservations={}
    def _event(self,e):
        if self.ledger: self.ledger.append(e)
    def available(self,eid):
        if self.active is None: return self.base.available(eid)
        cap=self.holds[self.active]['by_edge'].get(eid,0)
        used=sum(r['units'] for r in self.subreservations.values() if r['road_id']==self.active and r['state']=='RESERVED' and eid in r['edge_ids'])
        return cap-used
    def begin_road(self,road_id,requirements):
        if self.active is not None: raise RoadCapacityError('another road lease already active')
        reservations=[]; by_edge={}
        try:
            for eid,units in sorted(requirements.items()):
                if units<=0: continue
                rid=self.base.reserve([eid],int(units),f'ROAD:{road_id}:{eid}')
                reservations.append(rid); by_edge[eid]=int(units)
        except Exception:
            for rid in reservations:
                try:self.base.release(rid,'ROAD_HOLD_ABORT')
                except:pass
            raise
        self.holds[road_id]={'road_id':road_id,'reservations':reservations,'by_edge':by_edge,'state':'HELD'}; self.active=road_id
        self._event({'kind':'RAINBOW_BUS_ROAD_HELD','road_id':road_id,'requirements':dict(by_edge),'timestamp_ns':now_ns()}); return dict(self.holds[road_id])
    def reserve(self,edge_ids,units,owner):
        if self.active is None: return self.base.reserve(edge_ids,units,owner)
        for eid in edge_ids:
            if self.available(eid)<units: raise RoadCapacityError('road pool capacity '+eid)
        rid=digest_obj({'road':self.active,'owner':owner,'edges':list(edge_ids),'units':int(units),'ordinal':len(self.subreservations)})[:24]
        self.subreservations[rid]={'reservation_id':rid,'road_id':self.active,'owner':owner,'edge_ids':list(edge_ids),'units':int(units),'state':'RESERVED'}
        self._event({'kind':'ROAD_PORTAL_SUBRESERVED',**self.subreservations[rid]}); return rid
    def release(self,rid,reason='CLOSED'):
        if rid not in self.subreservations: return self.base.release(rid,reason)
        r=self.subreservations[rid]
        if r['state']=='RESERVED': r['state']='RELEASED'; r['release_reason']=reason; self._event({'kind':'ROAD_PORTAL_SUBRELEASED',**r})
        return dict(r)
    def end_road(self,road_id,reason='CLOSED'):
        if road_id not in self.holds: raise RoadCapacityError('unknown road hold')
        h=self.holds[road_id]
        for r in self.subreservations.values():
            if r['road_id']==road_id and r['state']=='RESERVED': raise RoadCapacityError('active portal subreservation remains')
        for rid in h['reservations']: self.base.release(rid,'ROAD_'+reason)
        h['state']='RELEASED'; h['release_reason']=reason; self._event({'kind':'RAINBOW_BUS_ROAD_RELEASED','road_id':road_id,'reason':reason,'timestamp_ns':now_ns()})
        if self.active==road_id:self.active=None
        return dict(h)
