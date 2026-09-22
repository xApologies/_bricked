from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .util import short_id, sha256_obj
from .errors import RuntimeFault, ClosureError, SectorError

@dataclass
class ReferenceBackend:
    backend_id: str='python-reference-backend'
    version: str='0.1.0'
    resources: dict[str,dict[str,Any]]=field(default_factory=dict)
    ledger: list[dict[str,Any]]=field(default_factory=list)
    overlay: dict[tuple[str,str],Any]=field(default_factory=dict)

    def _put(self, kind, payload, parents=(), sector=None, typestate='CLOSED'):
        body={'kind':kind,'payload':payload,'parents':list(parents),'sector':sector,'typestate':typestate}
        rid=short_id(kind.lower(),body)
        res={'resource_id':rid,**body,'content_hash':sha256_obj(body)}
        self.resources[rid]=res
        return res
    def _receipt(self, op, payload, parents=()):
        rec=self._put('RECEIPT',{'op':op,**payload},parents=parents,typestate='CLOSED')
        self.ledger.append(rec)
        return rec
    def mount_fabric(self, uri): return self._put('FABRIC',{'uri':uri,'immutable_base':True})
    def alloc(self, fabric, cells): return self._put('REGION',{'fabric':fabric['resource_id'],'cells':int(cells)},parents=[fabric['resource_id']])
    def read_fabric(self, fabric, addr):
        key=(fabric['resource_id'],str(addr)); return self.overlay.get(key, {'base':'reference','addr':addr})
    def write_overlay(self, fabric, addr, value):
        key=(fabric['resource_id'],str(addr)); self.overlay[key]=value
        return self._receipt('FABRIC_WRITE_OVERLAY',{'fabric':fabric['resource_id'],'addr':addr,'value_hash':sha256_obj(value)},[fabric['resource_id']])
    def instantiate(self, fabric, region, mmo):
        return self._put('GEOMETRIC',{'mmo':mmo,'fabric':fabric['resource_id'],'region':region['resource_id'],'closed':True},[fabric['resource_id'],region['resource_id']])
    def fork(self, geo, attrs):
        return self._put('GEOMETRIC',{'fork_of':geo['resource_id'],'attrs':attrs,'closed':True},[geo['resource_id']],sector=geo.get('sector'))
    def relate(self, geo, target, attrs): return self._put('RELATION',{'source':geo['resource_id'],'target':target,'attrs':attrs},[geo['resource_id']])
    def admit(self, geo, attrs): return self._put('ADMISSION',{'source':geo['resource_id'],'attrs':attrs,'admitted':attrs.get('admitted',True)},[geo['resource_id']])
    def transform(self, geo, admission, attrs):
        if not admission['payload'].get('admitted'): raise RuntimeFault('TRANSFORM_INADMISSIBLE')
        return self._put('GEOMETRIC',{'parent':geo['resource_id'],'transform':attrs,'closed':True},[geo['resource_id'],admission['resource_id']],sector=geo.get('sector'))
    def inherit(self, resource, attrs): return self._receipt('INHERIT',{'resource':resource['resource_id'],'attrs':attrs},[resource['resource_id']])
    def portal_open(self, geo, admission, sector, attrs):
        if not admission['payload'].get('admitted'): raise RuntimeFault('PORTAL_INADMISSIBLE')
        return self._put('PORTAL',{'source':geo['resource_id'],'admission':admission['resource_id'],'attrs':attrs},[geo['resource_id'],admission['resource_id']],sector=sector,typestate='OPEN')
    def portal_transport(self, portal, geo, attrs):
        if portal['typestate']!='OPEN': raise ClosureError('portal not open')
        sector=portal.get('sector')
        return self._put('GEOMETRIC',{'transported_from':geo['resource_id'],'portal':portal['resource_id'],'closed':True,'attrs':attrs},[geo['resource_id'],portal['resource_id']],sector=sector)
    def portal_close(self, portal, dest):
        if portal['typestate']!='OPEN': raise ClosureError('portal already closed')
        portal['typestate']='CLOSED'
        return self._receipt('PORTAL_CLOSE',{'portal':portal['resource_id'],'destination':dest['resource_id'],'sector':portal.get('sector')},[portal['resource_id'],dest['resource_id']])
    def road_begin(self, geo, attrs): return self._put('ROAD',{'source':geo['resource_id'],'legs':[],'attrs':attrs},[geo['resource_id']],typestate='OPEN')
    def road_append(self, road, receipt):
        if road['typestate']!='OPEN': raise ClosureError('road not open')
        legs=list(road['payload']['legs'])+[receipt['resource_id']]
        # Road values are persistent/versioned; original road remains valid history.
        return self._put('ROAD',{'source':road['payload']['source'],'legs':legs,'attrs':road['payload'].get('attrs',{})},[road['resource_id'],receipt['resource_id']],typestate='OPEN')
    def road_close(self, road, geo):
        if road['typestate']!='OPEN': raise ClosureError('road not open')
        road['typestate']='CLOSED'
        return self._receipt('ROAD_CLOSE',{'road':road['resource_id'],'destination':geo['resource_id'],'legs':road['payload']['legs']},[road['resource_id'],geo['resource_id']])
    def bridge(self, geo, from_sector, to_sector, attrs):
        if from_sector==to_sector: raise SectorError('bridge requires sector change')
        return self._put('BRIDGE',{'geometric':geo['resource_id'],'from':from_sector,'to':to_sector,'attrs':attrs},[geo['resource_id']],sector=to_sector)
    def q_prepare(self, geo, attrs): return self._put('QSTATE',{'geometric':geo['resource_id'],'state':'PREPARED','attrs':attrs},[geo['resource_id']],sector='QFT',typestate='OWNED')
    def q_successor(self, op, states, attrs):
        for s in states:
            if s['typestate']!='OWNED': raise RuntimeFault('QSTATE_NOT_OWNED')
        for s in states: s['typestate']='MOVED'
        return self._put('QSTATE',{'op':op,'inputs':[s['resource_id'] for s in states],'attrs':attrs},[s['resource_id'] for s in states],sector='QFT',typestate='OWNED')
    def q_measure(self, state, attrs):
        if state['typestate']!='OWNED': raise RuntimeFault('QSTATE_NOT_OWNED')
        state['typestate']='MEASURED'
        outcome=attrs.get('outcome',0)
        return self._put('QRESULT',{'state':state['resource_id'],'outcome':outcome,'classical':True},[state['resource_id']],sector='QFT')
    def brane_lift(self, geo, attrs): return self._put('M5',{'geometric':geo['resource_id'],'I':geo['resource_id'],'D':attrs.get('D','derived'),'Chi':attrs.get('Chi','preserved'),'R':attrs.get('R','history'),'P':attrs.get('P','ledger')},[geo['resource_id']])
    def provenance_seal(self, resource, attrs): return self._receipt('PROVENANCE_SEAL',{'resource':resource['resource_id'],'attrs':attrs},[resource['resource_id']])
    def assert_closure(self, resource):
        return resource.get('typestate') in ('CLOSED','MEASURED') or bool(resource.get('payload',{}).get('closed'))
    def execution_receipt(self, payload): return self._receipt('GVM_EXECUTION',payload)
