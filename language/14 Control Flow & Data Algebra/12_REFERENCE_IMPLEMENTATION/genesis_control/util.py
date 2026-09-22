import hashlib, json, re

def canonical_bytes(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha256_obj(x): return hashlib.sha256(canonical_bytes(x)).hexdigest()

def strip_comment(line):
    out=[]; q=None; esc=False
    for c in line:
        if esc: out.append(c); esc=False; continue
        if c=='\\': out.append(c); esc=True; continue
        if q:
            out.append(c)
            if c==q: q=None
            continue
        if c in ('"',"'"): q=c; out.append(c); continue
        if c=='#': break
        out.append(c)
    return ''.join(out)

def split_top(text, sep=','):
    out=[]; start=0; depth=0; q=None; esc=False
    opens=set('<({['); closes=set('>)}]')
    for i,c in enumerate(text):
        if esc: esc=False; continue
        if c=='\\': esc=True; continue
        if q:
            if c==q:q=None
            continue
        if c in ('"',"'"): q=c; continue
        if c in opens: depth+=1
        elif c in closes: depth-=1
        elif c==sep and depth==0:
            out.append(text[start:i].strip()); start=i+1
    out.append(text[start:].strip())
    return [x for x in out if x]

def normalize_type(t): return re.sub(r'\s+','',str(t)).upper()
def type_kind(t):
    s=normalize_type(t); m=re.match(r'^([A-Z_][A-Z0-9_]*)',s); return m.group(1) if m else s

def type_args(t):
    s=normalize_type(t)
    if '<' not in s:return []
    return split_top(s[s.index('<')+1:-1])
