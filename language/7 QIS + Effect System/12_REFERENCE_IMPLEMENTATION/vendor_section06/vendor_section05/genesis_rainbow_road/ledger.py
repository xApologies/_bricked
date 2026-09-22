from pathlib import Path
import json,hashlib
from .util import stable_json,now_ns

class RoadLedger:
    def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True); self.prev='0'*64
    def append(self,event):
        body={'prev_hash':self.prev,'event':event,'timestamp_ns':now_ns()}; h=hashlib.sha256(stable_json(body)).hexdigest(); body['entry_hash']=h; self.prev=h
        with self.path.open('a',encoding='utf-8') as f:f.write(json.dumps(body,sort_keys=True,separators=(',',':'))+'\n')
        return body
