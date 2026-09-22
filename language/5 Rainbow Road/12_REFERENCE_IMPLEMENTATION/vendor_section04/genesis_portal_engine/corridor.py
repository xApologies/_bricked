from collections import defaultdict
from dataclasses import asdict
from .model import CorridorPath
from .util import digest_obj
from .errors import NoCorridorError

class CorridorGraph:
    def __init__(self,edges=None):
        self.edges={}; self.out=defaultdict(list)
        for e in edges or []: self.add_edge(e)
    def add_edge(self,e): self.edges[e.edge_id]=e; self.out[e.source_domain].append(e.edge_id)
    def _edge_ok(self,e,req,available):
        if req.sector not in e.sectors: return False
        if req.chirality_class!='ANY' and 'ANY' not in e.chirality_classes and req.chirality_class not in e.chirality_classes: return False
        if req.residue_class!='ANY' and 'ANY' not in e.residue_classes and req.residue_class not in e.residue_classes: return False
        if e.resolution+1e-12 < req.resolution_required: return False
        if e.bandwidth+1e-12 < req.bandwidth_required: return False
        if available(e.edge_id) < req.capacity_units_required: return False
        if req.closure_target=='TARGET_ADDRESS' and not e.closure_supported and e.target_domain==req.target_address.domain_id: return False
        return True
    def candidate_paths(self,req,available,max_hops=16):
        src=req.source_address.domain_id; dst=req.target_address.domain_id; paths=[]
        stack=[(src,[],[src])]
        while stack:
            dom,eids,domains=stack.pop()
            if len(eids)>max_hops: continue
            if dom==dst and eids:
                es=[self.edges[x] for x in eids]
                paths.append((eids,domains,es)); continue
            for eid in sorted(self.out.get(dom,[]),reverse=True):
                e=self.edges[eid]
                if e.target_domain in domains: continue
                if self._edge_ok(e,req,available): stack.append((e.target_domain,eids+[eid],domains+[e.target_domain]))
        return paths
    def select(self,req,available):
        ps=self.candidate_paths(req,available)
        if not ps: raise NoCorridorError(f'no admissible corridor {req.source_address.domain_id}->{req.target_address.domain_id}')
        ranked=[]
        for eids,domains,es in ps:
            total=sum(e.cost for e in es); mr=min(e.resolution for e in es); mb=min(e.bandwidth for e in es)
            ch=[req.chirality_class]+[req.chirality_class for _ in es]; colors=[e.color_index for e in es]
            pid=digest_obj({'edges':eids,'domains':domains,'sector':req.sector})[:24]
            cp=CorridorPath(pid,domains,eids,total,mr,mb,ch,colors,req.sector)
            ranked.append((total,len(eids),-mb,pid,cp))
        ranked.sort(key=lambda x:x[:4]); return ranked[0][-1]
