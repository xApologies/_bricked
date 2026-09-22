from dataclasses import dataclass,field,asdict
from enum import Enum
from typing import Optional

class PortalSector(str,Enum):
    GENERIC='GENERIC'; QFT='QFT'; GR='GR'
class PortalState(str,Enum):
    DECLARED='DECLARED'; VALIDATED='VALIDATED'; CAPACITY_RESERVED='CAPACITY_RESERVED'; DESTINATION_RESERVED='DESTINATION_RESERVED'; OPEN='OPEN'; TRANSFERRING='TRANSFERRING'; ARRIVED='ARRIVED'; CLOSED='CLOSED'; INHERITED='INHERITED'; FAILED='FAILED'
class TransportMode(str,Enum): RE_REALIZE='RE_REALIZE'

@dataclass(frozen=True)
class PortalAddress:
    domain_id:str
    boundary_id:str='default'
    logical_location:str='root'
    sector:str='GENERIC'
    recursive_order:int=0
    fabric_tag:Optional[int]=None

@dataclass
class PreservationContract:
    fields:list=field(default_factory=lambda:['__FULL_CELL__'])
    preserve_canonical_mmo:bool=True
    preserve_representation:bool=True
    preserve_source:bool=True

@dataclass(frozen=True)
class CorridorEdge:
    edge_id:str
    source_domain:str
    target_domain:str
    sectors:tuple=('GENERIC',)
    chirality_classes:tuple=('ANY',)
    residue_classes:tuple=('ANY',)
    resolution:float=1.0
    bandwidth:float=1.0
    capacity_units:int=1
    cost:float=1.0
    color_index:str='UNSPECIFIED'
    closure_supported:bool=True
    bridge:bool=False

@dataclass
class CorridorPath:
    path_id:str
    domains:list
    edge_ids:list
    total_cost:float
    min_resolution:float
    min_bandwidth:float
    chirality_trajectory:list
    color_trajectory:list
    sector:str

@dataclass
class PortalRequest:
    source_instance:dict
    source_segment_chain:list
    source_address:PortalAddress
    target_address:PortalAddress
    sector:str='GENERIC'
    transport_mode:str='RE_REALIZE'
    preservation:PreservationContract=field(default_factory=PreservationContract)
    resolution_required:float=0.0
    bandwidth_required:float=0.0
    capacity_units_required:int=1
    chirality_class:str='ANY'
    residue_class:str='ANY'
    route_policy:str='LOWEST_COST'
    closure_target:str='TARGET_ADDRESS'
    expected_source_content_root:Optional[str]=None
    metadata:dict=field(default_factory=dict)

@dataclass
class PortalPlan:
    portal_id:str
    source_instance_id:str
    destination_instance_id:str
    source_address:dict
    target_address:dict
    sector:str
    transport_mode:str
    source_content_root:str
    source_residue_root:str
    corridor:dict
    route_reservation_id:str
    destination_reservation_id:str
    destination_region:dict
    preservation:dict
    lifecycle:list

@dataclass
class PortalResult:
    destination_instance:dict
    plan:dict
    receipt:dict
    destination_segment_path:str
