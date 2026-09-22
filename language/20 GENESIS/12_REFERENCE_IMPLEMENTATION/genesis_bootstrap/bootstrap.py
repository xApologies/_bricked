from __future__ import annotations
import tempfile
from pathlib import Path
from genesis_system_io.compiler import compile_source
from genesis_system_io.bytecode import encode,decode
from genesis_system_io.util import object_ref
from .runtime import BootstrapRuntime
from .model import StageRecord,BootstrapResult
from .frontier import load_frontier
from .util import sha256_bytes,digest_obj
from .errors import fail

class BootstrapHarness:
    def __init__(self,controller_source:Path,frontier_path:Path,compiler_id="python-oracle:genesis-system-0.6.0"):
        self.controller_source=Path(controller_source); self.frontier_path=Path(frontier_path); self.compiler_id=compiler_id
    def _stage0(self,text:str)->tuple[bytes,object]:
        p=compile_source(text,"bootstrap/bootstrap_controller.gen"); return encode(p),p
    def _run_stage(self,blob:bytes,text:bytes,stage:int,prior:str|None,work:Path)->tuple[StageRecord,bytes]:
        p=decode(blob); rt=BootstrapRuntime(p,work/f"stage{stage}",compiler_id=self.compiler_id)
        # Controller contract fixes this source endpoint/path.
        rt.seed("source","bootstrap/bootstrap_controller.gen",text)
        rr=rt.run()
        if rr.status!="CLOSED": fail("BOOTSTRAP_STAGE_OPEN",str(stage))
        compiled=rr.registers.get("compiled")
        if not isinstance(compiled,dict) or "bytecode_ref" not in compiled: fail("BOOTSTRAP_OUTPUT_NOT_IN_CAS",str(stage))
        new_blob=rt.cas.get(compiled["bytecode_ref"])
        rec=StageRecord(stage,sha256_bytes(text),sha256_bytes(new_blob),compiled["bytecode_ref"],compiled.get("program_id","") or "",compiled.get("proof_root","") or "",compiled.get("compiler_id",self.compiler_id),prior)
        return rec,new_blob
    def run(self,work_dir:Path|None=None)->BootstrapResult:
        if not self.controller_source.is_file(): fail("BOOTSTRAP_SOURCE_MISSING",str(self.controller_source))
        frontier=load_frontier(self.frontier_path); frontier_root=digest_obj(frontier)
        text=self.controller_source.read_bytes(); decoded=text.decode("utf-8")
        stage0_blob,p0=self._stage0(decoded); h0=sha256_bytes(stage0_blob)
        own=False; td=None
        if work_dir is None:
            td=tempfile.TemporaryDirectory(); work=Path(td.name); own=True
        else: work=Path(work_dir); work.mkdir(parents=True,exist_ok=True)
        try:
            s1,stage1_blob=self._run_stage(stage0_blob,text,1,h0,work)
            if s1.bytecode_sha256!=h0: fail("BOOTSTRAP_STAGE_MISMATCH",f"stage0={h0} stage1={s1.bytecode_sha256}")
            s2,stage2_blob=self._run_stage(stage1_blob,text,2,s1.bytecode_sha256,work)
            if s2.bytecode_sha256!=s1.bytecode_sha256: fail("BOOTSTRAP_STAGE_MISMATCH",f"stage1={s1.bytecode_sha256} stage2={s2.bytecode_sha256}")
            proof0=p0.metadata.get("verification",{}).get("proof_root","")
            if s1.proof_root!=proof0 or s2.proof_root!=proof0: fail("BOOTSTRAP_PROOF_MISMATCH")
            s0=StageRecord(0,sha256_bytes(text),h0,object_ref(stage0_blob),p0.metadata.get("program_id","") or "",proof0,self.compiler_id,None)
            stages=(s0,s1,s2)
            pre={"kind":"GENESIS_BOOTSTRAP_RECEIPT","version":"0.1.0","status":"BOOTSTRAP_FIXED_POINT","self_hosted":False,"source_sha256":sha256_bytes(text),"frontier_root":frontier_root,"stages":[s.as_dict() for s in stages]}
            root=digest_obj(pre)
            return BootstrapResult("BOOTSTRAP_FIXED_POINT",True,False,sha256_bytes(text),stages,frontier_root,root)
        finally:
            if own and td is not None: td.cleanup()
