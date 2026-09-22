import hashlib, math
from .util import clip01
from vendor.genesis_chirality_machine.cell import ChiralityCell, q16
from vendor.genesis_chirality_machine.constants import RIGHT_PATTERN, LEFT_PATTERN

FLAG_ADAPTER_DEFAULT=0x0001
FLAG_RESOLUTION_TO_TAU=0x0002
FLAG_COMPONENT_CELL=0x0004
FLAG_CONTROL_CELL=0x0008

ROLE_CHI00='chi_00'; ROLE_CHI01='chi_01'; ROLE_CHI10='chi_10'; ROLE_CHI11='chi_11'; ROLE_CONTROL='control'

class Generic3p1p1Profile:
    name='MMO_3P1P1_DENSE_V1'
    roles=[ROLE_CHI00,ROLE_CHI01,ROLE_CHI10,ROLE_CHI11,ROLE_CONTROL]
    cells_per_voxel=5
    def __init__(self,resolution_to_tau=True): self.resolution_to_tau=resolution_to_tau
    def required_cells(self,bundle):
        x,y,z=bundle.grid_shape; return x*y*z*self.cells_per_voxel
    def encode_voxel(self,bundle,x,y,z,identity_seed):
        field=bundle.arrays['chirality_field_3p1p1']
        mat=field[x,y,z]
        scalar=bundle.arrays.get('chirality_scalar')
        sval=float(scalar[x,y,z]) if scalar is not None else float(mat[0,0]+mat[1,1]-mat[0,1]-mat[1,0])
        hand=1 if sval>1e-12 else -1 if sval<-1e-12 else 0
        pattern=RIGHT_PATTERN if hand>0 else LEFT_PATTERN if hand<0 else 0
        comp=LEFT_PATTERN if hand>0 else RIGHT_PATTERN if hand<0 else 0
        cells=[]
        for k,(a,b) in enumerate(((0,0),(0,1),(1,0),(1,1))):
            tag=int.from_bytes(hashlib.sha256(f'{identity_seed}:{x}:{y}:{z}:{k}'.encode()).digest()[:8],'big')
            cells.append(ChiralityCell(occupancy_pattern=pattern,complement_pattern=comp,handedness=hand,state_class=16+k,
                        chi=q16(clip01(float(mat[a,b]))),flags=FLAG_COMPONENT_CELL,identity_tag=tag))
        sigma=1.0; flags=FLAG_CONTROL_CELL|FLAG_ADAPTER_DEFAULT
        adm=bundle.arrays.get('admissibility')
        if adm is not None: sigma=clip01(float(adm[x,y,z])); flags &= ~FLAG_ADAPTER_DEFAULT
        rho=0.0; pers=bundle.arrays.get('persistence')
        if pers is not None: rho=clip01(float(pers[x,y,z]))
        tau=0.0; res=bundle.arrays.get('resolution')
        if self.resolution_to_tau and res is not None:
            tau=clip01(float(res[x,y,z])); flags |= FLAG_RESOLUTION_TO_TAU
        tag=int.from_bytes(hashlib.sha256(f'{identity_seed}:{x}:{y}:{z}:control'.encode()).digest()[:8],'big')
        cells.append(ChiralityCell(occupancy_pattern=pattern,complement_pattern=comp,handedness=hand,state_class=1,
                    sigma=q16(sigma),chi=q16(clip01(abs(sval))),rho=q16(rho),tau=q16(tau),flags=flags,identity_tag=tag))
        return cells

class ScalarChiralityProfile:
    name='MMO_SCALAR_CHIRALITY_DENSE_V1'; roles=['control']; cells_per_voxel=1
    def __init__(self, persistence_key=None, admissibility_key=None): self.persistence_key=persistence_key; self.admissibility_key=admissibility_key
    def required_cells(self,bundle):
        x,y,z=bundle.grid_shape; return x*y*z
    def encode_voxel(self,bundle,x,y,z,identity_seed):
        arr=bundle.arrays.get('chirality_scalar')
        if arr is None: arr=bundle.arrays.get('chirality_statecode')
        sval=float(arr[x,y,z]); hand=1 if sval>0 else -1 if sval<0 else 0
        pattern=RIGHT_PATTERN if hand>0 else LEFT_PATTERN if hand<0 else 0; comp=LEFT_PATTERN if hand>0 else RIGHT_PATTERN if hand<0 else 0
        sigma=1.0; flags=FLAG_CONTROL_CELL|FLAG_ADAPTER_DEFAULT
        if self.admissibility_key and self.admissibility_key in bundle.arrays:
            sigma=clip01(float(bundle.arrays[self.admissibility_key][x,y,z])); flags &= ~FLAG_ADAPTER_DEFAULT
        rho=0.0
        if self.persistence_key and self.persistence_key in bundle.arrays: rho=clip01(float(bundle.arrays[self.persistence_key][x,y,z]))
        tag=int.from_bytes(hashlib.sha256(f'{identity_seed}:{x}:{y}:{z}:control'.encode()).digest()[:8],'big')
        return [ChiralityCell(occupancy_pattern=pattern,complement_pattern=comp,handedness=hand,state_class=1,
                    sigma=q16(sigma),chi=q16(clip01(abs(sval))),rho=q16(rho),flags=flags,identity_tag=tag)]
