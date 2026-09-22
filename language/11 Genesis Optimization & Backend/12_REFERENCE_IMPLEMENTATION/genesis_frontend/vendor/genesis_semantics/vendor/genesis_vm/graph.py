from collections import defaultdict
from .errors import GIRCompileError

def schedule_gir(gir):
    nodes = gir.get('nodes', [])
    by_id = {}
    producers = {}
    for n in nodes:
        nid=n['id']
        if nid in by_id: raise GIRCompileError(f'duplicate node id {nid}')
        by_id[nid]=n
        out=n.get('out')
        if out:
            if out in producers: raise GIRCompileError(f'duplicate value producer {out}')
            producers[out]=nid
    deps={nid:set() for nid in by_id}
    rev=defaultdict(set)
    for n in nodes:
        nid=n['id']
        for arg in n.get('args',[]):
            if isinstance(arg,str) and arg.startswith('%'):
                if arg not in producers: raise GIRCompileError(f'unknown value {arg} in {nid}')
                p=producers[arg]
                if p!=nid: deps[nid].add(p); rev[p].add(nid)
    for e in gir.get('edges',[]):
        if e.get('kind','dependency') in ('dependency','effect_order'):
            a=e['from']; b=e['to']
            if a not in by_id or b not in by_id: raise GIRCompileError(f'unknown edge {a}->{b}')
            deps[b].add(a); rev[a].add(b)
    ready=sorted([n for n,d in deps.items() if not d])
    out=[]
    while ready:
        nid=ready.pop(0); out.append(by_id[nid])
        for m in sorted(rev[nid]):
            deps[m].discard(nid)
            if not deps[m] and m not in [x['id'] for x in out] and m not in ready:
                ready.append(m); ready.sort()
    if len(out)!=len(nodes):
        remain=sorted(set(by_id)-{x['id'] for x in out})
        raise GIRCompileError(f'dependency cycle: {remain}')
    return out
