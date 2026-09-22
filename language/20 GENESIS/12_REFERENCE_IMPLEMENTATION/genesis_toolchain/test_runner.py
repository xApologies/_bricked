from __future__ import annotations
import json,tempfile
from pathlib import Path
from genesis_system_io.compiler import compile_source
from .build import BuildDriver
from .tracing import TracingRuntime

class TestRunner:
    def __init__(self,driver:BuildDriver|None=None): self.driver=driver or BuildDriver()
    def run_case(self,path:Path)->dict:
        path=Path(path); spec=json.loads(path.read_text(encoding="utf-8")); src=(path.parent/spec["source"]).read_text(encoding="utf-8")
        expected_diag=spec.get("expected_diagnostic")
        check=self.driver.check_text(src,spec["source"])
        if expected_diag:
            got=check.diagnostics[0].code if check.diagnostics else None
            return {"name":spec.get("name",path.stem),"pass":(not check.ok and got==expected_diag),"expected_diagnostic":expected_diag,"got":got}
        if not check.ok: return {"name":spec.get("name",path.stem),"pass":False,"diagnostics":[d.as_dict() for d in check.diagnostics]}
        with tempfile.TemporaryDirectory() as td:
            b=self.driver.build_text(src,Path(td)/"build",spec["source"])
            p=compile_source(src,spec["source"]); rt=TracingRuntime(p,Path(td)/"runtime")
            for seed in spec.get("seeds",[]): rt.seed(seed["endpoint"],seed["path"],bytes.fromhex(seed.get("hex","") ) if "hex" in seed else seed.get("text","").encode())
            try: run=rt.run()
            except Exception as e: return {"name":spec.get("name",path.stem),"pass":False,"runtime_error":str(e)}
            ok=run.status==spec.get("expected_status","CLOSED")
            for r in spec.get("expected_registers",[]): ok=ok and r in run.registers
            ops=[x["operation"] for x in run.receipts]
            for op in spec.get("expected_receipts",[]): ok=ok and op in ops
            return {"name":spec.get("name",path.stem),"pass":bool(ok),"status":run.status,"build_id":b.manifest.build_id if b.manifest else None,"receipt_root":run.receipt_root,"event_count":len(run.events)}
    def run_many(self,paths):
        rs=[self.run_case(Path(p)) for p in paths]; return {"pass":all(x["pass"] for x in rs),"count":len(rs),"results":rs}
