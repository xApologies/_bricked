from __future__ import annotations
import hashlib,json
from pathlib import Path
from typing import Any

def canonical_json(obj:Any)->bytes:
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False,default=_json_default).encode("utf-8")

def _json_default(v):
    if isinstance(v,bytes): return {"$bytes_hex":v.hex()}
    if hasattr(v,"as_dict"): return v.as_dict()
    raise TypeError(type(v).__name__)

def sha256_bytes(data:bytes)->str: return hashlib.sha256(data).hexdigest()
def sha256_file(path:Path)->str: return sha256_bytes(Path(path).read_bytes())
def digest_obj(obj:Any)->str: return sha256_bytes(canonical_json(obj))
def stable_write(path:Path,data:bytes|str):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(data,str): data=data.encode("utf-8")
    path.write_bytes(data)
