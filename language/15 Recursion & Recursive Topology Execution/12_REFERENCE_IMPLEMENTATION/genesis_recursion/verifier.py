from __future__ import annotations
from .model import *
from .errors import VerifyError

def verify(program,max_states=200000):
    n=len(program.instructions)
    if not n: raise VerifyError('empty recursion program','VERIFY_EMPTY')
    ranges={'__main__':(program.main_start,n)}|{k:(f.start,f.end) for k,f in program.functions.items()}
    recursive_edges=0; returns=0; closures=0
    for name,(start,end) in ranges.items():
        if not (0<=start<end<=n): raise VerifyError(f'bad function range {name}','VERIFY_FUNCTION_RANGE')
        defined=set(range(len(program.functions[name].params))) if name!='__main__' else set()
        # SSA is verified linearly as a conservative check. Branch paths only consume pre-branch identities in compiler v0.1.
        for pc in range(start,end):
            ins=program.instructions[pc]
            for r in ins.args:
                if r not in defined: raise VerifyError(f'{name} pc {pc}: use before define r{r}','VERIFY_USE_BEFORE_DEFINE')
            if ins.out is not None:
                if ins.out in defined: raise VerifyError(f'{name} pc {pc}: redefine r{ins.out}','VERIFY_REDEFINE')
                if not 0<=ins.out<256: raise VerifyError('register out of range','VERIFY_REGISTER')
                defined.add(ins.out)
            if ins.op==Op.BRANCH:
                for k in ('true','false'):
                    t=ins.attrs.get(k)
                    if not isinstance(t,int) or not start<=t<=end: raise VerifyError('branch escapes function','VERIFY_TARGET')
            if ins.op==Op.JUMP:
                t=ins.attrs.get('target')
                if not isinstance(t,int) or not start<=t<=end: raise VerifyError('jump escapes function','VERIFY_TARGET')
            if ins.op==Op.RCALL:
                target=ins.attrs.get('function')
                if target not in program.functions: raise VerifyError('unknown call target','VERIFY_CALL_TARGET')
                tf=program.functions[target]
                if len(ins.args)!=len(tf.params): raise VerifyError('call arity','VERIFY_CALL_ARITY')
                if ins.attrs.get('recursive'):
                    recursive_edges+=1
                    if name!=target: raise VerifyError('recur target is not current function','VERIFY_RECUR_TARGET')
                    if tf.mode=='DECREASING' and not int(ins.attrs.get('measure_delta',0))<0: raise VerifyError('recursive measure not decreasing','VERIFY_RECUR_DECREASE')
                    if tf.mode=='VISIT_ONCE' and 'visit_arg_index' not in ins.attrs: raise VerifyError('visit recursion missing key','VERIFY_RECUR_VISIT')
            if ins.op==Op.RECURSION_CLOSE: closures+=1
            if ins.op==Op.RRETURN:
                returns+=1
                if pc==start or program.instructions[pc-1].op!=Op.RECURSION_CLOSE: raise VerifyError('return without immediate closure','RECURSION_RETURN_UNCLOSED')
        if name!='__main__':
            f=program.functions[name]
            if f.mode not in ('DECREASING','FUEL','VISIT_ONCE'): raise VerifyError('unguarded recursion mode','RECURSION_UNGUARDED')
            if f.mode in ('DECREASING','VISIT_ONCE') and not f.max_depth: raise VerifyError('recursive max depth required','VERIFY_RECUR_DEPTH')
            if f.mode=='FUEL' and not f.fuel: raise VerifyError('fuel required','VERIFY_RECUR_FUEL')
    return {'ok':True,'verifier':'RECURSIVE_CFG_V0_1','instructions':n,'functions':len(program.functions),'recursive_edges':recursive_edges,'returns':returns,'closures':closures}
