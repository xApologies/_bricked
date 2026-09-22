import hashlib
from .delta import TransformationDeltaSegment
from vendor.genesis_geometric_engine.segment import GeometricOverlaySegment

def open_segment(path,verify=True):
    p=str(path)
    if p.endswith('.gtd'): return TransformationDeltaSegment(path,verify=verify)
    return GeometricOverlaySegment(path,verify=verify)

class TransformView:
    def __init__(self,fabric,segment_paths,staged=None):
        self.fabric=fabric; self.segments=[open_segment(p) for p in segment_paths]; self.staged=staged if staged is not None else {}
    def close(self):
        for s in self.segments: s.close()
    def read_index(self,idx):
        if idx in self.staged: return self.staged[idx]
        for s in reversed(self.segments):
            c=s.read_index(idx)
            if c is not None:return c
        return self.fabric.read(self.fabric.address_for_index(idx))
    def state_root(self,start,count):
        h=hashlib.sha256()
        for idx in range(int(start),int(start)+int(count)):
            h.update(int(idx).to_bytes(8,'big')); h.update(self.read_index(idx).pack())
        return h.hexdigest()
