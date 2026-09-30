"""Consumer smoke test: discover domain manifests from one registry, without text search."""
import json
from pathlib import Path
import sys

def discover(registry_path):
    registry_path = Path(registry_path).resolve()
    root = registry_path.parents[2]
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    result = {}
    for key, entry in registry['domains'].items():
        manifest_path = (root / entry['manifest']).resolve()
        if not manifest_path.is_relative_to(root):
            raise ValueError('Manifest escapes repository')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        result[key] = {field: manifest[field] for field in ['id', 'name', 'symbol', 'dimensions', 'adjacent_domains']}
    return result

if __name__ == '__main__':
    print(json.dumps(discover(sys.argv[1]), indent=2))
