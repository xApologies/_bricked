from __future__ import annotations
from genesis_system_io.brane import BraneHostReference
from genesis_system_io.compiler import compile_source
from genesis_system_io.bytecode import encode
from genesis_system_io.util import digest_obj,sha256_bytes
from genesis_system_io.errors import fail

class CompilerAwareBraneHost(BraneHostReference):
    """Bootstrap-only BRANE host adapter.

    A port with role=compiler and capability=compile accepts a CAS ref to Genesis
    source and returns a CAS ref to deterministic GIO bytecode. The compiler used
    here is intentionally the Stage-0 Python oracle and is reported as such.
    """
    def __init__(self,cas,host_id="mk43.brane.bootstrap.reference",compiler_id="python-oracle:genesis-system-0.6.0"):
        super().__init__(host_id); self.cas=cas; self.compiler_id=compiler_id
    def realize(self,alias:str,capability:str,payload_ref:str,m5=None):
        if alias in self.mounted and self.mounted[alias].role=="compiler" and capability=="compile":
            m=self.mounted[alias]
            if capability not in m.capabilities: fail("BRANE_CAPABILITY_UNAVAILABLE",capability)
            src=self.cas.get(payload_ref)
            try: text=src.decode("utf-8")
            except UnicodeDecodeError: fail("BOOTSTRAP_SOURCE_ENCODING","utf-8")
            p=compile_source(text,"bootstrap/bootstrap_controller.gen")
            blob=encode(p); out_ref=self.cas.put(blob)
            self.sequence+=1
            m5=dict(m5 or {})
            if "Z" in m5: fail("BRANE_Z_CALLER_OWNED")
            for k in ("I","D","Chi","R","P"): m5.setdefault(k,"unspecified")
            seed={"host":self.host_id,"sequence":self.sequence,"module":m.module_id,"capability":capability,"payload_ref":payload_ref,"M5":m5,"compiler_id":self.compiler_id}
            z="z:"+digest_obj(seed)
            result={"role":"compiler","module_id":m.module_id,"capability":"compile","payload_ref":payload_ref,"M6":{**m5,"Z":z},"status":"REALIZED","compiler_id":self.compiler_id,"source_ref":payload_ref,"bytecode_ref":out_ref,"bytecode_sha256":sha256_bytes(blob),"program_id":p.metadata.get("program_id"),"proof_root":p.metadata.get("verification",{}).get("proof_root"),"instruction_count":len(p.instructions)}
            result["result_root"]=digest_obj(result)
            return result
        return super().realize(alias,capability,payload_ref,m5)
