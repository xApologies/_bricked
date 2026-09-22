from .util import strip_comment

def format_source(text):
    out=[]; indent=0
    for raw in text.splitlines():
        s=strip_comment(raw).strip().rstrip(';').rstrip()
        if not s: continue
        if s=='}': indent=max(0,indent-1)
        out.append('  '*indent+s)
        if s.endswith('{'): indent+=1
    return '\n'.join(out)+'\n'
