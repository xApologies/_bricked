from __future__ import annotations
import hashlib,json,re

def canonical_json(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha256_obj(obj): return hashlib.sha256(canonical_json(obj).encode()).hexdigest()
def strip_comment(line):
    q=False; out=[]; i=0
    while i<len(line):
        c=line[i]
        if c=='"': q=not q; out.append(c); i+=1; continue
        if c=='#' and not q: break
        out.append(c); i+=1
    return ''.join(out)
def split_args(text):
    if not text.strip(): return []
    return [x.strip() for x in text.split(',') if x.strip()]
def norm_type(t): return re.sub(r'\s+','',t).upper()
