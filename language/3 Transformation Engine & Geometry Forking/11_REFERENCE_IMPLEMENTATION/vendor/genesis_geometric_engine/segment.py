from pathlib import Path
import hashlib, mmap, struct
from .errors import SegmentIntegrityError
from vendor.genesis_chirality_machine.cell import ChiralityCell

MAGIC=b'GOSMMO01'; VERSION=1; SUPERBLOCK=4096; RECORD_SIZE=40
HDR='<8sIIIIQQQQ32s32s32s32s'
HDR_SIZE=struct.calcsize(HDR)

class GeometricOverlayWriter:
    def __init__(self, path, fabric_tag, region_start, region_count, mmo_digest, instance_digest, source_manifest_digest):
        self.path=Path(path); self.fabric_tag=int(fabric_tag); self.region_start=int(region_start); self.region_count=int(region_count)
        self.mmo_digest=bytes.fromhex(mmo_digest); self.instance_digest=bytes.fromhex(instance_digest); self.source_digest=bytes.fromhex(source_manifest_digest)
        self.tmp=self.path.with_suffix(self.path.suffix+'.tmp'); self.f=self.tmp.open('wb+'); self.f.write(b'\0'*SUPERBLOCK); self.h=hashlib.sha256(); self.count=0; self.last=-1
    def write(self, cell_index, cell: ChiralityCell):
        cell_index=int(cell_index)
        if not (self.region_start <= cell_index < self.region_start+self.region_count): raise ValueError('record outside region')
        if cell_index <= self.last: raise ValueError('records must be strictly sorted')
        rec=struct.pack('<Q',cell_index)+cell.pack(); self.f.write(rec); self.h.update(rec); self.count+=1; self.last=cell_index
    def finalize(self):
        payload_hash=self.h.digest()
        header=struct.pack(HDR,MAGIC,VERSION,RECORD_SIZE,0,0,self.count,self.fabric_tag,self.region_start,self.region_count,
                           self.mmo_digest,self.instance_digest,payload_hash,self.source_digest)
        if len(header)>SUPERBLOCK: raise RuntimeError('header')
        self.f.seek(0); self.f.write(header); self.f.write(b'\0'*(SUPERBLOCK-len(header))); self.f.flush(); self.f.close()
        self.tmp.replace(self.path)
        return payload_hash.hex()
    def abort(self):
        try:self.f.close()
        except:pass
        if self.tmp.exists(): self.tmp.unlink()

class GeometricOverlaySegment:
    def __init__(self,path,verify=True):
        self.path=Path(path); self.f=self.path.open('rb'); self.mm=mmap.mmap(self.f.fileno(),0,access=mmap.ACCESS_READ)
        vals=struct.unpack(HDR,self.mm[:HDR_SIZE])
        magic,ver,rs,_r1,_r2,count,tag,start,span,mmo,inst,payload,source=vals
        if magic!=MAGIC or ver!=VERSION or rs!=RECORD_SIZE: raise SegmentIntegrityError('bad segment header')
        self.record_count=count; self.fabric_tag=tag; self.region_start=start; self.region_count=span
        self.mmo_digest=mmo.hex(); self.instance_digest=inst.hex(); self.payload_hash=payload.hex(); self.source_manifest_digest=source.hex()
        expected=SUPERBLOCK+count*RECORD_SIZE
        if len(self.mm)!=expected: raise SegmentIntegrityError('segment size')
        if verify and hashlib.sha256(self.mm[SUPERBLOCK:]).digest()!=payload: raise SegmentIntegrityError('payload hash')
    def close(self): self.mm.close(); self.f.close()
    def _idx_at(self, recno): return struct.unpack('<Q',self.mm[SUPERBLOCK+recno*RECORD_SIZE:SUPERBLOCK+recno*RECORD_SIZE+8])[0]
    def read_index(self, cell_index):
        lo,hi=0,self.record_count-1
        while lo<=hi:
            mid=(lo+hi)//2; idx=self._idx_at(mid)
            if idx==cell_index:
                off=SUPERBLOCK+mid*RECORD_SIZE+8; return ChiralityCell.unpack(self.mm[off:off+32])
            if idx<cell_index: lo=mid+1
            else: hi=mid-1
        return None
