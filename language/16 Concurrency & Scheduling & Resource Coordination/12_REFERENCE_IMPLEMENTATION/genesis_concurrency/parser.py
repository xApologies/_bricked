from __future__ import annotations
import re
from .model import *
from .errors import ConcurrencyError

_HDR=re.compile(r'^genesis\s+(\S+)$')
_MOD=re.compile(r'^module\s+([A-Za-z_][\w.]*)\s*\{$')
_RES=re.compile(r'^resource\s+([A-Za-z_]\w*)\s+capacity\s+(\d+)(?:\s+kind\s+([A-Za-z_]\w*))?$')
_TASK=re.compile(r'^task\s+([A-Za-z_]\w*)\s+priority\s+(-?\d+)\s+quantum\s+(\d+)\s*\{$')
_RTASK=re.compile(r'^recursive_task\s+([A-Za-z_]\w*)\s+priority\s+(-?\d+)\s+quantum\s+(\d+)\s+slice\s+(\d+)\s+state\s+(-?\d+)\s+delta\s+(-?\d+)\s+close_at\s+(-?\d+)\s*\{$')
_SPAWN=re.compile(r'^spawn\s+([A-Za-z_]\w*)\s+as\s+([A-Za-z_]\w*)$')
_JOIN=re.compile(r'^join\s+(.+)$')

def _clean(text):
    out=[]
    for n,raw in enumerate(text.splitlines(),1):
        s=raw.split('#',1)[0].strip()
        if s:out.append((n,s))
    return out

def parse_source(text:str,file='<memory>'):
    ls=_clean(text)
    if len(ls)<3:raise ConcurrencyError('source too short','CONCURRENCY_PARSE')
    m=_HDR.match(ls[0][1]);
    if not m or m.group(1)!='0.5.0':raise ConcurrencyError('expected genesis 0.5.0','CONCURRENCY_VERSION')
    mm=_MOD.match(ls[1][1]);
    if not mm:raise ConcurrencyError('expected module declaration','CONCURRENCY_PARSE')
    module=mm.group(1);resources={};templates={};spawns=[];joins=[];i=2
    while i<len(ls):
        ln,s=ls[i]
        if s=='}':break
        if (r:=_RES.match(s)):
            name=r.group(1)
            if name in resources:raise ConcurrencyError(f'duplicate resource {name}','RESOURCE_DUPLICATE')
            resources[name]=ResourceSpec(name,int(r.group(2)),(r.group(3) or 'FABRIC').upper());i+=1;continue
        tm=_TASK.match(s); rm=_RTASK.match(s)
        if tm or rm:
            if tm:name,pri,q=tm.group(1),int(tm.group(2)),int(tm.group(3));kind='STANDARD';rec=None
            else:
                name,pri,q=rm.group(1),int(rm.group(2)),int(rm.group(3));kind='RECURSIVE';rec={'task_id':name,'slice':int(rm.group(4)),'state':int(rm.group(5)),'delta':int(rm.group(6)),'close_at':int(rm.group(7))}
            if name in templates:raise ConcurrencyError(f'duplicate task {name}','TASK_TEMPLATE_DUPLICATE')
            i+=1;ops=[]
            while i<len(ls) and ls[i][1]!='}':
                lno,x=ls[i];p=x.split()
                if not p: i+=1; continue
                if p[0]=='work' and len(p)>=2:
                    attrs={'units':int(p[1])};
                    if len(p)>2:attrs['label']=' '.join(p[2:])
                    ops.append(TaskOp(Op.WORK,attrs,f'{file}:{lno}'))
                elif p[0]=='acquire' and len(p)>=3:
                    rn=p[1];mode=p[2].upper();attrs={'resource':rn,'mode':mode}
                    if mode=='SHARED':attrs['units']=int(p[3]) if len(p)>=4 else 1
                    ops.append(TaskOp(Op.ACQUIRE,attrs,f'{file}:{lno}'))
                elif p[0]=='release' and len(p)==2:ops.append(TaskOp(Op.RELEASE,{'resource':p[1]},f'{file}:{lno}'))
                elif p[0]=='yield' and len(p)==1:ops.append(TaskOp(Op.YIELD,{},f'{file}:{lno}'))
                elif p[0]=='recur_slice' and len(p)==2:ops.append(TaskOp(Op.RECURSION_SLICE,{'budget':int(p[1])},f'{file}:{lno}'))
                elif p[0]=='assert' and len(p)==2 and p[1] in ('true','false'):ops.append(TaskOp(Op.ASSERT,{'value':p[1]=='true'},f'{file}:{lno}'))
                elif p[0]=='close' and len(p)==1:ops.append(TaskOp(Op.TASK_CLOSE,{},f'{file}:{lno}'))
                else:raise ConcurrencyError(f'{file}:{lno}: unknown task statement {x}','CONCURRENCY_PARSE')
                i+=1
            if i>=len(ls) or ls[i][1]!='}':raise ConcurrencyError(f'{file}:{ln}: unterminated task {name}','CONCURRENCY_PARSE')
            if kind=='RECURSIVE' and not any(x.op==Op.RECURSION_SLICE for x in ops):
                ops.insert(0,TaskOp(Op.RECURSION_SLICE,{'budget':rec['slice']},f'{file}:{ln}'))
            templates[name]=TaskTemplate(name,pri,q,ops,kind,rec);i+=1;continue
        if (sp:=_SPAWN.match(s)):spawns.append(SpawnSpec(sp.group(1),sp.group(2)));i+=1;continue
        if (j:=_JOIN.match(s)):joins.extend(j.group(1).split());i+=1;continue
        if s=='export schedule':i+=1;continue
        raise ConcurrencyError(f'{file}:{ln}: unexpected {s}','CONCURRENCY_PARSE')
    return ConcurrentProgram(module,'0.5.0',resources,templates,spawns,joins,{'source_file':file})
