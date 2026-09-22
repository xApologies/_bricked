from genesis_frontend.vendor.genesis_semantics.effects import effects_for_op
PURE_OPS={'NOP','CONST','MOVE','HASH'}
QUANTUM_OPS={'Q_PREPARE','Q_SUPERPOSE','Q_ENTANGLE','Q_CHANNEL','Q_MEASURE'}
PORTAL_ROAD_OPS={'PORTAL_OPEN','PORTAL_TRANSPORT','PORTAL_CLOSE','ROAD_BEGIN','ROAD_APPEND','ROAD_CLOSE'}
BRIDGE_OPS={'BRIDGE_SECTOR'}
PROVENANCE_OPS={'INHERIT','PORTAL_CLOSE','ROAD_CLOSE','BRIDGE_SECTOR','PROVENANCE_SEAL','EMIT_RECEIPT'}

def effects(op): return effects_for_op(op)
def pure(op): return op in PURE_OPS and not effects(op)
