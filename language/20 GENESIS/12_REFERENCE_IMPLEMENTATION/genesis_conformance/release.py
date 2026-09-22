import json, hashlib, zipfile
from pathlib import Path
from .errors import ConformanceError

def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':')).encode()
def digest_obj(o): return hashlib.sha256(canonical(o)).hexdigest()
def sha256_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def load_json(p): return json.loads(Path(p).read_text())
def verify_release(d):
    if d.get('kind')!='GENESIS_V1_RELEASE_DESCRIPTOR' or d.get('version')!='1.0.0' or d.get('release_status')!='FROZEN':
        raise ConformanceError('V1_RELEASE_DESCRIPTOR_INVALID')
    x=dict(d); root=x.pop('release_root',None)
    if root!=digest_obj(x): raise ConformanceError('V1_RELEASE_ROOT_MISMATCH')
    if d.get('full_self_host') is not False: raise ConformanceError('V1_FALSE_FULL_SELF_HOST_CLAIM')
    if d.get('source_genesis_boundary')!='PRESERVED_DISTINCT_FROM_COMPUTATIONAL_GENESIS': raise ConformanceError('V1_SOURCE_COMPUTATIONAL_BOUNDARY_ERASED')
    if 'S0_STRUCTURAL_ZERO_VS_EXISTENCE_CONFLICT' not in d.get('known_unresolved_semantic_gates',[]): raise ConformanceError('V1_SEMANTIC_GATE_SILENTLY_RECONCILED')
    if d.get('blackglass_v3_status')!='READY_FOR_INTEGRATION_NOT_YET_MIGRATED': raise ConformanceError('V1_BLACKGLASS_MIGRATION_FALSE_CLAIM')
    return {'status':'PASS','release_root':root}
def verify_core_lock(d):
    if d.get('kind')!='GENESIS_V1_CORE_LOCK' or d.get('language_version')!='1.0.0': raise ConformanceError('V1_CORE_LOCK_INVALID')
    x=dict(d); root=x.pop('core_lock_root',None)
    if root!=digest_obj(x): raise ConformanceError('V1_CORE_LOCK_MISMATCH')
    secs=[e.get('section') for e in d.get('sections',[])]
    if secs!=list(range(1,20)): raise ConformanceError('V1_SECTION_MISSING')
    if any(e.get('core_crc')!='PASS' for e in d['sections']): raise ConformanceError('V1_CORE_PACKAGE_TAMPER')
    return {'status':'PASS','core_lock_root':root,'sections':19}
def verify_abi(d):
    if d.get('kind')!='GENESIS_V1_ABI_FREEZE' or d.get('version')!='1.0.0' or d.get('status')!='FROZEN': raise ConformanceError('V1_ABI_FREEZE_INVALID')
    x=dict(d); root=x.pop('abi_freeze_root',None)
    if root!=digest_obj(x) or len(d.get('contracts',[]))!=19: raise ConformanceError('V1_ABI_FREEZE_INVALID')
    return {'status':'PASS','abi_freeze_root':root}
def verify_format(d):
    if d.get('kind')!='GENESIS_V1_FORMAT_FREEZE' or d.get('version')!='1.0.0' or d.get('status')!='FROZEN': raise ConformanceError('V1_FORMAT_FREEZE_INVALID')
    x=dict(d); root=x.pop('format_freeze_root',None)
    if root!=digest_obj(x): raise ConformanceError('V1_FORMAT_FREEZE_INVALID')
    return {'status':'PASS','format_freeze_root':root}
def audit_supplied_cores(lock, root):
    root=Path(root); results=[]
    for e in lock['sections']:
        p=root/e['core_file']
        if not p.is_file(): raise ConformanceError(f"V1_SECTION_MISSING:{e['section']:02d}")
        if sha256_file(p)!=e['core_sha256']: raise ConformanceError(f"V1_CORE_PACKAGE_TAMPER:{e['section']:02d}")
        with zipfile.ZipFile(p) as z:
            bad=z.testzip()
        if bad is not None: raise ConformanceError(f"V1_CORE_PACKAGE_TAMPER:{e['section']:02d}:{bad}")
        results.append({'section':e['section'],'status':'PASS'})
    return results
