from .segment import GeometricOverlaySegment
class GeometricView:
    def __init__(self,fabric,segments): self.fabric=fabric; self.segments=list(segments)
    def read_index(self,idx):
        for seg in reversed(self.segments):
            c=seg.read_index(idx)
            if c is not None: return c
        return self.fabric.read(self.fabric.address_for_index(idx))
