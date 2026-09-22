from __future__ import annotations
from .model import *
from .errors import ConcurrencyError
from .util import sha256_obj

def verify(program: ConcurrentProgram):
    if program.version!='0.5.0': raise ConcurrencyError('unsupported concurrent program version','CONCURRENCY_VERSION')
    if not program.spawns: raise ConcurrencyError('program must spawn at least one task','CONCURRENCY_NO_TASKS')
    handles=set()
    for s in program.spawns:
        if s.template not in program.templates: raise ConcurrencyError(f'unknown task template {s.template}','TASK_TEMPLATE_UNKNOWN')
        if s.handle in handles: raise ConcurrencyError(f'duplicate spawn handle {s.handle}','TASK_HANDLE_DUPLICATE')
        handles.add(s.handle)
    for h in program.joins:
        if h not in handles: raise ConcurrencyError(f'join references unknown handle {h}','JOIN_UNKNOWN_HANDLE')
    for r in program.resources.values():
        if not 1<=int(r.capacity)<=1_000_000: raise ConcurrencyError(f'invalid capacity for {r.name}','RESOURCE_CAPACITY')
    for t in program.templates.values():
        if not -1024<=t.priority<=1024: raise ConcurrencyError(f'priority out of range for {t.name}','TASK_PRIORITY')
        if not 1<=t.quantum<=1024: raise ConcurrencyError(f'quantum out of range for {t.name}','TASK_QUANTUM')
        if not t.ops or t.ops[-1].op!=Op.TASK_CLOSE: raise ConcurrencyError(f'{t.name} must end with close','TASK_UNCLOSED')
        held=set()
        for op in t.ops:
            if op.op==Op.ACQUIRE:
                rn=op.attrs['resource']
                if rn not in program.resources: raise ConcurrencyError(f'{t.name}: unknown resource {rn}','RESOURCE_UNKNOWN')
                if rn in held: raise ConcurrencyError(f'{t.name}: duplicate acquire {rn}','RESOURCE_DOUBLE_ACQUIRE')
                mode=ClaimMode(op.attrs.get('mode','SHARED'))
                units=int(op.attrs.get('units',1))
                if mode is ClaimMode.EXCLUSIVE: units=program.resources[rn].capacity
                if units<1 or units>program.resources[rn].capacity: raise ConcurrencyError(f'{t.name}: invalid units for {rn}','RESOURCE_UNITS')
                held.add(rn)
            elif op.op==Op.RELEASE:
                rn=op.attrs['resource']
                if rn not in held: raise ConcurrencyError(f'{t.name}: release without acquire {rn}','RESOURCE_RELEASE_STATIC')
                held.remove(rn)
            elif op.op==Op.WORK:
                if int(op.attrs.get('units',0))<1: raise ConcurrencyError(f'{t.name}: work units must be positive','WORK_UNITS')
            elif op.op==Op.RECURSION_SLICE:
                if int(op.attrs.get('budget',0))<1: raise ConcurrencyError(f'{t.name}: recursion budget must be positive','RECURSION_SLICE_BUDGET')
        if held: raise ConcurrencyError(f'{t.name}: resource(s) remain open at close: {sorted(held)}','TASK_RESOURCE_LEAK_STATIC')
    summary={'module':program.module,'resources':sorted(program.resources),'templates':sorted(program.templates),'spawns':[(x.template,x.handle) for x in program.spawns],'joins':program.joins}
    return {'ok':True,'verifier':'CONCURRENCY_CFG_V0_1','proof_root':sha256_obj(summary)}
