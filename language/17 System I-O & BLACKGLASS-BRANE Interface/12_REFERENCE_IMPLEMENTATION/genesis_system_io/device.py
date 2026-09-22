from __future__ import annotations
from .errors import fail
from .util import digest_obj

class DeviceReference:
    def __init__(self,capabilities:dict[str,set[str]]|None=None):
        self.capabilities=capabilities or {"sensor":{"hearing.capture","vision.capture"},"speaker":{"speech.output"}}
        self.sequence=0
    def request(self,device:str,capability:str,payload_ref:str|None):
        if device not in self.capabilities or capability not in self.capabilities[device]: fail("DEVICE_CAPABILITY_UNAVAILABLE",f"{device}:{capability}")
        self.sequence+=1
        r={"device":device,"capability":capability,"payload_ref":payload_ref,"sequence":self.sequence,"status":"ACCEPTED"}
        r["request_root"]=digest_obj(r); return r
