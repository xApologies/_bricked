from abc import ABC, abstractmethod

class FabricBackend(ABC):
    @abstractmethod
    def mount(self): ...
    @abstractmethod
    def read_cell(self, address): ...
    @abstractmethod
    def fabric_identity(self): ...

class BlockDeviceBackend(FabricBackend):
    """Design stub. Commodity block devices expose logical sectors through a controller."""
    def __init__(self, device_path, readonly=True):
        self.device_path=device_path; self.readonly=readonly
    def mount(self): raise NotImplementedError('requires device-specific implementation')
    def read_cell(self, address): raise NotImplementedError
    def fabric_identity(self): raise NotImplementedError

class FPGARegisterBackend(FabricBackend):
    """Design stub for ROM/BRAM/register mapped hardware."""
    def __init__(self, descriptor): self.descriptor=descriptor
    def mount(self): raise NotImplementedError
    def read_cell(self, address): raise NotImplementedError
    def fabric_identity(self): raise NotImplementedError
