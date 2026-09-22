class GenesisSemanticError(Exception): pass
class TypeCheckError(GenesisSemanticError): pass
class LinkError(GenesisSemanticError): pass
class CapabilityError(GenesisSemanticError): pass
