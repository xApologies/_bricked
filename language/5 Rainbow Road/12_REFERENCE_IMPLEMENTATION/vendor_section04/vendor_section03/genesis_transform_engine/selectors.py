from .errors import SelectorError

def _shape(inst):
    b=inst.get('brane_m5',{})
    # Section02 manifest does not store grid shape directly; infer from plan metadata if attached, else region/cpv 32^3 fixtures.
    shape=inst.get('grid_shape') or b.get('I',{}).get('grid_shape')
    if shape: return tuple(shape)
    cpv=int(inst['cells_per_voxel']); vox=inst['region']['count']//cpv
    n=round(vox ** (1/3))
    if n*n*n==vox: return (n,n,n)
    raise SelectorError('grid_shape required for voxel_box selector')

def resolve_selector(inst,spec):
    typ=spec.get('type','all'); start=int(inst['region']['start']); count=int(inst['region']['count']); cpv=int(inst['cells_per_voxel'])
    roles=list(inst.get('roles',[])); end=start+count
    if typ=='all': return list(range(start,end))
    if typ=='range':
        a=int(spec.get('start',0)); b=int(spec.get('end',count))
        if a<0 or b<a or b>count: raise SelectorError('range outside region')
        return list(range(start+a,start+b))
    if typ=='role':
        role=spec['role']
        if role not in roles: raise SelectorError('unknown role')
        off=roles.index(role)
        return list(range(start+off,end,cpv))
    if typ=='voxel_box':
        xN,yN,zN=_shape(inst); x0,x1=spec.get('x',[0,xN]); y0,y1=spec.get('y',[0,yN]); z0,z1=spec.get('z',[0,zN])
        if not (0<=x0<=x1<=xN and 0<=y0<=y1<=yN and 0<=z0<=z1<=zN): raise SelectorError('voxel box')
        rs=spec.get('roles',roles)
        offs=[]
        for r in rs:
            if r not in roles: raise SelectorError('unknown role')
            offs.append(roles.index(r))
        out=[]
        for x in range(x0,x1):
          for y in range(y0,y1):
            for z in range(z0,z1):
              v=(x*yN*zN+y*zN+z); base=start+v*cpv
              out.extend(base+o for o in offs)
        return sorted(set(out))
    raise SelectorError('unknown selector type')
