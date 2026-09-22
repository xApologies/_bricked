import json
from pathlib import Path
class Ledger:
    def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
    def append(self,obj):
        with self.path.open('a',encoding='utf-8') as f:f.write(json.dumps(obj,sort_keys=True,default=str)+'\n')
