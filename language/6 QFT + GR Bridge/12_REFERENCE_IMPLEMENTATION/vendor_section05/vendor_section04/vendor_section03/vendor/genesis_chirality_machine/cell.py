from dataclasses import dataclass
import struct
from .constants import RIGHT_PATTERN, LEFT_PATTERN, CELL_SIZE

_FMT = '<BBbBHHHHHHIIQ'
assert struct.calcsize(_FMT) == CELL_SIZE

def q16(x: float) -> int:
    if x < 0 or x > 1: raise ValueError('Q0.16 value must be in [0,1]')
    return min(65535, round(x * 65535))

def uq16(v: int) -> float:
    return v / 65535.0

@dataclass(frozen=True)
class ChiralityCell:
    occupancy_pattern: int = 0
    complement_pattern: int = 0
    handedness: int = 0
    state_class: int = 0
    sigma: int = 0
    chi: int = 0
    rho: int = 0
    lambda_: int = 0
    tau: int = 0
    flags: int = 0
    adjacency_index: int = 0
    lineage_index: int = 0
    identity_tag: int = 0

    def pack(self) -> bytes:
        return struct.pack(_FMT, self.occupancy_pattern, self.complement_pattern,
                           self.handedness, self.state_class, self.sigma, self.chi,
                           self.rho, self.lambda_, self.tau, self.flags,
                           self.adjacency_index, self.lineage_index, self.identity_tag)

    @classmethod
    def unpack(cls, b: bytes):
        if len(b) != CELL_SIZE: raise ValueError('cell size')
        return cls(*struct.unpack(_FMT, b))

    @property
    def occupancy_3d(self):
        # serialization convention only: bit 7..0 -> z,y,x lexical positions
        bits=[(self.occupancy_pattern >> (7-i)) & 1 for i in range(8)]
        return (((bits[0],bits[1]),(bits[2],bits[3])),
                ((bits[4],bits[5]),(bits[6],bits[7])))

    def mirror(self):
        return ChiralityCell(
            occupancy_pattern=self.complement_pattern,
            complement_pattern=self.occupancy_pattern,
            handedness=-self.handedness,
            state_class=self.state_class,
            sigma=self.sigma, chi=self.chi, rho=self.rho,
            lambda_=self.lambda_, tau=self.tau, flags=self.flags,
            adjacency_index=self.adjacency_index,
            lineage_index=self.lineage_index,
            identity_tag=self.identity_tag)

    @classmethod
    def right(cls, **kw):
        return cls(occupancy_pattern=RIGHT_PATTERN, complement_pattern=LEFT_PATTERN, handedness=1, **kw)

    @classmethod
    def left(cls, **kw):
        return cls(occupancy_pattern=LEFT_PATTERN, complement_pattern=RIGHT_PATTERN, handedness=-1, **kw)
