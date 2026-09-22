from __future__ import annotations
from pathlib import Path
from .model import *
from .storage import SandboxFS,CASStore
from .brane import BraneHostReference
from .blackglass import BlackglassHeartReference
from .device import DeviceReference
from .verifier import verify
from .receipts import make_receipt
from .errors import fail
from .util import canonical_json,digest_obj

class SystemRuntime:
    def __init__(self,program:SystemProgram,base:Path):
        verify(program); self.p=program; self.base=Path(base)
        roots={ep.root:self.base/ep.root for ep in program.endpoints.values() if ep.kind in (EndpointKind.SOURCE,EndpointKind.DERIVED,EndpointKind.AUDIT)}
        self.fs=SandboxFS(roots); self.cas=CASStore(self.base/"cas"); self.brane=BraneHostReference(); self.heart=BlackglassHeartReference(self.cas); self.devices=DeviceReference()
        self.regs={}; self.receipts=[]; self.root="0"*64; self.seq=0
    def seed(self,endpoint:str,path:str,data:bytes):
        ep=self.p.endpoints[endpoint]
        if ep.kind!=EndpointKind.SOURCE: fail("SYSTEM_SEED_SOURCE_ONLY")
        p=self.fs._path(ep.root,path); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data)
    def _receipt(self,op,target,status,input_value=None,output_value=None,detail=None):
        self.seq+=1; r=make_receipt(self.seq,op,target,status,input_value,output_value,self.root,detail); self.root=r.provenance_root; self.receipts.append(r.as_dict())
    def run(self)->RunResult:
        status="OPEN"
        for ins in self.p.instructions:
            op=ins.op; a=ins.attrs
            if op==Op.READ:
                ep=self.p.endpoints[a["endpoint"]]; data=self.fs.read(ep.root,a["path"]); self.regs[a["out"]]=data; self._receipt("READ",ep.name,"PASS",None,data,{"path":a["path"]})
            elif op==Op.WRITE_DERIVED:
                ep=self.p.endpoints[a["endpoint"]]; data=self._bytes(self.regs[a["src"]]); ref=self.fs.write_derived(ep.root,a["path"],data); self._receipt("WRITE_DERIVED",ep.name,"PASS",data,ref,{"path":a["path"]})
            elif op==Op.APPEND_AUDIT:
                ep=self.p.endpoints[a["endpoint"]]; data=self._bytes(self.regs[a["src"]]); ref=self.fs.append_audit(ep.root,a["path"],data); self._receipt("APPEND_AUDIT",ep.name,"PASS",data,ref,{"path":a["path"]})
            elif op==Op.CAS_PUT:
                data=self._bytes(self.regs[a["src"]]); ref=self.cas.put(data); self.regs[a["out"]]=ref; self._receipt("CAS_PUT","cas","PASS",data,ref)
            elif op==Op.CAS_GET:
                ref=self.regs[a["ref"]]; data=self.cas.get(ref); self.regs[a["out"]]=data; self._receipt("CAS_GET","cas","PASS",ref,data)
            elif op==Op.BRANE_MOUNT:
                out=self.brane.mount(self.p.ports[a["port"]]); self._receipt("BRANE_MOUNT",a["port"],"PASS",self.p.ports[a["port"]].as_dict(),out)
            elif op==Op.BRANE_REALIZE:
                payload=self.regs[a["payload"]]
                if isinstance(payload,str) and payload.startswith("sha256:"): pref=payload
                else: pref=self.cas.put(self._bytes(payload))
                out=self.brane.realize(a["port"],a["capability"],pref); self.regs[a["out"]]=out; self._receipt("BRANE_REALIZE",a["port"],"PASS",pref,out,{"capability":a["capability"]})
            elif op==Op.BLACKGLASS_PROPOSE:
                v=self.regs[a["src"]]; out=self.heart.propose(v,self.root); self.regs[a["out"]]=out; self._receipt("BLACKGLASS_PROPOSE",a["endpoint"],"STAGED",v,out)
            elif op==Op.BLACKGLASS_ADMIT:
                v=self.regs[a["proposal"]]; pid=v["proposal_id"] if isinstance(v,dict) else str(v); out=self.heart.admit(pid,authority=True); self.regs[a["out"]]=out; self._receipt("BLACKGLASS_ADMIT",a["endpoint"],"COMMITTED",v,out)
            elif op==Op.DEVICE_REQUEST:
                pv=self.regs[a["payload"]] if a.get("payload") else None; pref=None if pv is None else (pv if isinstance(pv,str) and pv.startswith("sha256:") else self.cas.put(self._bytes(pv)))
                out=self.devices.request(a["device"],a["capability"],pref); self.regs[a["out"]]=out; self._receipt("DEVICE_REQUEST",a["endpoint"],"ACCEPTED",pref,out,{"device":a["device"],"capability":a["capability"]})
            elif op==Op.ASSERT_EQ:
                if self.regs[a["left"]]!=self.regs[a["right"]]: fail("SYSTEM_ASSERT_FAILED",f"{a['left']} != {a['right']}")
                self._receipt("ASSERT_EQ","runtime","PASS",self.regs[a["left"]],self.regs[a["right"]])
            elif op==Op.SYS_CLOSE:
                status="CLOSED"; self._receipt("SYS_CLOSE","runtime","CLOSED",None,{"register_count":len(self.regs)})
        return RunResult(status,self.regs.copy(),list(self.receipts),self.root,self.heart.durable.copy())
    @staticmethod
    def _bytes(v):
        if isinstance(v,bytes): return v
        if isinstance(v,str): return v.encode()
        return canonical_json(v)
