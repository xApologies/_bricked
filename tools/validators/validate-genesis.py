"""Validate DP-007 registries and current navigation; no mathematical proof claims.

The standard-library schema evaluator supports exactly the JSON Schema keywords
used by the committed schemas and rejects unsupported keywords rather than skipping them.
"""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote
ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {'state': ('R5', [5], ['nexus']), 'nexus': ('H6', [6], ['state', 'shell']),
            'shell': ('Sigma7:8', [7, 8], ['nexus', 'sea']), 'sea': ('S9:11', [9, 10, 11], ['shell'])}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def schema_check(value, schema, location='$'):
    supported = {'$schema', 'type', 'required', 'properties', 'additionalProperties', 'const', 'enum', 'items', 'minItems', 'maxItems', 'uniqueItems', 'minLength', 'minProperties'}
    require(set(schema) <= supported, f'Unsupported schema keyword at {location}')
    if 'const' in schema: require(value == schema['const'], f'Constant mismatch: {location}')
    if 'enum' in schema: require(value in schema['enum'], f'Enum mismatch: {location}')
    types = {'object': dict, 'array': list, 'string': str, 'integer': int}
    if 'type' in schema: require(type(value) is types[schema['type']], f'Type mismatch: {location}')
    if isinstance(value, dict):
        require(set(schema.get('required', [])) <= set(value), f'Missing fields: {location}')
        require(len(value) >= schema.get('minProperties', 0), f'Too few properties: {location}')
        props = schema.get('properties', {})
        extra = schema.get('additionalProperties', True)
        for key, item in value.items():
            if key in props: schema_check(item, props[key], location + '.' + key)
            elif extra is False: raise ValueError(f'Unexpected field: {location}.{key}')
            elif isinstance(extra, dict): schema_check(item, extra, location + '.' + key)
    if isinstance(value, list):
        require(schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', float('inf')), f'Array length: {location}')
        if schema.get('uniqueItems'): require(len({json.dumps(x, sort_keys=True) for x in value}) == len(value), f'Duplicate item: {location}')
        for i, item in enumerate(value): schema_check(item, schema.get('items', {}), f'{location}[{i}]')
    if isinstance(value, str): require(len(value) >= schema.get('minLength', 0), f'Empty string: {location}')

def read(path): return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
def reference(path):
    require(not Path(path).is_absolute() and '\\' not in path, f'Not a portable repository-relative path: {path}')
    resolved = (ROOT / path).resolve()
    require(resolved.is_relative_to(ROOT) and resolved.exists(), f'Unresolved/escaping reference: {path}')
    return resolved

def validate_registry(reg):
    schema_check(reg, read('genesis/schemas/domain-registry.schema.json'))
    require(reg['topology'] == ['sea', 'shell', 'nexus', 'state'], 'Topology differs')
    require(reg['adjacency'] == [['sea', 'shell'], ['shell', 'nexus'], ['nexus', 'state']], 'Nonadjacent or missing edge')
    for key, (symbol, dimensions, adjacent) in EXPECTED.items():
        entry = reg['domains'][key]
        require(entry['symbol'] == symbol and entry['dimensions'] == dimensions, f'Identity mismatch: {key}')
        geometry = {'state': 'five-dimensional sphere', 'nexus': 'six-dimensional hypercube', 'shell': 'coupled shell', 'sea': 'coupled sea'}
        require(entry['geometry'] == geometry[key], f'Geometry mismatch: {key}')
        require(entry['path'] == 'genesis/domains/' + key and entry['manifest'] == entry['path'] + '/MANIFEST.json', f'Mount mismatch: {key}')
    return True

def validate():
    reg = read('genesis/registries/DOMAIN_REGISTRY.json')
    validate_registry(reg)
    require({p.name for p in (ROOT/'genesis/domains').iterdir() if p.is_dir()} == set(EXPECTED), 'Extra/missing physical domain')
    authority = read('genesis/registries/AUTHORITY_REGISTRY.json')
    cross = read('genesis/registries/CROSSCUTTING_REGISTRY.json')
    schema_check(authority, read('genesis/schemas/authority-registry.schema.json'))
    schema_check(cross, read('genesis/schemas/crosscutting-registry.schema.json'))
    expected_authorities = {'genesis_mathematics': 'genesis_mathematics', 'chirality_fabric': 'chirality_fabric', 'genesis_programming_language': 'language', 'structural_language': 'language/_lang', 'architecture': 'genesis', 'provenance': 'provenance', 'development': 'development'}
    require(set(expected_authorities) <= set(authority['authorities']), 'Missing required source authority')
    for key, path in expected_authorities.items(): require(authority['authorities'][key]['path'] == path, f'Authority mount drift: {key}')
    for a in authority['authorities'].values(): reference(a['path'])
    for a in cross['systems'].values():
        reference(a['path'])
        for path in a['authority_refs']: reference(path)
    for key, entry in reg['domains'].items():
        manifest = read(entry['manifest'])
        schema_check(manifest, read('genesis/schemas/domain-manifest.schema.json'))
        require(manifest['id'] == key and manifest['name'] == 'Genesis ' + key.title(), f'Manifest identity: {key}')
        for field in ['symbol', 'dimensions', 'geometry', 'role']: require(manifest[field] == entry[field], f'Manifest drift: {key}.{field}')
        require(manifest['adjacent_domains'] == EXPECTED[key][2], f'Manifest adjacency: {key}')
        require(set(manifest['crosscutting_systems']) == set(cross['systems']), f'Systems drift: {key}')
        for path in manifest['authority_refs'] + list(manifest['documents'].values()): reference(path)
        for name, path in manifest['documents'].items(): require(path == entry['path'] + '/' + name.upper() + '.md', f'Document mount: {key}')
    version = read('genesis/registries/SCHEMA_VERSION.json')
    require(version['version'] == '1.0.0' and version['path_base'] == 'repository_root' and set(version['domain_ids']) == set(EXPECTED), 'Schema version metadata')
    for path in version['schemas'].values(): reference(path)
    index = read('genesis/registries/LANGUAGE_INDEX.json')
    require(index['architectural_domain'] is False and [x['section'] for x in index['sections']] == list(range(1,21)), 'Language section index')
    for section in index['sections']:
        reference(section['path']); reference(section['entry'])
    docs = [ROOT/'README.md'] + list((ROOT/'genesis').rglob('*.md')) + list((ROOT/'docs/architecture').glob('*.md')) + list((ROOT/'docs/genesis').glob('*.md'))
    edges = {}; broken = []
    for doc in docs:
        text = doc.read_text(encoding='utf-8-sig'); edges[doc.resolve()] = []
        for target in re.findall(r'\]\(([^)\n]+)\)', text):
            if '://' in target or target.startswith('#'): continue
            target = unquote(target.split('#')[0].strip('<>'))
            dest = (doc.parent / target).resolve()
            if not dest.exists(): broken.append(f'{doc.relative_to(ROOT)} -> {target}')
            edges[doc.resolve()].append(dest)
    require(not broken, 'Broken current links: ' + '; '.join(broken))
    reachable = {ROOT/'README.md'}
    for _ in range(2): reachable |= {d for p in list(reachable) for d in edges.get(p, [])}
    require(all(ROOT/e['path']/'README.md' in reachable for e in reg['domains'].values()), 'Root navigation exceeds two hops')
    stale = (ROOT/'docs/architecture/GENESIS_STATE_NEXT.md').read_text()
    require('Status: SUPERSEDED' in stale and 'genesis/domains/state/DOMAIN.md' in stale, 'Stale current State planning authority')
    result = subprocess.run([sys.executable, '-B', str(ROOT/'tools/validators/crawl-genesis.py'), str(ROOT/'genesis/registries/DOMAIN_REGISTRY.json')], capture_output=True, text=True, check=True)
    discovered = json.loads(result.stdout)
    require(set(discovered) == set(EXPECTED), 'Crawler did not discover exactly four domains')
    print(f'PASS schemas, four manifests, references, adjacency, {len(docs)} current documents, two-hop navigation and registry-only crawler')

if __name__ == '__main__': validate()
