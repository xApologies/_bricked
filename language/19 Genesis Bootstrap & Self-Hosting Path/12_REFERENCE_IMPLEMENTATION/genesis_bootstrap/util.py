from __future__ import annotations
import hashlib,json
from pathlib import Path
from typing import Any

def canonical_json(obj:Any)->bytes:
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

def sha256_bytes(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path:Path)->str:
    return sha256_bytes(Path(path).read_bytes())

def digest_obj(obj:Any)->str:
    return sha256_bytes(canonical_json(obj))
