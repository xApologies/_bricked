import hashlib, json, time

def sha256_bytes(b: bytes): return hashlib.sha256(b).hexdigest()
def stable_json(obj): return json.dumps(obj, sort_keys=True, separators=(',',':')).encode()
def digest_obj(obj): return hashlib.sha256(stable_json(obj)).hexdigest()
def now_ns(): return time.time_ns()
def clip01(v): return 0.0 if v < 0 else 1.0 if v > 1 else float(v)
