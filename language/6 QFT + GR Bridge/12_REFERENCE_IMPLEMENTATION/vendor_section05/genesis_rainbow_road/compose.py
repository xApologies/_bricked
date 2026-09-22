from dataclasses import asdict
from .errors import RoadCompositionError

def compose_plans(a,b):
    if a.sector!=b.sector: raise RoadCompositionError('sector mismatch')
    if not a.waypoints or a.waypoints[-1]['domain_id']!=b.source_address['domain_id']: raise RoadCompositionError('endpoint mismatch')
    return {
      'kind':'COMPOSED_ROAD_PLAN',
      'sector':a.sector,
      'source_address':a.source_address,
      'waypoints':list(a.waypoints)+list(b.waypoints),
      'road_ids':[a.road_id,b.road_id],
      'portal_leg_count':len(a.leg_plans)+len(b.leg_plans),
      'rainbow_trajectory':list(a.rainbow_trajectory)+list(b.rainbow_trajectory),
    }
