from .image import FabricImage
from .machine import GenesisChiralityMachine

def boot(path, verify=True):
    fabric=FabricImage(path, verify=verify)
    machine=GenesisChiralityMachine(fabric)
    return machine, machine.mount_receipt()
