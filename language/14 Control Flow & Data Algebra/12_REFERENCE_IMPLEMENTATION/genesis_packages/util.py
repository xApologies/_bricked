import hashlib,json
from pathlib import Path

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def canonical(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def sha256_obj(obj): return sha256_bytes(canonical(obj))
def read_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def package_file_hashes(root):
    root=Path(root); out=[]
    for p in sorted(x for x in root.rglob('*') if x.is_file() and not any(part in {'.git','__pycache__','.genesis'} for part in x.relative_to(root).parts) and x.name!='genesis.lock.json'):
        out.append({'path':p.relative_to(root).as_posix(),'sha256':sha256_bytes(p.read_bytes()),'size':p.stat().st_size})
    return out
