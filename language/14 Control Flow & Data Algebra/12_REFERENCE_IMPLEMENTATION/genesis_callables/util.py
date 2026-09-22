import hashlib, json, re

def canonical_bytes(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def sha256_obj(obj): return hashlib.sha256(canonical_bytes(obj)).hexdigest()
def sha256_text(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()

def split_top_level(text, sep=','):
    out=[]; start=0; angle=paren=bracket=0; quote=False; esc=False
    for i,c in enumerate(text):
        if esc: esc=False; continue
        if c=='\\' and quote: esc=True; continue
        if c=='"': quote=not quote; continue
        if quote: continue
        if c=='<': angle+=1
        elif c=='>': angle=max(0,angle-1)
        elif c=='(': paren+=1
        elif c==')': paren=max(0,paren-1)
        elif c=='[': bracket+=1
        elif c==']': bracket=max(0,bracket-1)
        elif c==sep and angle==0 and paren==0 and bracket==0:
            out.append(text[start:i].strip()); start=i+1
    out.append(text[start:].strip())
    return [x for x in out if x]

def replace_identifier(text, mapping):
    """Identifier substitution outside strings. Dotted names are treated component-wise only for exact bare identifiers."""
    out=[]; i=0; quote=False; esc=False
    while i<len(text):
        c=text[i]
        if quote:
            out.append(c)
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': quote=False
            i+=1; continue
        if c=='"': quote=True; out.append(c); i+=1; continue
        if c.isalpha() or c=='_':
            j=i+1
            while j<len(text) and (text[j].isalnum() or text[j]=='_'): j+=1
            tok=text[i:j]; out.append(mapping.get(tok,tok)); i=j; continue
        out.append(c); i+=1
    return ''.join(out)

def replace_type_vars(text, mapping):
    # Generic variable names only occur as type tokens in Section 13's grammar.
    return replace_identifier(text,mapping)

CALL_RX=re.compile(r'^call\s+(.+?)\s+as\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:@\{.*\})?$')

def parse_call_head(line):
    # call fn<T,U> (a,b) as out  OR call fn<T> a b as out
    m=CALL_RX.match(line.strip())
    if not m: return None
    left,out=m.group(1).strip(),m.group(2)
    # attrs are deliberately not part of v0.1 callable syntax; base ops retain attrs.
    if '(' in left:
        p=left.find('('); q=left.rfind(')')
        if q<p: return None
        fnpart=left[:p].strip(); argtext=left[p+1:q].strip()
        if left[q+1:].strip(): return None
        args=split_top_level(argtext)
    else:
        # split function reference (including nested angle args) from whitespace args
        depth=0; cut=None
        for i,c in enumerate(left):
            if c=='<': depth+=1
            elif c=='>': depth=max(0,depth-1)
            elif c.isspace() and depth==0:
                cut=i; break
        if cut is None: fnpart=left; args=[]
        else: fnpart=left[:cut].strip(); args=[x for x in left[cut:].split() if x]
    type_args=[]; fnref=fnpart
    if '<' in fnpart:
        p=fnpart.find('<')
        if not fnpart.endswith('>'): return None
        fnref=fnpart[:p].strip(); inner=fnpart[p+1:-1]
        type_args=split_top_level(inner)
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.]*(?:::[A-Za-z_][A-Za-z0-9_]*)?',fnref): return None
    return fnref,tuple(type_args),tuple(args),out
