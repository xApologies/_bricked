from dataclasses import dataclass,field
from enum import Enum
from typing import Optional

class Sector(str,Enum): QFT='QFT'; GR='GR'
class BridgeState(str,Enum): DECLARED='DECLARED'; CHARACTERIZED='CHARACTERIZED'; SOURCE_VIEW='SOURCE_VIEW'; TARGET_VIEW='TARGET_VIEW'; ANCESTRY_VERIFIED='ANCESTRY_VERIFIED'; CLOSED='CLOSED'; INHERITED='INHERITED'; FAILED='FAILED'
class MixedRoadState(str,Enum): DECLARED='DECLARED'; PREFLIGHTED='PREFLIGHTED'; BUS_RESERVED='BUS_RESERVED'; RUNNING='RUNNING'; ACTION_CLOSED='ACTION_CLOSED'; END_TO_END_AUDIT='END_TO_END_AUDIT'; CLOSED='CLOSED'; INHERITED='INHERITED'; FAILED='FAILED'; FAILED_PARTIAL='FAILED_PARTIAL'

@dataclass(frozen=True)
class BridgePreservation:
    preserve_canonical_mmo:bool=True
    preserve_representation_id:bool=True
    preserve_content_root:bool=True
    preserve_residue_root:bool=True
    preserve_source_segments:bool=True

@dataclass
class SectorRepresentation:
    representation_view_id:str
    sector:str
    source_instance_id:str
    canonical_mmo_id:str
    source_representation_id:str
    content_root:str
    residue_root:str
    fabric_witness_id:str
    address:dict
    projection_profile:str
    invariants:dict
    payload:dict
    physics_status:str='SOFTWARE_REFERENCE_READOUT'

@dataclass
class BridgeRequest:
    source_instance:dict
    source_segment_chain:list
    address:object
    source_sector:str
    target_sector:str
    preservation:BridgePreservation=field(default_factory=BridgePreservation)
    projection_profile_qft:str='QFT_REFERENCE_V0_1'
    projection_profile_gr:str='GR_REFERENCE_V0_1'
    metadata:dict=field(default_factory=dict)

@dataclass
class BridgePlan:
    bridge_id:str
    source_sector:str
    target_sector:str
    source_instance_id:str
    address:dict
    source_view:dict
    target_view:dict
    fabric_witness_id:str
    common_ancestry_relation_id:str
    preservation:dict
    lifecycle:list

@dataclass
class BridgeResult:
    instance:dict
    address:object
    source_view:dict
    target_view:dict
    plan:dict
    receipt:dict

@dataclass
class MixedSectorRoadRequest:
    source_instance:dict
    source_segment_chain:list
    source_address:object
    waypoints:list
    preservation:object
    bridge_preservation:BridgePreservation=field(default_factory=BridgePreservation)
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
class MixedActionPlan:
    index:int
    kind:str
    source_address:dict
    target_address:dict
    detail:dict

@dataclass
class MixedRoadPlan:
    road_id:str
    road_name:Optional[str]
    source_instance_id:str
    source_content_root:str
    source_residue_root:str
    source_address:dict
    waypoints:list
    actions:list
    hold_requirements:dict
    sector_trajectory:list
    rainbow_trajectory:list
    lifecycle:list

@dataclass
class MixedRoadResult:
    final_instance:dict
    final_address:object
    plan:dict
    receipt:dict
    action_results:list
