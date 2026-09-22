from __future__ import annotations
from typing import Any
from .model import PortManifest
from .errors import fail
from .util import digest_obj, canonical_json

class BraneHostReference:
    def __init__(self,host_id:str="mk43.brane.reference"):
        self.host_id=host_id; self.mounted:dict[str,PortManifest]={}; self.sequence=0
    @staticmethod
    def validate_manifest(m:PortManifest):
        if m.internal_dimension!=5: fail("BRANE_PORT_INVALID","internal_dimension")
        if m.contract_version!="2.0": fail("BRANE_PORT_INVALID","contract_version")
        if m.canonical_state_policy!="READ_ONLY": fail("BRANE_PORT_INVALID","canonical_state_policy")
        if m.rewrite_policy!="DERIVED_ONLY": fail("BRANE_PORT_INVALID","rewrite_policy")
        if not m.role or not m.module_id or not m.capabilities: fail("BRANE_PORT_INVALID","identity/capabilities")
        return True
    def mount(self,m:PortManifest):
        self.validate_manifest(m); self.mounted[m.alias]=m
        return {"alias":m.alias,"module_id":m.module_id,"status":"MOUNTED","manifest_root":digest_obj(m.as_dict())}
    def realize(self,alias:str,capability:str,payload_ref:str,m5:dict[str,Any]|None=None):
        if alias not in self.mounted: fail("BRANE_PORT_NOT_MOUNTED",alias)
        m=self.mounted[alias]
        if capability not in m.capabilities: fail("BRANE_CAPABILITY_UNAVAILABLE",capability)
        m5=dict(m5 or {})
        if "Z" in m5: fail("BRANE_Z_CALLER_OWNED")
        required=("I","D","Chi","R","P")
        for k in required: m5.setdefault(k,"unspecified")
        self.sequence+=1
        seed={"host":self.host_id,"sequence":self.sequence,"module":m.module_id,"capability":capability,"payload_ref":payload_ref,"M5":m5}
        z="z:"+digest_obj(seed)
        m6={**m5,"Z":z}
        result={"role":m.role,"module_id":m.module_id,"capability":capability,"payload_ref":payload_ref,"M6":m6,"status":"REALIZED"}
        result["result_root"]=digest_obj(result)
        return result
