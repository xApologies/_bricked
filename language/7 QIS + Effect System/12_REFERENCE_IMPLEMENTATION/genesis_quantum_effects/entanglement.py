import math
from .state import StateFactory,ampvec,rhomat
from .linalg import tensor_vec,density_from_state
from .errors import StateValidationError


def bell_pair(member_a,member_b,source_instance_id=None,canonical_mmo_id=None):
    s=1/math.sqrt(2)
    return StateFactory.pure(['00','01','10','11'],[s,0,0,s],source_instance_id,canonical_mmo_id,[member_a,member_b],{'relationship':'BELL_REFERENCE'})

def tensor_product(a,b,member_names=None):
    av,bv=ampvec(a),ampvec(b)
    basis=[f'{x}|{y}' for x in a.basis for y in b.basis]
    members=member_names or (list(a.members or [a.state_id])+list(b.members or [b.state_id]))
    return StateFactory.pure(basis,tensor_vec(av,bv),a.source_instance_id or b.source_instance_id,a.canonical_mmo_id or b.canonical_mmo_id,members,{'relationship':'TENSOR_PRODUCT'})

def reduced_two_level(state,which=0):
    if len(state.basis)!=4 or len(state.members)!=2: raise StateValidationError('reference reduction supports two 2-level members')
    v=ampvec(state)
    # basis order 00,01,10,11. partial trace over other member.
    if which==0:
        r00=abs(v[0])**2+abs(v[1])**2; r11=abs(v[2])**2+abs(v[3])**2; r01=v[0]*v[2].conjugate()+v[1]*v[3].conjugate()
    else:
        r00=abs(v[0])**2+abs(v[2])**2; r11=abs(v[1])**2+abs(v[3])**2; r01=v[0]*v[1].conjugate()+v[2]*v[3].conjugate()
    return [[r00,r01],[r01.conjugate(),r11]]

def is_entangled_reference(state,tol=1e-9):
    if len(state.members)!=2 or len(state.basis)!=4: return False
    red=reduced_two_level(state,0)
    purity=(red[0][0]*red[0][0]+red[0][1]*red[1][0]+red[1][0]*red[0][1]+red[1][1]*red[1][1]).real
    return purity < 1-tol
