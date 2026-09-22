import json
from pathlib import Path
from .harness import V1ConformanceHarness
root=Path(__file__).resolve().parents[2]
print(json.dumps(V1ConformanceHarness(root).run(),indent=2,sort_keys=True))
