class GeometricError(Exception): pass
class SourceFormatError(GeometricError): pass
class AllocationError(GeometricError): pass
class InstantiationError(GeometricError): pass
class SegmentIntegrityError(GeometricError): pass
class StateTransitionError(GeometricError): pass
