class GCMError(Exception): pass
class FabricIntegrityError(GCMError): pass
class FabricReadOnlyError(GCMError): pass
class InvalidAddressError(GCMError): pass
class CodecError(GCMError): pass
class AdmissionError(GCMError): pass
class ClosureError(GCMError): pass
