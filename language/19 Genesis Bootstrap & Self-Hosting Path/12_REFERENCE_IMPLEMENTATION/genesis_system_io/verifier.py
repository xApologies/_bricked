from __future__ import annotations
from .model import SystemProgram,Op,EndpointKind,EndpointMode
from .capabilities import REQUIRED,require,endpoint_read_cap
from .brane import BraneHostReference
from .errors import fail
from .util import digest_obj

def verify(p:SystemProgram)->dict:
    if p.version!="0.6.0": fail("SYSTEM_VERSION",p.version)
    regs:set[str]=set(); closed=False
    mounted:set[str]=set()
    for port in p.ports.values(): BraneHostReference.validate_manifest(port)
    for idx,ins in enumerate(p.instructions):
        if closed: fail("SYSTEM_AFTER_CLOSE",str(idx))
        op=ins.op; a=ins.attrs
        require(p.capabilities,REQUIRED[op])
        if op==Op.READ:
            ep=p.endpoints.get(a["endpoint"])
            if not ep: fail("SYSTEM_ENDPOINT_UNKNOWN",a["endpoint"])
            require(p.capabilities,endpoint_read_cap(ep.kind.value))
            if ep.mode not in (EndpointMode.READ,EndpointMode.READ_WRITE): fail("SYSTEM_ENDPOINT_MODE",ep.name)
            _bind(regs,a["out"])
        elif op==Op.WRITE_DERIVED:
            ep=_ep(p,a["endpoint"])
            if ep.kind!=EndpointKind.DERIVED or ep.mode!=EndpointMode.READ_WRITE: fail("SYSTEM_ENDPOINT_MODE",ep.name)
            _use(regs,a["src"])
        elif op==Op.APPEND_AUDIT:
            ep=_ep(p,a["endpoint"])
            if ep.kind!=EndpointKind.AUDIT or ep.mode!=EndpointMode.APPEND: fail("SYSTEM_ENDPOINT_MODE",ep.name)
            _use(regs,a["src"])
        elif op==Op.CAS_PUT: _use(regs,a["src"]); _bind(regs,a["out"])
        elif op==Op.CAS_GET: _use(regs,a["ref"]); _bind(regs,a["out"])
        elif op==Op.BRANE_MOUNT:
            if a["port"] not in p.ports: fail("BRANE_PORT_INVALID",a["port"])
            mounted.add(a["port"])
        elif op==Op.BRANE_REALIZE:
            if a["port"] not in mounted: fail("BRANE_PORT_NOT_MOUNTED",a["port"])
            port=p.ports[a["port"]]
            if a["capability"] not in port.capabilities: fail("BRANE_CAPABILITY_UNAVAILABLE",a["capability"])
            _use(regs,a["payload"]); _bind(regs,a["out"])
            if "Z" in a.get("m5",{}): fail("BRANE_Z_CALLER_OWNED")
        elif op==Op.BLACKGLASS_PROPOSE:
            ep=_ep(p,a["endpoint"])
            if ep.kind!=EndpointKind.BLACKGLASS or ep.mode!=EndpointMode.PROPOSE: fail("SYSTEM_ENDPOINT_MODE",ep.name)
            _use(regs,a["src"]); _bind(regs,a["out"])
        elif op==Op.BLACKGLASS_ADMIT:
            ep=_ep(p,a["endpoint"])
            if ep.kind!=EndpointKind.BLACKGLASS or ep.mode!=EndpointMode.PROPOSE: fail("SYSTEM_ENDPOINT_MODE",ep.name)
            _use(regs,a["proposal"]); _bind(regs,a["out"])
        elif op==Op.DEVICE_REQUEST:
            ep=_ep(p,a["endpoint"])
            if ep.kind!=EndpointKind.DEVICE or ep.mode!=EndpointMode.REQUEST: fail("SYSTEM_ENDPOINT_MODE",ep.name)
            if a.get("payload"): _use(regs,a["payload"])
            _bind(regs,a["out"])
        elif op==Op.ASSERT_EQ: _use(regs,a["left"]); _use(regs,a["right"])
        elif op==Op.SYS_CLOSE: closed=True
        else: fail("SYSTEM_OPCODE_UNKNOWN",str(op))
    if not closed: fail("SYSTEM_PROGRAM_UNCLOSED")
    proof={"module":p.module,"capabilities":sorted(p.capabilities),"registers":sorted(regs),"instruction_count":len(p.instructions)}
    proof["proof_root"]=digest_obj(proof); return proof

def _ep(p,n):
    if n not in p.endpoints: fail("SYSTEM_ENDPOINT_UNKNOWN",n)
    return p.endpoints[n]
def _use(regs,n):
    if n not in regs: fail("SYSTEM_REGISTER_UNDEFINED",n)
def _bind(regs,n):
    if n in regs: fail("SYSTEM_REGISTER_REDEFINED",n)
    regs.add(n)
