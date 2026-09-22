import hashlib

FIELDS=('occupancy_pattern','complement_pattern','handedness','state_class','sigma','chi','rho','lambda_','tau','flags','adjacency_index','lineage_index','identity_tag')

def _enc(v):
    if isinstance(v,int): return int(v).to_bytes(16,'big',signed=True)
    return str(v).encode()

def residue_root(view,start,count,fields):
    h=hashlib.sha256(); fields=list(fields)
    full='__FULL_CELL__' in fields
    for ordinal,idx in enumerate(range(int(start),int(start)+int(count))):
        c=view.read_index(idx); h.update(ordinal.to_bytes(8,'big'))
        if full: h.update(c.pack())
        else:
            for f in fields:
                if f not in FIELDS: raise ValueError('unknown residue field '+f)
                h.update(f.encode()+b'\0'+_enc(getattr(c,f)))
    return h.hexdigest()

def characterize(view,inst):
    start,count=inst['region']['start'],inst['region']['count']
    full=residue_root(view,start,count,['__FULL_CELL__'])
    hands=set(); states=set(); minvals={'sigma':65535,'chi':65535,'rho':65535,'lambda_':65535,'tau':65535}; maxvals={k:0 for k in minvals}
    for idx in range(start,start+count):
        c=view.read_index(idx); hands.add(c.handedness); states.add(c.state_class)
        for k in minvals:
            v=getattr(c,k); minvals[k]=min(minvals[k],v); maxvals[k]=max(maxvals[k],v)
    return {'content_root':full,'handedness':sorted(hands),'state_classes':sorted(states),'min_q16':minvals,'max_q16':maxvals}
