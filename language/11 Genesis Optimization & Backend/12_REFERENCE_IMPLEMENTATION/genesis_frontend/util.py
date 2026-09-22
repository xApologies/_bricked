import json,hashlib,re

def canonical_bytes(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def sha256_obj(obj): return hashlib.sha256(canonical_bytes(obj)).hexdigest()
def sha256_text(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()

def strip_comment(line):
    out=[]; quote=False; esc=False; i=0
    while i<len(line):
        c=line[i]
        if esc: out.append(c); esc=False; i+=1; continue
        if c=='\\' and quote: out.append(c); esc=True; i+=1; continue
        if c=='"': quote=not quote; out.append(c); i+=1; continue
        if not quote and c=='#': break
        if not quote and c=='/' and i+1<len(line) and line[i+1]=='/': break
        out.append(c); i+=1
    return ''.join(out).rstrip()

def split_attrs(line):
    quote=False; esc=False; depth=0
    for i,c in enumerate(line):
        if esc: esc=False; continue
        if c=='\\' and quote: esc=True; continue
        if c=='"': quote=not quote; continue
        if not quote and c=='@' and i+1<len(line) and line[i+1]=='{':
            raw=line[i+1:].strip().rstrip(';').strip()
            return line[:i].rstrip(), json.loads(raw)
    return line.rstrip(';').rstrip(), {}

def coarse_type(t):
    return re.split(r'<',str(t).strip(),1)[0].upper()
