import json,hashlib,time
from pathlib import Path

def stable_json(x): return json.dumps(x,sort_keys=True,separators=(',',':'),default=str).encode()
def digest_obj(x): return hashlib.sha256(stable_json(x)).hexdigest()
def file_sha256(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def now_ns(): return time.time_ns()
