from pathlib import Path
import json,hashlib
from .util import stable_json,now_ns
class TransformationLedger:
    def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True); self.prev=self._last_hash()
    def _last_hash(self):
        if not self.path.exists(): return '0'*64
        last=None
        for line in self.path.read_text().splitlines():
            if line.strip(): last=json.loads(line)
        return last.get('entry_hash','0'*64) if last else '0'*64
    def append(self,receipt):
        body={'prev_hash':self.prev,'receipt':receipt,'timestamp_ns':now_ns()}; eh=hashlib.sha256(stable_json(body)).hexdigest(); body['entry_hash']=eh
        with self.path.open('a',encoding='utf-8') as f:f.write(json.dumps(body,sort_keys=True,separators=(',',':'))+'\n')
        self.prev=eh; return body
