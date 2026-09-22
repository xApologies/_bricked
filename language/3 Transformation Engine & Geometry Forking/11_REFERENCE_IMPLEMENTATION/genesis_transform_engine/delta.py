from pathlib import Path
import hashlib,mmap,struct
from vendor.genesis_chirality_machine.cell import ChiralityCell
from .errors import DeltaIntegrityError

MAGIC=b'GTDXFR01'; VERSION=1; SUPERBLOCK=4096; RECORD_SIZE=40
HDR='<8sIIIIQQQQ32s32s32s32s32s32s'
HDR_SIZE=struct.calcsize(HDR)

class TransformationDeltaWriter:
    def __init__(self,path,fabric_tag,region_start,region_count,parent_digest,child_digest,plan_digest,pre_root,post_root):
        self.path=Path(path); self.tmp=self.path.with_suffix(self.path.suffix+'.tmp'); self.f=self.tmp.open('wb+'); self.f.write(b'\0'*SUPERBLOCK)
        self.fabric_tag=int(fabric_tag); self.region_start=int(region_start); self.region_count=int(region_count)
        self.parent=bytes.fromhex(parent_digest); self.child=bytes.fromhex(child_digest); self.plan=bytes.fromhex(plan_digest); self.pre=bytes.fromhex(pre_root); self.post=bytes.fromhex(post_root)
        self.h=hashlib.sha256(); self.count=0; self.last=-1
    def write(self,idx,cell):
        idx=int(idx)
        if not self.region_start<=idx<self.region_start+self.region_count: raise ValueError('delta outside region')
        if idx<=self.last: raise ValueError('delta records must be sorted unique')
        rec=struct.pack('<Q',idx)+cell.pack(); self.f.write(rec); self.h.update(rec); self.count+=1; self.last=idx
    def finalize(self):
        payload=self.h.digest(); hdr=struct.pack(HDR,MAGIC,VERSION,RECORD_SIZE,0,0,self.count,self.fabric_tag,self.region_start,self.region_count,self.parent,self.child,self.plan,self.pre,self.post,payload)
        if len(hdr)>SUPERBLOCK: raise RuntimeError('header')
        self.f.seek(0); self.f.write(hdr); self.f.write(b'\0'*(SUPERBLOCK-len(hdr))); self.f.flush(); self.f.close(); self.tmp.replace(self.path); return payload.hex()
    def abort(self):
        try:self.f.close()
        except:pass
        if self.tmp.exists(): self.tmp.unlink()

class TransformationDeltaSegment:
    def __init__(self,path,verify=True):
        self.path=Path(path); self.f=self.path.open('rb'); self.mm=mmap.mmap(self.f.fileno(),0,access=mmap.ACCESS_READ)
        vals=struct.unpack(HDR,self.mm[:HDR_SIZE]); magic,ver,rs,_a,_b,count,tag,start,span,parent,child,plan,pre,post,payload=vals
        if magic!=MAGIC or ver!=VERSION or rs!=RECORD_SIZE: raise DeltaIntegrityError('bad delta header')
        self.record_count=count; self.fabric_tag=tag; self.region_start=start; self.region_count=span; self.parent_digest=parent.hex(); self.child_digest=child.hex(); self.plan_digest=plan.hex(); self.pre_state_root=pre.hex(); self.post_state_root=post.hex(); self.payload_hash=payload.hex()
        if len(self.mm)!=SUPERBLOCK+count*RECORD_SIZE: raise DeltaIntegrityError('delta size')
        if verify and hashlib.sha256(self.mm[SUPERBLOCK:]).digest()!=payload: raise DeltaIntegrityError('delta payload hash')
    def close(self): self.mm.close(); self.f.close()
    def _idx_at(self,n): return struct.unpack('<Q',self.mm[SUPERBLOCK+n*RECORD_SIZE:SUPERBLOCK+n*RECORD_SIZE+8])[0]
    def read_index(self,idx):
        lo,hi=0,self.record_count-1
        while lo<=hi:
            m=(lo+hi)//2; x=self._idx_at(m)
            if x==idx:
                o=SUPERBLOCK+m*RECORD_SIZE+8; return ChiralityCell.unpack(self.mm[o:o+32])
            if x<idx: lo=m+1
            else: hi=m-1
        return None
