class SectorBridgeError(Exception): pass
class UnsupportedSectorPair(SectorBridgeError): pass
class CommonAncestryMismatch(SectorBridgeError): pass
class BridgeContentDrift(SectorBridgeError): pass
class BridgeResidueDrift(SectorBridgeError): pass
class BridgeSourceMutated(SectorBridgeError): pass
class BridgeFabricMutated(SectorBridgeError): pass
class InverseRequired(SectorBridgeError): pass
class MixedRoadError(SectorBridgeError):
    def __init__(self,msg,receipt=None): super().__init__(msg); self.receipt=receipt
class MixedRoadPreflightError(MixedRoadError): pass
class MixedRoadExecutionError(MixedRoadError): pass
