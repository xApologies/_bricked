from dataclasses import dataclass, field, asdict
from typing import Optional

@dataclass
class RepresentationBundle:
    canonical_mmo_id: str
    representation_id: str
    source_kind: str
    grid_shape: tuple
    arrays: dict
    source_hashes: dict
    source_manifest: dict = field(default_factory=dict)
    dependencies: list = field(default_factory=list)
    provenance: list = field(default_factory=list)

@dataclass(frozen=True)
class FabricRegion:
    start: int
    count: int
    alignment: int = 1
    guard_before: int = 0
    guard_after: int = 0
    @property
    def end(self): return self.start + self.count

@dataclass
class InstantiationPlan:
    plan_id: str
    instance_id: str
    canonical_mmo_id: str
    representation_id: str
    fabric_tag: int
    grid_shape: tuple
    mapping_profile: str
    roles: list
    cells_per_voxel: int
    required_cells: int
    region: Optional[FabricRegion] = None
    source_hashes: dict = field(default_factory=dict)
    defaults: list = field(default_factory=list)

@dataclass
class GeometricInstance:
    instance_id: str
    canonical_mmo_id: str
    representation_id: str
    fabric_tag: int
    region: FabricRegion
    mapping_profile: str
    roles: list
    cells_per_voxel: int
    segment_path: str
    segment_sha256: str
    state: str = 'COMMITTED'
    parent_instance_id: Optional[str] = None
    history: list = field(default_factory=list)
    provenance: list = field(default_factory=list)
    brane_m5: dict = field(default_factory=dict)
    def to_dict(self):
        d=asdict(self); d['region']=asdict(self.region); return d
