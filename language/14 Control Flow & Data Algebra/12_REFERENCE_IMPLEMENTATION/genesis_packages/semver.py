from dataclasses import dataclass
import re
from .errors import PackageError

_RX=re.compile(r'^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$')
@dataclass(frozen=True,order=True)
class Version:
    major:int; minor:int; patch:int
    @classmethod
    def parse(cls,s):
        m=_RX.fullmatch(str(s))
        if not m: raise PackageError(f'invalid semantic version {s!r}','VERSION_INVALID')
        return cls(*(int(x) for x in m.groups()))
    def __str__(self): return f'{self.major}.{self.minor}.{self.patch}'

@dataclass(frozen=True)
class Requirement:
    raw:str
    def matches(self,v):
        if not isinstance(v,Version): v=Version.parse(v)
        s=self.raw.strip()
        if s=='*': return True
        if s.startswith('^'):
            b=Version.parse(s[1:])
            if b.major>0: upper=Version(b.major+1,0,0)
            elif b.minor>0: upper=Version(0,b.minor+1,0)
            else: upper=Version(0,0,b.patch+1)
            return b<=v<upper
        if s.startswith('~'):
            b=Version.parse(s[1:]); return b<=v<Version(b.major,b.minor+1,0)
        if '*' in s:
            parts=s.split('.')
            if len(parts)==2 and parts[1]=='*':
                return v.major==int(parts[0])
            if len(parts)==3 and parts[2]=='*':
                return v.major==int(parts[0]) and v.minor==int(parts[1])
            raise PackageError(f'invalid wildcard requirement {s!r}','VERSION_INVALID')
        return v==Version.parse(s)
