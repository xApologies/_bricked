from __future__ import annotations
import io,json,zipfile
from pathlib import Path
from .util import sha256_bytes,canonical_json
from .errors import fail

FIXED=(1980,1,1,0,0,0)

def _zi(name):
    z=zipfile.ZipInfo(name,FIXED); z.compress_type=zipfile.ZIP_DEFLATED; z.external_attr=(0o644 & 0xFFFF)<<16; return z

def build_gboot(out:Path,files:dict[str,bytes])->dict:
    out=Path(out); payload=dict(files)
    manifest={k:{"sha256":sha256_bytes(v),"bytes":len(v)} for k,v in sorted(payload.items())}
    payload["BOOTSTRAP_MANIFEST.json"]=canonical_json({"kind":"GENESIS_GBOOT_MANIFEST","version":"0.1.0","files":manifest})
    with zipfile.ZipFile(out,"w") as z:
        for name,data in sorted(payload.items()): z.writestr(_zi(name),data)
    blob=out.read_bytes(); return {"path":str(out),"sha256":sha256_bytes(blob),"bytes":len(blob),"file_count":len(payload)}

def verify_gboot(path:Path)->dict:
    try:
        with zipfile.ZipFile(path,"r") as z:
            names=z.namelist(); man=json.loads(z.read("BOOTSTRAP_MANIFEST.json"))
            for name,meta in man["files"].items():
                data=z.read(name)
                if sha256_bytes(data)!=meta["sha256"] or len(data)!=meta["bytes"]: fail("BOOTSTRAP_IMAGE_TAMPER",name)
    except (zipfile.BadZipFile,KeyError,json.JSONDecodeError) as e: fail("BOOTSTRAP_IMAGE_TAMPER",str(e))
    return {"status":"PASS","sha256":sha256_bytes(Path(path).read_bytes()),"entries":len(names)}
