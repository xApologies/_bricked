from __future__ import annotations
import hashlib, json
from typing import Any

def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj)).hexdigest()
