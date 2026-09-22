from collections import defaultdict
from .effects import effects, QUANTUM_OPS, PORTAL_ROAD_OPS, BRIDGE_OPS, PROVENANCE_OPS
from .util import sha256_obj
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm.graph import schedule_gir

def analyze_gir(gir):
    nodes=list(gir.get('nodes',[])); byid={n['id']:n for n in nodes}; producers={}
    consumers=defaultdict(list)
    for n in nodes:
        if n.get('out'): producers[n['out']]=n['id']
    for n in nodes:
        for a in n.get('args',[]):
            if isinstance(a,str) and a.startswith('%'):
                consumers[a].append(n['id'])
    scheduled=schedule_gir(gir)
    effectful=[n['id'] for n in scheduled if effects(n['op'])]
    return {
      'gir_hash':sha256_obj(gir),'nodes':len(nodes),'edges':len(gir.get('edges',[])),
      'producers':producers,'consumers':{k:sorted(v) for k,v in consumers.items()},
      'exports':list(gir.get('exports',[])),
      'schedule':[n['id'] for n in scheduled],
      'effectful_order':effectful,
      'quantum_order':[n['id'] for n in scheduled if n['op'] in QUANTUM_OPS],
      'portal_road_order':[n['id'] for n in scheduled if n['op'] in PORTAL_ROAD_OPS],
      'bridge_order':[n['id'] for n in scheduled if n['op'] in BRIDGE_OPS],
      'provenance_order':[n['id'] for n in scheduled if n['op'] in PROVENANCE_OPS],
    }
