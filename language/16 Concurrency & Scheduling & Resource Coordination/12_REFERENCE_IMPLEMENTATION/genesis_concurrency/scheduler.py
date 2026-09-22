from __future__ import annotations
from typing import Any
from .model import *
from .resource import ResourceManager
from .recursive_adapter import make_token,run_slice
from .verifier import verify
from .errors import ConcurrencyError
from .util import sha256_obj

TERMINAL={TaskState.CLOSED,TaskState.FAILED,TaskState.CANCELLED}

class DeterministicScheduler:
    def __init__(self, program:ConcurrentProgram, max_ticks:int=1_000_000):
        self.program=program; self.max_ticks=int(max_ticks); self.verification=verify(program)
        self.rm=ResourceManager(program.resources); self.tasks={}; self.handle_to_task={}; self.events=[]; self.tick=0; self._ready_seq=0; self._wait_seq=0; self._task_serial=0
        for s in program.spawns:self._spawn(s.template,s.handle)
    def _event(self,kind,task_id=None,**fields):
        e={'tick':self.tick,'kind':kind}
        if task_id is not None:e['task_id']=task_id
        e.update(fields); e['event_id']='evt-'+sha256_obj(e)[:24]; self.events.append(e); return e
    def _spawn(self,template,handle):
        self._task_serial+=1; tid=f'task-{self._task_serial:08d}-{handle}'; tt=self.program.templates[template]
        rec=None
        if tt.kind=='RECURSIVE':
            cfg=dict(tt.recursion or {}); rec=make_token(cfg.get('task_id',tid),cfg.get('state',0),cfg.get('delta',1),cfg.get('close_at'))
        tr=TaskRuntime(tid,template,tt.priority,tt.quantum,list(tt.ops),state=TaskState.READY,recursion=rec)
        self.tasks[tid]=tr; self.handle_to_task[handle]=tid; self._enqueue(tr); self._event('TASK_SPAWN',tid,template=template,handle=handle,priority=tt.priority,quantum=tt.quantum); return tid
    def _enqueue(self,t):
        if t.state in TERMINAL:return
        self._ready_seq+=1;t.ready_seq=self._ready_seq;t.state=TaskState.READY;t.waiting_resource=None
    def _ready(self):
        xs=[t for t in self.tasks.values() if t.state==TaskState.READY]
        return min(xs,key=lambda t:(-t.priority,t.ready_seq,t.task_id)) if xs else None
    def _wake_waiters(self,resource):
        rr=self.rm.resources[resource]
        for _,tid,mode,units in list(rr.waiters):
            t=self.tasks.get(tid)
            if not t or t.state!=TaskState.BLOCKED: continue
            if self.rm.can_acquire(tid,resource,mode,units):
                rr.waiters=[x for x in rr.waiters if x[1]!=tid]; self._enqueue(t); self._event('TASK_WAKE',tid,resource=resource); break
    def cancel(self,task_id,reason='CANCELLED_BY_HOST'):
        t=self.tasks[task_id]
        if t.state in TERMINAL:return False
        released=self.rm.release_all(task_id); t.state=TaskState.CANCELLED
        self._event('TASK_CANCEL',task_id,reason=reason,released=[x['lease_id'] for x in released])
        for x in released:self._wake_waiters(x['resource'])
        return True
    def _close(self,t):
        if t.leases: raise ConcurrencyError(f'{t.task_id}: cannot close with live leases','TASK_RESOURCE_LEAK_RUNTIME')
        payload={'task_id':t.task_id,'template':t.template,'local_steps':t.local_steps,'history_root':t.history_root,'tick':self.tick}
        payload['receipt_id']='task-close-'+sha256_obj(payload)[:32]; t.close_receipt=payload;t.state=TaskState.CLOSED
        self._event('TASK_CLOSE',t.task_id,receipt_id=payload['receipt_id'])
    def _step_op(self,t):
        if t.pc>=len(t.ops): raise ConcurrencyError(f'{t.task_id}: pc beyond task','TASK_PC')
        op=t.ops[t.pc]; t.local_steps+=1
        if op.op==Op.WORK:
            if t.work_remaining<=0:t.work_remaining=int(op.attrs['units'])
            t.work_remaining-=1; self._event('WORK',t.task_id,remaining=t.work_remaining,label=op.attrs.get('label'))
            t.history_root=sha256_obj({'history':t.history_root,'op':'WORK','remaining':t.work_remaining,'task':t.task_id})
            if t.work_remaining==0:t.pc+=1
            return 'CONTINUE'
        if op.op==Op.ACQUIRE:
            rn=op.attrs['resource'];mode=ClaimMode(op.attrs.get('mode','SHARED'));units=int(op.attrs.get('units',1))
            if mode is ClaimMode.EXCLUSIVE:units=self.program.resources[rn].capacity
            lease=self.rm.acquire(t.task_id,rn,mode,units)
            if lease is None:
                self._wait_seq+=1;t.wait_seq=self._wait_seq;t.state=TaskState.BLOCKED;t.waiting_resource=rn;self.rm.enqueue_waiter(t.task_id,rn,mode,units,t.wait_seq)
                self._event('RESOURCE_BLOCK',t.task_id,resource=rn,mode=mode.value,units=units);return 'BLOCK'
            t.leases[rn]=lease;t.pc+=1;self._event('RESOURCE_ACQUIRE',t.task_id,resource=rn,lease_id=lease['lease_id'],mode=lease['mode'],units=lease['units']);return 'CONTINUE'
        if op.op==Op.RELEASE:
            rn=op.attrs['resource'];lease=self.rm.release(t.task_id,rn);t.leases.pop(rn,None);t.pc+=1;self._event('RESOURCE_RELEASE',t.task_id,resource=rn,lease_id=lease['lease_id']);self._wake_waiters(rn);return 'CONTINUE'
        if op.op==Op.YIELD:
            t.pc+=1;self._event('TASK_YIELD',t.task_id);return 'YIELD'
        if op.op==Op.RECURSION_SLICE:
            if t.recursion is None:
                cfg=op.attrs.get('initial',{});t.recursion=make_token(cfg.get('task_id',t.task_id),cfg.get('state',0),cfg.get('delta',1),cfg.get('close_at'))
            r=run_slice(t.recursion,int(op.attrs['budget']));self._event('RECURSION_SLICE',t.task_id,status=r['status'],state=r['state'],steps_used=r['steps_used'])
            if r['status']=='CLOSED':t.recursion=None;t.pc+=1;return 'CONTINUE'
            t.recursion=r['continuation'];t.state=TaskState.SUSPENDED;return 'SUSPEND'
        if op.op==Op.ASSERT:
            value=bool(op.attrs.get('value',False));self._event('ASSERT',t.task_id,value=value)
            if not value:raise ConcurrencyError(f'{t.task_id}: assertion failed','TASK_ASSERT')
            t.pc+=1;return 'CONTINUE'
        if op.op==Op.TASK_CLOSE:
            t.pc+=1;self._close(t);return 'CLOSE'
        raise ConcurrencyError(f'unimplemented op {op.op}','CONCURRENCY_OPCODE')
    def _resume_suspended(self):
        # deterministic cooperative resumption: suspended recursion gets a new ready turn after every scheduling cycle
        xs=sorted([t for t in self.tasks.values() if t.state==TaskState.SUSPENDED],key=lambda t:(-t.priority,t.ready_seq,t.task_id))
        for t in xs:self._enqueue(t);self._event('TASK_RESUME_READY',t.task_id)
    def wait_for_graph(self):
        g={tid:set() for tid,t in self.tasks.items() if t.state==TaskState.BLOCKED}
        for tid in list(g):
            rn=self.tasks[tid].waiting_resource
            if rn:
                for holder in self.rm.holders(rn):
                    if holder!=tid:g[tid].add(holder)
        return g
    def deadlock_cycle(self):
        g=self.wait_for_graph();seen=set();stack=[];active=set()
        def dfs(n):
            seen.add(n);active.add(n);stack.append(n)
            for m in sorted(g.get(n,())):
                if m not in g:continue
                if m not in seen:
                    c=dfs(m)
                    if c:return c
                elif m in active:
                    i=stack.index(m);return stack[i:]+[m]
            stack.pop();active.remove(n);return None
        for n in sorted(g):
            if n not in seen:
                c=dfs(n)
                if c:return c
        return None
    def run(self):
        while True:
            if self.tick>=self.max_ticks: raise ConcurrencyError('scheduler tick budget exhausted','SCHEDULER_TICK_BUDGET')
            joined=[self.tasks[self.handle_to_task[h]] for h in self.program.joins]
            if joined and all(t.state in TERMINAL for t in joined):
                status='CLOSED' if all(t.state==TaskState.CLOSED for t in joined) else 'PARTIAL'
                return self._result(status)
            t=self._ready()
            if t is None:
                suspended=[x for x in self.tasks.values() if x.state==TaskState.SUSPENDED]
                if suspended:
                    self.tick+=1;self._resume_suspended();continue
                blocked=[x for x in self.tasks.values() if x.state==TaskState.BLOCKED]
                if blocked:
                    cyc=self.deadlock_cycle()
                    if cyc:
                        self._event('DEADLOCK',cycle=cyc);return self._result('DEADLOCK',{'cycle':cyc})
                    return self._result('BLOCKED')
                if all(x.state in TERMINAL for x in self.tasks.values()):return self._result('CLOSED' if all(x.state==TaskState.CLOSED for x in self.tasks.values()) else 'PARTIAL')
                raise ConcurrencyError('scheduler has no runnable state','SCHEDULER_STALLED')
            self.tick+=1;t.state=TaskState.RUNNING;self._event('TASK_DISPATCH',t.task_id,quantum=t.quantum,priority=t.priority)
            reason='QUANTUM'
            try:
                for _ in range(t.quantum):
                    if t.state!=TaskState.RUNNING:break
                    reason=self._step_op(t)
                    if reason in ('BLOCK','YIELD','SUSPEND','CLOSE'):break
            except Exception as e:
                released=self.rm.release_all(t.task_id);t.leases.clear();t.state=TaskState.FAILED
                self._event('TASK_FAIL',t.task_id,error=str(e),released=[x['lease_id'] for x in released])
                for x in released:self._wake_waiters(x['resource'])
                reason='FAIL'
            if t.state==TaskState.RUNNING:self._enqueue(t);self._event('TASK_REQUEUE',t.task_id,reason=reason)
    def _result(self,status,extra=None):
        task_view={tid:{'template':t.template,'state':t.state.value,'pc':t.pc,'local_steps':t.local_steps,'history_root':t.history_root,'leases':dict(t.leases),'close_receipt':t.close_receipt,'recursion':t.recursion} for tid,t in sorted(self.tasks.items())}
        receipt={'module':self.program.module,'status':status,'logical_ticks':self.tick,'event_root':sha256_obj(self.events),'resource_root':sha256_obj(self.rm.snapshot()),'task_root':sha256_obj(task_view),'proof_root':self.verification['proof_root'],'scheduler':'DETERMINISTIC_COOPERATIVE_V0_1'}
        if extra:receipt.update(extra)
        receipt['receipt_id']='gsched-'+sha256_obj(receipt)[:32]
        return ScheduleResult(status,task_view,list(self.events),receipt,self.tick)
