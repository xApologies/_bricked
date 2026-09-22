from .model import Effect,StateKind
from .errors import EffectViolation,QuantumSectorViolation

EFFECT_RULES={
 Effect.SUPERPOSE.value: {'sector':'QFT','inputs':{'CLASSICAL','PURE'},'output':'PURE','consumes':False,'coherence':'CREATE'},
 Effect.ENTANGLE.value: {'sector':'QFT','inputs':{'PURE','JOINT'},'output':'JOINT','consumes':True,'coherence':'PRESERVE_OR_CREATE'},
 Effect.UNITARY.value: {'sector':'QFT','inputs':{'PURE','JOINT'},'output':'PURE_OR_JOINT','consumes':False,'coherence':'PRESERVE'},
 Effect.CHANNEL.value: {'sector':'QFT','inputs':{'PURE','JOINT','DENSITY','DECOHERED'},'output':'DENSITY_OR_PURE','consumes':False,'coherence':'DECLARED'},
 Effect.DEPHASE.value: {'sector':'QFT','inputs':{'PURE','JOINT','DENSITY'},'output':'DECOHERED','consumes':False,'coherence':'MAY_REDUCE'},
 Effect.MEASURE.value: {'sector':'QFT','inputs':{'PURE','JOINT'},'output':'MEASURED','consumes':True,'coherence':'DESTROY_ALLOWED'},
 Effect.QFT_PORTAL_TRANSPORT.value: {'sector':'QFT','inputs':{'PURE','JOINT','DENSITY','DECOHERED'},'output':'DECLARED_BY_CHANNEL','consumes':False,'coherence':'DECLARED'},
 Effect.STRUCTURAL_TRANSDUCE.value: {'sector':'ANY','inputs':{'ANY'},'output':'STRUCTURAL_VIEW','consumes':False,'coherence':'NOT_CLAIMED'},
}

class EffectChecker:
    def check(self,effect,state_kind,sector):
        e=effect.value if hasattr(effect,'value') else str(effect); r=EFFECT_RULES.get(e)
        if not r: return {'admitted':True,'effect':e,'rule':'UNSPECIALIZED'}
        if r['sector']!='ANY' and sector!=r['sector']: raise QuantumSectorViolation(f'{e} requires {r["sector"]}')
        if 'ANY' not in r['inputs'] and state_kind not in r['inputs']: raise EffectViolation(f'{e} rejects {state_kind}')
        return {'admitted':True,'effect':e,'rule':r}
