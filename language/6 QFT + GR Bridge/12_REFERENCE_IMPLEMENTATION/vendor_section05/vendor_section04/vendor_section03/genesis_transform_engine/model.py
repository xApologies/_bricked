from dataclasses import dataclass,field,asdict
from typing import Optional

@dataclass
class InvariantContract:
    name:str='STRICT_IDENTITY'
    preserve_canonical_mmo:bool=True
    preserve_fabric_region:bool=True
    preserve_identity_tags:bool=True
    preserve_occupancy:bool=False
    preserve_handedness:bool=False
    preserve_chi:bool=False
    preserve_sigma:bool=False
    preserve_rho:bool=False
    preserve_lambda:bool=False
    preserve_tau:bool=False
    preserve_adjacency:bool=False
    require_no_changes:bool=False

@dataclass
class TransformRequest:
    parent_instance:dict
    segment_chain:list
    capability_profile:str
    operators:list
    invariants:InvariantContract=field(default_factory=InvariantContract)
    identity_policy:str='PRESERVE_MMO'
    derived_mmo_id:Optional[str]=None
    derived_representation_id:Optional[str]=None
    expected_parent_root:Optional[str]=None
    metadata:dict=field(default_factory=dict)

@dataclass
class TransformPlan:
    plan_id:str
    parent_instance_id:str
    child_instance_id:str
    pre_state_root:str
    capability_profile:str
    effects:list
    operators:list
    invariants:dict
    identity_policy:str
    derived_mmo_id:Optional[str]=None
    derived_representation_id:Optional[str]=None

@dataclass
class TransformResult:
    child_instance:dict
    plan:dict
    receipt:dict
    delta_path:str
    changed_cells:int
    pre_state_root:str
    post_state_root:str
