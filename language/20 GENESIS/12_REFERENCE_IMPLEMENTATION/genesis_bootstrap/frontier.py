from __future__ import annotations
import json
from pathlib import Path
from .errors import fail
from .util import digest_obj

ALLOWED={"HOST_ORACLE","GENESIS_CONTROLLED","GENESIS_NATIVE","DEFERRED"}
REQUIRED={"bootstrap_controller","parser","verifier","bytecode_encoder","runtime"}

def load_frontier(path:Path)->dict:
    data=json.loads(Path(path).read_text(encoding="utf-8")); verify_frontier(data); return data

def verify_frontier(data:dict)->dict:
    if data.get("kind")!="GENESIS_SELF_HOST_FRONTIER" or data.get("version")!="0.1.0": fail("BOOTSTRAP_FRONTIER_INVALID","header")
    comps=data.get("components",{})
    if not REQUIRED.issubset(comps): fail("BOOTSTRAP_FRONTIER_INVALID","missing required components")
    for name,item in comps.items():
        if item.get("status") not in ALLOWED: fail("BOOTSTRAP_FRONTIER_INVALID",name)
    if data.get("release_status")=="FULL_SELF_HOST":
        if any(v.get("status")!="GENESIS_NATIVE" for v in comps.values() if v.get("required_for_boot",True)):
            fail("BOOTSTRAP_FALSE_SELF_HOST_CLAIM")
    return {"frontier_root":digest_obj(data),"component_count":len(comps),"release_status":data.get("release_status")}
