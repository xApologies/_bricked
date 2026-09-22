from dataclasses import dataclass, field
from .overlay import FabricOverlay
from .address import FabricAddress
from .cell import ChiralityCell
from .codec import CalibratedLevelCodec

@dataclass
class GenesisChiralityMachine:
    fabric: object
    overlay: FabricOverlay = field(default_factory=FabricOverlay)
    codec: CalibratedLevelCodec = field(default_factory=CalibratedLevelCodec)
    G: list = field(default_factory=lambda:[None]*16)
    A: list = field(default_factory=lambda:[None]*16)
    C: list = field(default_factory=lambda:[None]*8)
    R: list = field(default_factory=lambda:[None]*8)
    P: list = field(default_factory=lambda:[None]*8)
    status: dict = field(default_factory=dict)

    def read(self, address):
        return self.overlay.read(address, self.fabric.read)

    def stage(self, address, cell):
        self.fabric.cell_index(address) # validate
        self.overlay.stage(address, cell)

    def commit(self, reason='gcm_commit'):
        return self.overlay.commit(reason)

    def geometric_region(self, start_index, count):
        if start_index < 0 or count < 0 or start_index+count > self.fabric.cell_count: raise ValueError('region')
        return {'fabric_tag':self.fabric.fabric_tag, 'start_index':start_index, 'count':count}

    def mount_receipt(self):
        return {'kind':'FABRIC_MOUNT_RECEIPT','fabric_tag':self.fabric.fabric_tag,
                'cell_count':self.fabric.cell_count,'data_hash':self.fabric.data_hash.hex(),
                'overlay_root':self.overlay.root_hash()}
