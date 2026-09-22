from pathlib import Path
import sys, tempfile, numpy as np
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'10_REFERENCE_IMPLEMENTATION'))
from vendor.genesis_chirality_machine.cell import ChiralityCell
from vendor.genesis_chirality_machine.image import FabricImageBuilder,FabricImage
from genesis_geometric_engine.model import RepresentationBundle
from genesis_geometric_engine.allocator import RegionAllocator
from genesis_geometric_engine.profiles import Generic3p1p1Profile
from genesis_geometric_engine.engine import InstantiationEngine

with tempfile.TemporaryDirectory() as td:
 p=Path(td); FabricImageBuilder.build(p/'fabric.gcf',[ChiralityCell.right() for _ in range(8192)]); f=FabricImage(p/'fabric.gcf')
 field=np.zeros((4,4,4,2,2),np.float32); field[...,0,0]=.2; field[...,1,1]=.8
 b=RepresentationBundle('demo:mmo','demo:mmo:3p1p1','synthetic',(4,4,4),{'chirality_field_3p1p1':field},{'field':'demo'})
 e=InstantiationEngine(f,RegionAllocator(f.cell_count),p/'segments'); plan,rid=e.plan(b,Generic3p1p1Profile()); inst,receipts=e.materialize(b,Generic3p1p1Profile(),plan,rid)
 print(inst.to_dict()); f.close()
