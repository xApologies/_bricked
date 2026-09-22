from dataclasses import asdict
from .model import QuantumEffectEnvelope,QuantumPreservation
from .effects import EffectChecker
from .audit import audit_transition
from .util import digest,now_ns
from .errors import QuantumSectorViolation,QuantumClosureError

class QuantumPortalEngine:
    def __init__(self,ownership,ledger=None): self.ownership=ownership; self.effects=EffectChecker(); self.ledger=ledger
    def transport(self,state,envelope,channel,ordinary_portal_receipt=None):
        if state.sector!='QFT': raise QuantumSectorViolation('quantum transport requires QFT state')
        if envelope.source_address.get('sector')!='QFT' or envelope.target_address.get('sector')!='QFT': raise QuantumSectorViolation('Portal<QFT> required')
        self.ownership.assert_owned(state.state_id,envelope.ownership_token)
        self.effects.check('QFT_PORTAL_TRANSPORT',state.kind,'QFT')
        target=channel.apply(state)
        audit=audit_transition(state,target,envelope.preservation)
        if not audit['pass']: raise QuantumClosureError(str(audit['findings']))
        moved=self.ownership.move(state.state_id,envelope.ownership_token,'PORTAL:'+envelope.target_address.get('domain_id','target'))
        newown=self.ownership.claim(target,moved.owner)
        # old semantic state handle is consumed after channel result owns successor.
        self.ownership.consume(state.state_id,moved.token,'PORTAL_SUCCESSOR_CREATED')
        rec={'kind':'QUANTUM_PORTAL_CLOSURE_RECEIPT','status':'CLOSED','quantum_portal_id':digest({'source':state.state_id,'target':target.state_id,'channel':channel.channel_id,'src':envelope.source_address,'dst':envelope.target_address}),'source_state_id':state.state_id,'target_state_id':target.state_id,'channel_id':channel.channel_id,'channel_class':channel.channel_class,'source_address':envelope.source_address,'target_address':envelope.target_address,'source_instance_id':state.source_instance_id,'canonical_mmo_id':state.canonical_mmo_id,'preservation':asdict(envelope.preservation),'audit':audit,'ordinary_portal_receipt_id':(ordinary_portal_receipt or {}).get('portal_id'),'target_ownership_token':newown.token,'entanglement_relation_ids':list(envelope.entanglement_relation_ids),'physics_status':'SOFTWARE_REFERENCE_QUANTUM_INFORMATION_TRANSPORT','timestamp_ns':now_ns()}
        if self.ledger:self.ledger.append(rec)
        return target,newown,rec
