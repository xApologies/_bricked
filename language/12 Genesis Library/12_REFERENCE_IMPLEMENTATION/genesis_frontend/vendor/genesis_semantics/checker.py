from collections import defaultdict
from .model import Diagnostic, CheckResult, TypeExpr
from .typesys import parse_type, compatible, sector_of
from .effects import effects_for_op, OP_EFFECTS

class State:
    def __init__(self,seed=None,module=None):
        self.types=dict(seed or {})
        self.module=module
        self.diags=[]; self.effects=set(); self.bridges=[]; self.portal={}; self.road={}; self.q_live={}
        self.producers={}
    def err(self,code,msg,node=None): self.diags.append(Diagnostic(code,msg,node,self.module))

def _schedule(gir,seed_values):
    nodes=gir.get('nodes',[]); by={}; prod={}; deps={}; rev=defaultdict(set)
    for n in nodes:
        nid=n.get('id')
        if not nid: raise ValueError('node missing id')
        if nid in by: raise ValueError(f'duplicate node {nid}')
        by[nid]=n; deps[nid]=set()
        out=n.get('out')
        if out:
            if out in prod: raise ValueError(f'duplicate output {out}')
            prod[out]=nid
    for n in nodes:
        nid=n['id']
        for a in n.get('args',[]):
            if isinstance(a,str) and a.startswith('%'):
                if a in prod:
                    p=prod[a]
                    if p!=nid: deps[nid].add(p); rev[p].add(nid)
                elif a not in seed_values:
                    raise KeyError(f'unknown value {a} in {nid}')
    for e in gir.get('edges',[]):
        if e.get('kind','dependency') in ('dependency','effect_order'):
            a=e.get('from'); b=e.get('to')
            if a not in by or b not in by: raise KeyError(f'unknown edge {a}->{b}')
            deps[b].add(a); rev[a].add(b)
    ready=sorted([x for x,d in deps.items() if not d]); out=[]; done=set()
    while ready:
        x=ready.pop(0); out.append(by[x]); done.add(x)
        for y in sorted(rev[x]):
            deps[y].discard(x)
            if not deps[y] and y not in done and y not in ready:
                ready.append(y); ready.sort()
    if len(out)!=len(nodes): raise ValueError('dependency cycle: '+','.join(sorted(set(by)-done)))
    return out

def _arg(st,n,i,required=None):
    args=n.get('args',[])
    if i>=len(args): st.err('ARITY_MISMATCH',f"{n['op']} missing argument {i}",n['id']); return TypeExpr('ANY'),None
    a=args[i]
    if not (isinstance(a,str) and a.startswith('%')): return TypeExpr('ANY'),a
    if a not in st.types: st.err('UNKNOWN_VALUE',f'unknown value {a}',n['id']); return TypeExpr('ANY'),a
    t=st.types[a]
    if required and not compatible(required,t): st.err('TYPE_MISMATCH',f'{n["op"]} arg {i} requires {required}, got {t}',n['id'])
    return t,a

def _portal_state(st,val,node):
    if val is None: return
    if st.portal.get(val)!='OPEN': st.err('PORTAL_NOT_OPEN',f'portal {val} is not OPEN',node)

def _road_state(st,val,node):
    if val is None:return
    if st.road.get(val)!='OPEN': st.err('ROAD_NOT_OPEN',f'road {val} is not OPEN',node)

def _consume_q(st,val,node):
    if val is None:return
    if not st.q_live.get(val,False): st.err('LINEAR_USE_AFTER_MOVE',f'QSTATE {val} is not live/owned',node)
    else: st.q_live[val]=False

def _infer(st,n):
    op=n.get('op'); attrs=n.get('attrs',{}); nid=n['id']
    st.effects |= effects_for_op(op)
    if op not in OP_EFFECTS: st.err('UNKNOWN_OPCODE',f'unknown operation {op}',nid); return TypeExpr('ANY')
    if op=='NOP': return TypeExpr('VOID')
    if op=='CONST': return TypeExpr('ANY')
    if op=='MOVE':
        t,v=_arg(st,n,0)
        if t.kind=='QSTATE': st.err('QSTATE_GENERIC_MOVE','generic MOVE cannot copy/move QSTATE',nid)
        return t
    if op=='HASH': _arg(st,n,0); return TypeExpr('HASH')
    if op=='FABRIC_MOUNT': return TypeExpr('FABRIC')
    if op=='FABRIC_ALLOC': _arg(st,n,0,'FABRIC'); return TypeExpr('REGION')
    if op=='FABRIC_READ': _arg(st,n,0,'FABRIC'); return TypeExpr('ANY')
    if op=='FABRIC_WRITE_OVERLAY': _arg(st,n,0,'FABRIC'); return TypeExpr('RECEIPT',('OVERLAY_WRITE',))
    if op=='GEO_INSTANTIATE':
        _arg(st,n,0,'FABRIC'); _arg(st,n,1,'REGION'); return TypeExpr('GEOMETRIC',('CLOSED','UNBOUND'))
    if op=='GEO_FORK':
        t,_=_arg(st,n,0,'GEOMETRIC'); return TypeExpr('GEOMETRIC',('CLOSED',sector_of(t) or 'UNBOUND'))
    if op=='RELATE': _arg(st,n,0,'GEOMETRIC'); return TypeExpr('RELATION')
    if op=='ADMIT': _arg(st,n,0,'GEOMETRIC'); return TypeExpr('ADMISSION')
    if op=='TRANSFORM':
        t,_=_arg(st,n,0,'GEOMETRIC'); _arg(st,n,1,'ADMISSION'); return TypeExpr('GEOMETRIC',('CLOSED',sector_of(t) or 'UNBOUND'))
    if op=='INHERIT': _arg(st,n,0); return TypeExpr('RECEIPT',('INHERIT',))
    if op=='PORTAL_OPEN':
        gt,gv=_arg(st,n,0,'GEOMETRIC'); _arg(st,n,1,'ADMISSION')
        sec=str(attrs.get('sector','GENERIC')).upper(); gsec=sector_of(gt)
        if gsec and gsec not in ('UNBOUND','GENERIC',sec):
            ok=any(b['geo']==gv and b['from']==gsec and b['to']==sec for b in st.bridges)
            if not ok: st.err('BRIDGE_REQUIRED',f'{gsec}->{sec} requires explicit BRIDGE_SECTOR for {gv}',nid)
        out=TypeExpr('PORTAL',(sec,'OPEN'))
        return out
    if op=='PORTAL_TRANSPORT':
        pt,pv=_arg(st,n,0,'PORTAL'); _portal_state(st,pv,nid); _arg(st,n,1,'GEOMETRIC')
        sec=sector_of(pt) or 'GENERIC'; return TypeExpr('GEOMETRIC',('CLOSED',sec))
    if op=='PORTAL_CLOSE':
        pt,pv=_arg(st,n,0,'PORTAL'); _portal_state(st,pv,nid); gt,_=_arg(st,n,1,'GEOMETRIC')
        psec=sector_of(pt); gsec=sector_of(gt)
        if psec and gsec and gsec not in ('UNBOUND','GENERIC',psec): st.err('SECTOR_MISMATCH',f'portal {psec} cannot close on {gsec} destination',nid)
        if pv is not None: st.portal[pv]='CLOSED'
        return TypeExpr('RECEIPT',('PORTAL_CLOSE',))
    if op=='ROAD_BEGIN': _arg(st,n,0,'GEOMETRIC'); return TypeExpr('ROAD',('OPEN',))
    if op=='ROAD_APPEND':
        _,rv=_arg(st,n,0,'ROAD'); _road_state(st,rv,nid); _arg(st,n,1,'RECEIPT')
        if rv is not None: st.road[rv]='MOVED'
        return TypeExpr('ROAD',('OPEN',))
    if op=='ROAD_CLOSE':
        _,rv=_arg(st,n,0,'ROAD'); _road_state(st,rv,nid); _arg(st,n,1,'GEOMETRIC')
        if rv is not None: st.road[rv]='CLOSED'
        return TypeExpr('RECEIPT',('ROAD_CLOSE',))
    if op=='BRIDGE_SECTOR':
        gt,gv=_arg(st,n,0,'GEOMETRIC'); fs=str(attrs.get('from','')).upper(); ts=str(attrs.get('to','')).upper()
        if not fs or not ts or fs==ts: st.err('BRIDGE_MISMATCH','Bridge requires distinct from/to sectors',nid)
        gsec=sector_of(gt)
        if gsec and gsec not in ('UNBOUND','GENERIC',fs): st.err('BRIDGE_MISMATCH',f'Bridge from {fs} does not match Geometric sector {gsec}',nid)
        st.bridges.append({'geo':gv,'from':fs,'to':ts,'node':nid})
        return TypeExpr('BRIDGE',(fs,ts))
    if op=='Q_PREPARE': _arg(st,n,0,'GEOMETRIC'); return TypeExpr('QSTATE',('OWNED',))
    if op in ('Q_SUPERPOSE','Q_CHANNEL'):
        _,q=_arg(st,n,0,'QSTATE'); _consume_q(st,q,nid); return TypeExpr('QSTATE',('OWNED',))
    if op=='Q_ENTANGLE':
        _,q1=_arg(st,n,0,'QSTATE'); _,q2=_arg(st,n,1,'QSTATE');
        if q1==q2 and q1 is not None: st.err('LINEAR_ALIAS',f'Q_ENTANGLE cannot consume same QSTATE twice: {q1}',nid)
        _consume_q(st,q1,nid); _consume_q(st,q2,nid); return TypeExpr('QSTATE',('OWNED',))
    if op=='Q_MEASURE':
        _,q=_arg(st,n,0,'QSTATE'); _consume_q(st,q,nid); return TypeExpr('QRESULT',('CLASSICAL',))
    if op=='BRANE_LIFT': _arg(st,n,0,'GEOMETRIC'); return TypeExpr('M5')
    if op=='PROVENANCE_SEAL': _arg(st,n,0); return TypeExpr('RECEIPT',('PROVENANCE',))
    if op=='ASSERT_CLOSURE': _arg(st,n,0); return TypeExpr('BOOL')
    if op=='EMIT_RECEIPT': return TypeExpr('RECEIPT',('EXECUTION',))
    if op in ('JUMP','CALL','RETURN','HALT'): return TypeExpr('VOID')
    if op=='BRANCH': _arg(st,n,0,'BOOL'); return TypeExpr('VOID')
    return TypeExpr('ANY')

def check_gir(gir,seed_types=None,module=None,effect_budget=None,export_values=None):
    seed={k:parse_type(v) for k,v in (seed_types or {}).items()}; st=State(seed,module)
    try: ordered=_schedule(gir,set(seed))
    except KeyError as e: st.err('UNKNOWN_VALUE',str(e)); return CheckResult(False,st.diags,st.types,st.effects,{})
    except ValueError as e:
        msg=str(e); code='NODE_DUPLICATE' if 'duplicate' in msg else 'DEPENDENCY_CYCLE'; st.err(code,msg); return CheckResult(False,st.diags,st.types,st.effects,{})
    for n in ordered:
        inferred=_infer(st,n); out=n.get('out')
        declared=n.get('type')
        if declared:
            try:
                if not compatible(parse_type(declared),inferred): st.err('TYPE_MISMATCH',f'declared {declared}, inferred {inferred}',n['id'])
            except ValueError as e: st.err('TYPE_SYNTAX',str(e),n['id'])
        if out:
            if out in st.types: st.err('VALUE_REDEFINITION',f'value {out} already defined',n['id'])
            st.types[out]=inferred
            if inferred.kind=='PORTAL': st.portal[out]='OPEN'
            if inferred.kind=='ROAD': st.road[out]='OPEN'
            if inferred.kind=='QSTATE': st.q_live[out]=True
            st.producers[out]=n['id']
    if effect_budget is not None:
        allowed=set(effect_budget); extra=st.effects-allowed
        if extra: st.err('EFFECT_BUDGET_EXCEEDED','undeclared effects: '+','.join(sorted(extra)))
    leakedp=sorted(k for k,v in st.portal.items() if v=='OPEN')
    leakedr=sorted(k for k,v in st.road.items() if v=='OPEN')
    if leakedp: st.err('PORTAL_UNCLOSED','open Portals at boundary: '+','.join(leakedp))
    if leakedr: st.err('ROAD_UNCLOSED','open Roads at boundary: '+','.join(leakedr))
    liveq=sorted(k for k,v in st.q_live.items() if v)
    exports=set(export_values or [])
    leakedq=[q for q in liveq if q not in exports]
    if leakedq: st.err('QSTATE_LEAK','owned QSTATE not consumed or exported: '+','.join(leakedq))
    witnesses={'checked_nodes':len(ordered),'bridge_witnesses':list(st.bridges),'open_portals':leakedp,'open_roads':leakedr,'live_qstate_exports':sorted(set(liveq)&exports)}
    return CheckResult(not any(d.severity=='ERROR' for d in st.diags),st.diags,st.types,st.effects,witnesses)

def check_module(mod,import_types=None):
    if mod.get('ir')!='GIR-MODULE':
        return CheckResult(False,[Diagnostic('MODULE_FORMAT','not GIR-MODULE',module=mod.get('module'))],{},set(),{})
    seeds={}
    for imp in mod.get('imports',[]): seeds[imp['local']]=imp.get('type','ANY')
    if import_types:
        for k,v in import_types.items(): seeds[k]=v
    exports=[e['value'] for e in mod.get('exports',[])]
    return check_gir(mod.get('gir',{}),seeds,mod.get('module'),mod.get('effects'),exports)
