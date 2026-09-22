from pathlib import Path
import hashlib, mmap, os, struct
from .constants import MAGIC, FORMAT_VERSION, SUPERBLOCK_SIZE, CELL_SIZE, PAGE_SIZE, CELLS_PER_PAGE
from .cell import ChiralityCell
from .address import FabricAddress
from .errors import FabricIntegrityError, InvalidAddressError

_HDR_FMT = '<8sIIIIQQ32s32s'
_HDR_SIZE = struct.calcsize(_HDR_FMT)

class FabricImageBuilder:
    @staticmethod
    def build(path, cells, source_manifest_hash=b'\x00'*32):
        path=Path(path)
        payload=b''.join(c.pack() for c in cells)
        data_hash=hashlib.sha256(payload).digest()
        fabric_tag=int.from_bytes(data_hash[:8], 'big')
        header=struct.pack(_HDR_FMT, MAGIC, FORMAT_VERSION, CELL_SIZE, PAGE_SIZE, 0,
                           len(cells), fabric_tag, source_manifest_hash, data_hash)
        if len(header) > SUPERBLOCK_SIZE: raise RuntimeError('header too large')
        with path.open('wb') as f:
            f.write(header)
            f.write(b'\x00'*(SUPERBLOCK_SIZE-len(header)))
            f.write(payload)
        return fabric_tag

class FabricImage:
    def __init__(self, path, verify=True):
        self.path=Path(path)
        self._f=self.path.open('rb')
        self._mm=mmap.mmap(self._f.fileno(), 0, access=mmap.ACCESS_READ)
        vals=struct.unpack(_HDR_FMT, self._mm[:_HDR_SIZE])
        magic, ver, cell_size, page_size, _reserved, count, tag, src_hash, data_hash=vals
        if magic != MAGIC or ver != FORMAT_VERSION or cell_size != CELL_SIZE or page_size != PAGE_SIZE:
            raise FabricIntegrityError('unsupported or corrupt superblock')
        self.cell_count=count; self.fabric_tag=tag; self.source_manifest_hash=src_hash; self.data_hash=data_hash
        if len(self._mm) != SUPERBLOCK_SIZE + count*CELL_SIZE:
            raise FabricIntegrityError('size mismatch')
        if verify:
            actual=hashlib.sha256(self._mm[SUPERBLOCK_SIZE:]).digest()
            if actual != data_hash: raise FabricIntegrityError('cell data hash mismatch')
            if int.from_bytes(actual[:8],'big') != tag: raise FabricIntegrityError('fabric tag mismatch')

    def close(self):
        self._mm.close(); self._f.close()

    def cell_index(self, address: FabricAddress):
        if address.fabric_tag != self.fabric_tag: raise InvalidAddressError('wrong fabric tag')
        idx=address.page*CELLS_PER_PAGE + address.cell
        if idx >= self.cell_count: raise InvalidAddressError('cell out of range')
        return idx

    def address_for_index(self, idx, lane=0, flags=0):
        if not 0 <= idx < self.cell_count: raise InvalidAddressError('index')
        return FabricAddress(self.fabric_tag, idx//CELLS_PER_PAGE, idx%CELLS_PER_PAGE, lane, flags)

    def read(self, address):
        idx=self.cell_index(address)
        off=SUPERBLOCK_SIZE + idx*CELL_SIZE
        return ChiralityCell.unpack(self._mm[off:off+CELL_SIZE])
