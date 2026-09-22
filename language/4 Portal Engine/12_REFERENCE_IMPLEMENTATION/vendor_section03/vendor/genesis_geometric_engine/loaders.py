import io, json, zipfile, hashlib, re
import numpy as np
from .model import RepresentationBundle
from .errors import SourceFormatError

def _hash(b): return hashlib.sha256(b).hexdigest()
def _npy(zf,name): return np.load(io.BytesIO(zf.read(name)), allow_pickle=False)

def load_mmo_source(path, model_id=None):
    path=str(path)
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        # Virus / 3+1+1 package
        hits=[n for n in names if n.endswith('chirality_field_3p1p1_32x32x32x2x2.npy') and (model_id is None or model_id in n)]
        if hits:
            field_name=hits[0]; prefix=field_name.rsplit('/',1)[0]+'/'
            manifest_name=prefix+'manifest.json'; manifest=json.loads(z.read(manifest_name)) if manifest_name in names else {}
            cid=manifest.get('model_id') or prefix.rstrip('/').split('/')[-1]
            arrays={'chirality_field_3p1p1':_npy(z,field_name)}; hashes={field_name:_hash(z.read(field_name)),manifest_name:_hash(z.read(manifest_name)) if manifest_name in names else None}
            mapping={
              'chirality_scalar':'chirality_scalar_32x32x32.npy','chirality_statecode':'chirality_statecode_32x32x32.npy',
              'occupancy':'occupancy_32x32x32.npy','persistence':'persistence_32x32x32.npy','resolution':'resolution_32x32x32.npy','mass_density':'mass_density_32x32x32.npy'}
            for k,s in mapping.items():
                n=prefix+s
                if n in names: arrays[k]=_npy(z,n); hashes[n]=_hash(z.read(n))
            return RepresentationBundle(cid,cid+':3p1p1','HSV1_V028' if 'HSV1' in cid else 'GENERIC_3P1P1',tuple(arrays['chirality_field_3p1p1'].shape[:3]),arrays,hashes,manifest)
        # Hydrogen v2
        if 'hydrogen_v2_chirality_field.npy' in names:
            manifest=json.loads(z.read('hydrogen_v2_manifest.json'))
            mapping={'chirality_scalar':'hydrogen_v2_chirality_field.npy','admissibility':'hydrogen_v2_environment_admissibility.npy',
                     'closure_topology':'hydrogen_v2_closure_topology.npy','pair_closure':'hydrogen_v2_pair_closure_topology.npy',
                     'mixed_closure':'hydrogen_v2_mixed_closure_admissibility.npy','polarization_shell':'hydrogen_v2_polarization_shell.npy',
                     'redistribution_resistance':'hydrogen_v2_redistribution_resistance.npy'}
            arrays={}; hashes={}
            for k,n in mapping.items():
                if n in names: arrays[k]=_npy(z,n); hashes[n]=_hash(z.read(n))
            return RepresentationBundle('H:HYDROGEN_V2','H:HYDROGEN_V2:scalar','HYDROGEN_V2',tuple(arrays['chirality_scalar'].shape),arrays,hashes,manifest)
        # Oxygen phase 5
        oh=[n for n in names if n.endswith('oxygen_phase5_chirality.npy')]
        if oh:
            n=oh[0]; prefix=n.rsplit('/',1)[0]+'/'; manifest=json.loads(z.read(prefix+'manifest.json'))
            arr=_npy(z,n)
            return RepresentationBundle('O:OXYGEN_PHASE5_V1','O:OXYGEN_PHASE5_V1:scalar','OXYGEN_PHASE5_V1',tuple(arr.shape),{'chirality_scalar':arr},{n:_hash(z.read(n)),prefix+'manifest.json':_hash(z.read(prefix+'manifest.json'))},manifest)
        # blank
        bh=[n for n in names if n.endswith('chirality_statecode_32x32x32.npy') and 'Blank' in n]
        if bh:
            n=bh[0]; prefix=n.rsplit('/',1)[0]+'/'; manifest=json.loads(z.read(prefix+'manifest.json')); arr=_npy(z,n)
            return RepresentationBundle('BLANK_MANIFOLD_V0_1','BLANK_MANIFOLD_V0_1:statecode','BLANK_MANIFOLD_V0_1',tuple(arr.shape),{'chirality_statecode':arr},{n:_hash(z.read(n)),prefix+'manifest.json':_hash(z.read(prefix+'manifest.json'))},manifest)
    raise SourceFormatError('unsupported MMO source package')
