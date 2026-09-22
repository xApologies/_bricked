import hashlib, json

def canonical_bytes(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')

def sha256_obj(x): return hashlib.sha256(canonical_bytes(x)).hexdigest()
def sha256_bytes(x): return hashlib.sha256(x).hexdigest()

def canonical_obj(x):
    if isinstance(x,dict): return {k:canonical_obj(x[k]) for k in sorted(x)}
    if isinstance(x,list): return [canonical_obj(v) for v in x]
    return x
