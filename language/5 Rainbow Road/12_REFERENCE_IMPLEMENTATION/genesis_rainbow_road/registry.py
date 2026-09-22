from pathlib import Path
import json
from dataclasses import asdict

class RoadRegistry:
    def __init__(self,path=None): self.path=Path(path) if path else None; self.templates={}; self.plans={}; self.aliases={}
    def register_template(self,t):
        self.templates[t.template_id]=asdict(t)
        if t.alias:self.aliases[t.alias]=('template',t.template_id)
        self._flush(); return t.template_id
    def register_plan(self,p,alias=None):
        self.plans[p.road_id]=asdict(p)
        if alias:self.aliases[alias]=('plan',p.road_id)
        self._flush(); return p.road_id
    def resolve(self,key):
        if key in self.aliases:
            kind,i=self.aliases[key]; return (self.templates if kind=='template' else self.plans)[i]
        if key in self.templates:return self.templates[key]
        if key in self.plans:return self.plans[key]
        raise KeyError(key)
    def _flush(self):
        if self.path:
            self.path.parent.mkdir(parents=True,exist_ok=True); self.path.write_text(json.dumps({'templates':self.templates,'plans':self.plans,'aliases':self.aliases},indent=2,sort_keys=True),encoding='utf-8')
