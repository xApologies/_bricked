from __future__ import annotations
from .model import Op
from .errors import fail

REQUIRED = {
    Op.READ: None,
    Op.WRITE_DERIVED: "io.derived.write",
    Op.APPEND_AUDIT: "io.audit.append",
    Op.CAS_PUT: "cas.put",
    Op.CAS_GET: "cas.get",
    Op.BRANE_MOUNT: "brane.mount",
    Op.BRANE_REALIZE: "brane.realize",
    Op.BLACKGLASS_PROPOSE: "blackglass.commit.propose",
    Op.BLACKGLASS_ADMIT: "blackglass.commit.admit",
    Op.DEVICE_REQUEST: "device.request",
    Op.ASSERT_EQ: None,
    Op.SYS_CLOSE: None,
}

def endpoint_read_cap(kind: str) -> str:
    if kind == "SOURCE": return "io.source.read"
    if kind == "DERIVED": return "io.derived.read"
    fail("SYSTEM_ENDPOINT_MODE", f"{kind} is not readable")

def require(caps: set[str], cap: str|None):
    if cap and cap not in caps: fail("SYSTEM_CAPABILITY_MISSING", cap)
