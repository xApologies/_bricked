from dataclasses import dataclass
import struct

@dataclass(frozen=True, order=True)
class FabricAddress:
    fabric_tag: int
    page: int
    cell: int
    lane: int = 0
    flags: int = 0

    def __post_init__(self):
        if not (0 <= self.fabric_tag < 2**64): raise ValueError('fabric_tag')
        if not (0 <= self.page < 2**32): raise ValueError('page')
        if not (0 <= self.cell < 2**16): raise ValueError('cell')
        if not (0 <= self.lane < 2**8): raise ValueError('lane')
        if not (0 <= self.flags < 2**8): raise ValueError('flags')

    def pack(self) -> bytes:
        return struct.pack('>QIHBB', self.fabric_tag, self.page, self.cell, self.lane, self.flags)

    @classmethod
    def unpack(cls, b: bytes):
        if len(b) != 16: raise ValueError('FabricAddress requires 16 bytes')
        return cls(*struct.unpack('>QIHBB', b))

    def as_int(self) -> int:
        return int.from_bytes(self.pack(), 'big')
