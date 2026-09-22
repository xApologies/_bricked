import json,hashlib,time

def stable_json(x): return json.dumps(x,sort_keys=True,separators=(',',':'),default=str).encode()
def digest_obj(x): return hashlib.sha256(stable_json(x)).hexdigest()
def now_ns(): return time.time_ns()
