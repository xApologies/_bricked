from copy import deepcopy
from .effects import pure
from .util import canonical_obj
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm.util import sha256_obj as vm_sha256_obj

def canonicalize(g):
    x=deepcopy(g)
    x['nodes']=[canonical_obj(n) for n in sorted(x.get('nodes',[]),key=lambda n:n['id'])]
    x['edges']=[canonical_obj(e) for e in sorted(x.get('edges',[]),key=lambda e:(e.get('from',''),e.get('to',''),e.get('kind','')))]
    return x, {'changed': x!=g}

def dedupe_edges(g):
    x=deepcopy(g); seen=set(); out=[]; removed=[]
    for e in x.get('edges',[]):
        key=(e.get('from'),e.get('to'),e.get('kind','dependency'))
        if key in seen: removed.append(key); continue
        seen.add(key); out.append(e)
    x['edges']=out
    return x, {'changed':bool(removed),'removed':removed}

def fold_const_hash(g):
    x=deepcopy(g); byout={n.get('out'):n for n in x.get('nodes',[]) if n.get('out')}; folded=[]
    for n in x.get('nodes',[]):
        if n.get('op')!='HASH' or len(n.get('args',[]))!=1: continue
        p=byout.get(n['args'][0])
        if not p or p.get('op')!='CONST': continue
        val=p.get('attrs',{}).get('value')
        n['op']='CONST'; n['args']=[]; n['attrs']={'value':vm_sha256_obj(val),'folded_from':'HASH','source_const':p['id']}; n['type']='HASH'
        folded.append(n['id'])
    return x, {'changed':bool(folded),'folded':folded}

def _resolve_alias(v,aliases):
    seen=set()
    while isinstance(v,str) and v in aliases and v not in seen:
        seen.add(v); v=aliases[v]
    return v

def coalesce_alias_moves(g):
    x=deepcopy(g); aliases={}; removed=[]
    # only explicit alias-only moves; QSTATE moves are forbidden.
    for n in x.get('nodes',[]):
        if n.get('op')=='MOVE' and n.get('attrs',{}).get('alias_only') is True and len(n.get('args',[]))==1 and n.get('type')!='QSTATE':
            aliases[n.get('out')]=n['args'][0]; removed.append(n['id'])
    if not aliases: return x, {'changed':False,'removed':[]}
    for n in x.get('nodes',[]):
        if n['id'] in removed: continue
        n['args']=[_resolve_alias(a,aliases) for a in n.get('args',[])]
        attrs=dict(n.get('attrs',{}))
        for k,v in list(attrs.items()):
            if isinstance(v,str) and v.startswith('%'): attrs[k]=_resolve_alias(v,aliases)
        n['attrs']=attrs
    x['exports']=[_resolve_alias(e,aliases) for e in x.get('exports',[])]
    x['nodes']=[n for n in x.get('nodes',[]) if n['id'] not in removed]
    x=_bypass_removed_edges(x,set(removed))
    return x, {'changed':True,'removed':removed,'aliases':aliases}

def _bypass_removed_edges(g,removed):
    x=deepcopy(g); edges=x.get('edges',[]); incoming={r:[] for r in removed}; outgoing={r:[] for r in removed}; keep=[]
    for e in edges:
        a,b=e.get('from'),e.get('to')
        if b in removed: incoming[b].append(e)
        if a in removed: outgoing[a].append(e)
        if a not in removed and b not in removed: keep.append(e)
    # Conservative local bypass for effect_order/dependency edges.
    for r in removed:
        for i in incoming.get(r,[]):
            for o in outgoing.get(r,[]):
                if i.get('kind')==o.get('kind') and i.get('kind') in ('effect_order','dependency'):
                    keep.append({'from':i['from'],'to':o['to'],'kind':i.get('kind')})
    x['edges']=keep
    return x

def dead_pure_elimination(g):
    x=deepcopy(g); nodes=x.get('nodes',[]); producers={n.get('out'):n for n in nodes if n.get('out')}
    live_nodes=set(); work=[]
    for n in nodes:
        if not pure(n.get('op')):
            live_nodes.add(n['id']); work.append(n)
    for e in x.get('exports',[]):
        p=producers.get(e)
        if p and p['id'] not in live_nodes: live_nodes.add(p['id']); work.append(p)
    while work:
        n=work.pop()
        for a in n.get('args',[]):
            p=producers.get(a)
            if p and p['id'] not in live_nodes:
                live_nodes.add(p['id']); work.append(p)
    removed=[n['id'] for n in nodes if n['id'] not in live_nodes]
    if not removed: return x, {'changed':False,'removed':[]}
    x['nodes']=[n for n in nodes if n['id'] in live_nodes]
    x=_bypass_removed_edges(x,set(removed))
    return x, {'changed':True,'removed':removed}
