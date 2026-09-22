from dataclasses import dataclass,field,asdict
from enum import Enum
from typing import Optional

class RoadState(str,Enum):
    DECLARED='DECLARED'; PREFLIGHTED='PREFLIGHTED'; BUS_RESERVED='BUS_RESERVED'; RUNNING='RUNNING'; LEG_CLOSED='LEG_CLOSED'; END_TO_END_AUDIT='END_TO_END_AUDIT'; CLOSED='CLOSED'; INHERITED='INHERITED'; FAILED='FAILED'; FAILED_PARTIAL='FAILED_PARTIAL'

@dataclass(frozen=True)
class RoadTemplate:
    template_id:str
    alias:Optional[str]
    source_domain:str
    waypoint_domains:tuple
    sector:str
    chirality_class:str='ANY'
    residue_class:str='ANY'
    resolution_required:float=0.0
    bandwidth_required:float=0.0
    capacity_units_required:int=1

@dataclass
class RainbowRoadRequest:
    source_instance:dict
    source_segment_chain:list
    source_address:object
    waypoints:list
    sector:str='GENERIC'
    preservation:object=None
    resolution_required:float=0.0
    bandwidth_required:float=0.0
    capacity_units_required:int=1
    chirality_class:str='ANY'
    residue_class:str='ANY'
    route_policy:str='LOWEST_COST'
    require_end_to_end_content_identity:bool=True
    road_name:Optional[str]=None
    metadata:dict=field(default_factory=dict)

@dataclass
class RoadLegPlan:
    index:int
    source_address:dict
    target_address:dict
    corridor:dict

@dataclass
class RainbowRoadPlan:
    road_id:str
    road_name:Optional[str]
    source_instance_id:str
    source_content_root:str
    source_residue_root:str
    source_address:dict
    waypoints:list
    sector:str
    chirality_class:str
    residue_class:str
    preservation:dict
    leg_plans:list
    hold_requirements:dict
    total_cost:float
    min_resolution:float
    min_bandwidth:float
    rainbow_trajectory:list
    transport_holonomy_witness:str
    lifecycle:list

@dataclass
class RainbowRoadResult:
    final_instance:dict
    plan:dict
    receipt:dict
    portal_results:list
