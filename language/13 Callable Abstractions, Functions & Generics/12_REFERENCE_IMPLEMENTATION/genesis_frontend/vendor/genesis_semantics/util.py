import json, hashlib

def canonical_bytes(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def sha256_obj(obj): return hashlib.sha256(canonical_bytes(obj)).hexdigest()
def sha256_bytes(data): return hashlib.sha256(data).hexdigest()
