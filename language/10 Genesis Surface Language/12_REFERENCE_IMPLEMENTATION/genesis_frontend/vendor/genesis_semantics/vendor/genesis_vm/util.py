import hashlib, json

def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def sha256_obj(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def short_id(prefix, obj):
    return f"{prefix}-{sha256_obj(obj)[:20]}"
