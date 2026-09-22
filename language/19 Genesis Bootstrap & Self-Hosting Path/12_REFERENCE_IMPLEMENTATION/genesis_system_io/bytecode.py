from __future__ import annotations
import struct,json
from .model import *
from .util import canonical_json,sha256_bytes
from .errors import fail
from .verifier import verify
MAGIC=b"GIO1"

def _payload(p:SystemProgram):
    return {"module":p.module,"version":p.version,"capabilities":sorted(p.capabilities),"endpoints":{k:v.as_dict() for k,v in sorted(p.endpoints.items())},"ports":{k:v.as_dict() for k,v in sorted(p.ports.items())},"instructions":[i.as_dict() for i in p.instructions],"metadata":p.metadata}

def encode(p:SystemProgram)->bytes:
    verify(p); data=canonical_json(_payload(p)); h=bytes.fromhex(sha256_bytes(data)); return MAGIC+struct.pack(">I",len(data))+h+data

def decode(blob:bytes)->SystemProgram:
    if len(blob)<40 or blob[:4]!=MAGIC: fail("SYSTEM_BYTECODE_MAGIC")
    n=struct.unpack(">I",blob[4:8])[0]; h=blob[8:40]; data=blob[40:]
    if len(data)!=n or bytes.fromhex(sha256_bytes(data))!=h: fail("SYSTEM_BYTECODE_TAMPER")
    d=json.loads(data)
    eps={k:EndpointSpec(v["name"],EndpointKind(v["kind"]),EndpointMode(v["mode"]),v["root"]) for k,v in d["endpoints"].items()}
    ports={k:PortManifest(v["alias"],v["role"],v["module_id"],v["version"],v["internal_dimension"],v["contract_version"],v["canonical_state_policy"],v["rewrite_policy"],tuple(v["capabilities"]),v.get("chirality_model","declared"),v.get("provenance_model","declared")) for k,v in d["ports"].items()}
    ins=[Instruction(Op(x["op"]),x["attrs"],x.get("source")) for x in d["instructions"]]
    p=SystemProgram(d["module"],d["version"],set(d["capabilities"]),eps,ports,ins,d.get("metadata",{})); verify(p); return p
