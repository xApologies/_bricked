from dataclasses import asdict
class QuantumEffectBraneAdapter:
    def adapt(self,instance,state,receipts):
        base=dict(instance.get('brane_m5') or {})
        base.setdefault('I',{}).update({'quantum_state_id':state.state_id,'canonical_mmo_id':state.canonical_mmo_id})
        base.setdefault('D',{}).update({'quantum_receipt_ids':[r.get('quantum_portal_id') or r.get('measurement_id') for r in receipts if isinstance(r,dict)]})
        base.setdefault('Chi',{}).update({'quantum_sector':'QFT','state_kind':state.kind})
        base.setdefault('R',{}).update({'quantum_effect_count':len(receipts),'quantum_state_members':list(state.members)})
        base.setdefault('P',{}).update({'quantum_effect_receipts':receipts})
        return base
