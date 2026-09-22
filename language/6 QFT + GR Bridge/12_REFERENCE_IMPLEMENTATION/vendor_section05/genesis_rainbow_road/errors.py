class RainbowRoadError(Exception): pass
class EmptyRoadError(RainbowRoadError): pass
class RoadCompositionError(RainbowRoadError): pass
class RoadSectorMismatch(RainbowRoadError): pass
class RoadRouteDrift(RainbowRoadError): pass
class RoadCapacityError(RainbowRoadError): pass
class RoadClosureError(RainbowRoadError): pass
class RoadExecutionError(RainbowRoadError):
    def __init__(self,message,receipt=None):
        super().__init__(message); self.receipt=receipt
