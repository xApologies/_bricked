from dataclasses import replace
from .effects import Effect
from .util import clamp_u16

class Operator:
    name='OP'; effects=frozenset({Effect.READ})
    def __init__(self,spec): self.spec=spec
    def apply(self,idx,cell,ctx): return cell

class Inherit(Operator):
    name='INHERIT'; effects=frozenset({Effect.READ,Effect.LINEAGE_WRITE})

class StabilizeRho(Operator):
    name='STABILIZE_RHO'; effects=frozenset({Effect.PERSISTENCE_WRITE})
    def apply(self,idx,c,ctx): return replace(c,rho=clamp_u16(c.rho+int(self.spec.get('delta',0))))

class DestabilizeRho(Operator):
    name='DESTABILIZE_RHO'; effects=frozenset({Effect.PERSISTENCE_WRITE})
    def apply(self,idx,c,ctx): return replace(c,rho=clamp_u16(c.rho-int(self.spec.get('delta',0))))

class SetTau(Operator):
    name='SET_TAU'; effects=frozenset({Effect.TRANSLATION_WRITE})
    def apply(self,idx,c,ctx):
        v=self.spec.get('value'); d=self.spec.get('delta')
        return replace(c,tau=clamp_u16(v if v is not None else c.tau+int(d or 0)))

class SetSigma(Operator):
    name='SET_SIGMA'; effects=frozenset({Effect.ADMISSIBILITY_WRITE})
    def apply(self,idx,c,ctx):
        v=self.spec.get('value'); d=self.spec.get('delta')
        return replace(c,sigma=clamp_u16(v if v is not None else c.sigma+int(d or 0)))

class MirrorChirality(Operator):
    name='MIRROR_CHIRALITY'; effects=frozenset({Effect.CHIRALITY_WRITE,Effect.OCCUPANCY_WRITE})
    def apply(self,idx,c,ctx): return c.mirror()

class NormalizeComponents(Operator):
    name='NORMALIZE_COMPONENTS'
    def __init__(self,spec):
        super().__init__(spec); fields=spec.get('fields',['sigma','chi','rho','lambda_','tau'])
        em={'sigma':Effect.ADMISSIBILITY_WRITE,'chi':Effect.CHIRALITY_WRITE,'rho':Effect.PERSISTENCE_WRITE,'lambda_':Effect.LOCALITY_WRITE,'tau':Effect.TRANSLATION_WRITE}
        self.fields=fields; self.effects=frozenset(em[f] for f in fields)
    def apply(self,idx,c,ctx):
        target=int(self.spec.get('target',32768)); strength=float(self.spec.get('strength',0.25)); kw={}
        for f in self.fields:
            old=getattr(c,f); kw[f]=clamp_u16(round(old+(target-old)*strength))
        return replace(c,**kw)

class SetCellFields(Operator):
    name='SET_CELL_FIELDS'
    MAP={'sigma':Effect.ADMISSIBILITY_WRITE,'chi':Effect.CHIRALITY_WRITE,'rho':Effect.PERSISTENCE_WRITE,'lambda_':Effect.LOCALITY_WRITE,'tau':Effect.TRANSLATION_WRITE,'flags':Effect.FLAGS_WRITE,'adjacency_index':Effect.ADJACENCY_WRITE,'identity_tag':Effect.IDENTITY_TAG_WRITE,'occupancy_pattern':Effect.OCCUPANCY_WRITE,'complement_pattern':Effect.OCCUPANCY_WRITE,'handedness':Effect.CHIRALITY_WRITE}
    def __init__(self,spec):
        super().__init__(spec); self.fields=spec.get('fields',{}); self.effects=frozenset(self.MAP[k] for k in self.fields)
    def apply(self,idx,c,ctx):
        kw={k:(clamp_u16(v) if k in {'sigma','chi','rho','lambda_','tau'} else v) for k,v in self.fields.items()}
        return replace(c,**kw)

class RedistributeRho(Operator):
    name='REDISTRIBUTE_RHO'; effects=frozenset({Effect.PERSISTENCE_WRITE})
    # handled as group operator by engine
    group=True
    def apply_group(self,indices,get,set_):
        amount=int(self.spec.get('amount',1))
        for a,b in zip(indices[0::2],indices[1::2]):
            ca,cb=get(a),get(b); move=min(amount,ca.rho,65535-cb.rho)
            if move:
                set_(a,replace(ca,rho=ca.rho-move)); set_(b,replace(cb,rho=cb.rho+move))

OPS={c.name:c for c in [Inherit,StabilizeRho,DestabilizeRho,SetTau,SetSigma,MirrorChirality,NormalizeComponents,SetCellFields,RedistributeRho]}

def operator_from_spec(spec):
    name=spec['op'].upper()
    if name not in OPS: raise ValueError(f'unknown operator {name}')
    return OPS[name](spec)
