from __future__ import annotations
import shlex
from .model import *
from .errors import fail

def parse_source(text:str,source:str="<memory>")->SystemProgram:
    raw=[]
    for ln,line in enumerate(text.splitlines(),1):
        s=line.strip()
        if not s or s.startswith("#"): continue
        raw.append((ln,s))
    if not raw or not raw[0][1].startswith("genesis "): fail("SYSTEM_VERSION","missing")
    head=raw[0][1].split()
    if len(head)!=2: fail("SYSTEM_VERSION","malformed")
    version=head[1]
    if len(raw)<3 or not raw[1][1].startswith("module ") or not raw[1][1].endswith("{"): fail("SYSTEM_MODULE")
    module=raw[1][1][7:-1].strip()
    if not module: fail("SYSTEM_MODULE")
    if raw[-1][1]!="}": fail("SYSTEM_MODULE_CLOSE")
    caps=set(); endpoints={}; ports={}; ins=[]
    for ln,s in raw[2:-1]:
        try: t=shlex.split(s)
        except ValueError as e: fail("SYSTEM_PARSE",f"line {ln}: {e}")
        if not t: continue
        if t[0]=="capability" and len(t)==2:
            caps.add(t[1]); continue
        if t[0]=="endpoint" and len(t)==8 and t[2]=="kind" and t[4]=="mode" and t[6]=="root":
            try: ep=EndpointSpec(t[1],EndpointKind(t[3]),EndpointMode(t[5]),t[7])
            except Exception: fail("SYSTEM_ENDPOINT_DECL",f"line {ln}")
            if ep.name in endpoints: fail("SYSTEM_ENDPOINT_DUPLICATE",ep.name)
            endpoints[ep.name]=ep; continue
        if t[0]=="port":
            keys={}
            if len(t)<18 or (len(t)-2)%2: fail("BRANE_PORT_DECL",f"line {ln}")
            alias=t[1]; i=2
            while i<len(t):
                keys[t[i]]=t[i+1]; i+=2
            try:
                pm=PortManifest(
                    alias,keys["role"],keys["module"],keys["version"],int(keys["dimension"]),keys["contract"],
                    keys["canonical"],keys["rewrite"],tuple(x for x in keys["caps"].split(",") if x),
                    keys.get("chirality","declared"),keys.get("provenance","declared")
                )
            except Exception: fail("BRANE_PORT_DECL",f"line {ln}")
            if alias in ports: fail("BRANE_PORT_DUPLICATE",alias)
            ports[alias]=pm; continue
        ins.append(_parse_ins(t,source,ln))
    return SystemProgram(module,version,caps,endpoints,ports,ins,{"source":source})

def _parse_ins(t,source,ln):
    src=f"{source}:{ln}"
    if not t: fail("SYSTEM_PARSE",src)
    k=t[0]
    if k=="read" and len(t)==5 and t[3]=="as":
        return Instruction(Op.READ,{"endpoint":t[1],"path":t[2],"out":t[4]},src)
    if k=="write" and len(t)==5 and t[3]=="from":
        return Instruction(Op.WRITE_DERIVED,{"endpoint":t[1],"path":t[2],"src":t[4]},src)
    if k=="append" and len(t)==5 and t[3]=="from":
        return Instruction(Op.APPEND_AUDIT,{"endpoint":t[1],"path":t[2],"src":t[4]},src)
    if k=="cas_put" and len(t)==4 and t[2]=="as":
        return Instruction(Op.CAS_PUT,{"src":t[1],"out":t[3]},src)
    if k=="cas_get" and len(t)==4 and t[2]=="as":
        return Instruction(Op.CAS_GET,{"ref":t[1],"out":t[3]},src)
    if k=="mount" and len(t)==2:
        return Instruction(Op.BRANE_MOUNT,{"port":t[1]},src)
    if k=="realize" and len(t)==8 and t[2]=="capability" and t[4]=="payload" and t[6]=="as":
        return Instruction(Op.BRANE_REALIZE,{"port":t[1],"capability":t[3],"payload":t[5],"out":t[7]},src)
    if k=="propose" and len(t)==5 and t[3]=="as":
        return Instruction(Op.BLACKGLASS_PROPOSE,{"endpoint":t[1],"src":t[2],"out":t[4]},src)
    if k=="admit" and len(t)==5 and t[3]=="as":
        return Instruction(Op.BLACKGLASS_ADMIT,{"endpoint":t[1],"proposal":t[2],"out":t[4]},src)
    if k=="device" and len(t)==8 and t[2]=="target" and t[4]=="capability" and t[6]=="as":
        return Instruction(Op.DEVICE_REQUEST,{"endpoint":t[1],"device":t[3],"capability":t[5],"payload":None,"out":t[7]},src)
    if k=="device" and len(t)==10 and t[2]=="target" and t[4]=="capability" and t[6]=="payload" and t[8]=="as":
        return Instruction(Op.DEVICE_REQUEST,{"endpoint":t[1],"device":t[3],"capability":t[5],"payload":t[7],"out":t[9]},src)
    if k=="assert_eq" and len(t)==3:
        return Instruction(Op.ASSERT_EQ,{"left":t[1],"right":t[2]},src)
    if k=="close" and len(t)==1:
        return Instruction(Op.SYS_CLOSE,{},src)
    fail("SYSTEM_PARSE",src+" "+" ".join(t))
