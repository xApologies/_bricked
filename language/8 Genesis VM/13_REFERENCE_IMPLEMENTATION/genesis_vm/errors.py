class GenesisVMError(Exception): pass
class GIRCompileError(GenesisVMError): pass
class VerifyError(GenesisVMError): pass
class BytecodeError(GenesisVMError): pass
class RuntimeFault(GenesisVMError): pass
class LinearResourceError(RuntimeFault): pass
class ClosureError(RuntimeFault): pass
class SectorError(RuntimeFault): pass
