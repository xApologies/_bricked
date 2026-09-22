import hashlib, json, time

def stable_json(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest_obj(obj): return hashlib.sha256(stable_json(obj)).hexdigest()
def now_ns(): return time.time_ns()
def file_sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
