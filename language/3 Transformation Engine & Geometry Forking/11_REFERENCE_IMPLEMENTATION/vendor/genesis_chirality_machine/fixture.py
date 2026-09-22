import random
from .cell import ChiralityCell, q16

def deterministic_cells(count, seed=430043):
    rng=random.Random(seed)
    cells=[]
    for i in range(count):
        hand=1 if i%2==0 else -1
        base=ChiralityCell.right if hand==1 else ChiralityCell.left
        sc=i%8
        cells.append(base(state_class=sc,
            sigma=q16(rng.random()), chi=q16(rng.random()), rho=q16(rng.random()),
            lambda_=q16(rng.random()), tau=q16(rng.random()),
            adjacency_index=i%65536, lineage_index=i//1024,
            identity_tag=((i*0x9E3779B97F4A7C15)&((1<<64)-1))))
    return cells
