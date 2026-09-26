from pathlib import Path
import hashlib

HERE = Path(__file__).resolve().parent
OUT = HERE / "GENESIS_MANUSCRIPT_v3_0_MATHEMATICS_ONLY_20260828.zip"
parts = sorted(HERE.glob("GENESIS_v3_0_*.part"))

with OUT.open("wb") as w:
    for p in parts:
        with p.open("rb") as r:
            while True:
                block = r.read(1024*1024)
                if not block:
                    break
                w.write(block)

h = hashlib.sha256()
with OUT.open("rb") as f:
    for block in iter(lambda: f.read(1024*1024), b""):
        h.update(block)

print("Reassembled:", OUT)
print("SHA-256:", h.hexdigest())
print("Expected:", "8b9a92ac56ab71ece3880e47ef6f8d47bc6a69beaab7e67994ed87b36f330209")
print("Match:", h.hexdigest() == "8b9a92ac56ab71ece3880e47ef6f8d47bc6a69beaab7e67994ed87b36f330209")
