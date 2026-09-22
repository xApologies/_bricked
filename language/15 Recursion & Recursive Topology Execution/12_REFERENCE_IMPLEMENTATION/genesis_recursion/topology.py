from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .util import sha256_obj
from .errors import RuntimeFault

@dataclass
class TopologyTraversalResult:
    visits:list[Any]; edges:list[tuple[Any,Any]]; cycles:list[dict]; closures:list[Any]; history_root:str; receipt:dict

class TopologyRecursiveExecutor:
    def walk(self,start,adjacency,cycle_policy='skip',max_depth=256):
        if cycle_policy not in ('skip','error'): raise ValueError('cycle_policy must be skip or error')
        if not 1<=max_depth<=4096: raise ValueError('max_depth out of range')
        visits=[]; edges=[]; cycles=[]; closures=[]; visited=set(); active=[]; root='0'*64
        def rec(node,depth,path):
            nonlocal root
            if depth>max_depth: raise RuntimeFault('topology recursion depth exceeded','RECURSION_DEPTH_EXCEEDED')
            if node in visited or node in active:
                witness={'node':node,'path':list(path),'active':node in active,'visited':node in visited}; cycles.append(witness); root=sha256_obj({'history':root,'cycle':witness})
                if cycle_policy=='error': raise RuntimeFault(f'topology cycle/revisit at {node!r}','TOPOLOGY_CYCLE')
                return
            visited.add(node); active.append(node); visits.append(node); root=sha256_obj({'history':root,'enter':node,'depth':depth})
            for nxt in adjacency.get(node,[]):
                edges.append((node,nxt)); root=sha256_obj({'history':root,'edge':[node,nxt]}); rec(nxt,depth+1,path+[node])
            active.pop(); closures.append(node); root=sha256_obj({'history':root,'close':node,'depth':depth})
        rec(start,0,[])
        receipt={'start':start,'cycle_policy':cycle_policy,'visits':len(visits),'edges':len(edges),'cycles':len(cycles),'closures':len(closures),'history_root':root,'status':'CLOSED'}
        receipt['receipt_id']='gtopo-'+sha256_obj(receipt)[:32]
        return TopologyTraversalResult(visits,edges,cycles,closures,root,receipt)
