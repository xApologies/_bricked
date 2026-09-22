from __future__ import annotations
import re, json
from .model import *
from .parser import parse_source
from .util import normalize_type,type_kind,type_args,sha256_obj,split_top
from .errors import ControlError
from .verifier import verify

BASE_KIND_TO_OP={
'mount':'FABRIC_MOUNT','alloc':'FABRIC_ALLOC','instantiate':'GEO_INSTANTIATE','fork':'GEO_FORK','rel':'RELATE','admit':'ADMIT','transform':'TRANSFORM','inherit':'INHERIT','portal':'PORTAL_OPEN','transport':'PORTAL_TRANSPORT','portal_close':'PORTAL_CLOSE','road_begin':'ROAD_BEGIN','road_append':'ROAD_APPEND','road_close':'ROAD_CLOSE','bridge':'BRIDGE_SECTOR','q_prepare':'Q_PREPARE','q_superpose':'Q_SUPERPOSE','q_entangle':'Q_ENTANGLE','q_channel':'Q_CHANNEL','q_measure':'Q_MEASURE','lift':'BRANE_LIFT','seal':'PROVENANCE_SEAL','assert_closure':'ASSERT_CLOSURE','emit_receipt':'EMIT_RECEIPT'
}
BASE_RESULT={
'FABRIC_MOUNT':'FABRIC','FABRIC_ALLOC':'REGION','GEO_INSTANTIATE':'GEOMETRIC','GEO_FORK':'GEOMETRIC','RELATE':'RELATION','ADMIT':'ADMISSION','TRANSFORM':'GEOMETRIC','INHERIT':'RECEIPT','PORTAL_OPEN':'PORTAL','PORTAL_TRANSPORT':'GEOMETRIC','PORTAL_CLOSE':'RECEIPT','ROAD_BEGIN':'ROAD','ROAD_APPEND':'ROAD','ROAD_CLOSE':'RECEIPT','BRIDGE_SECTOR':'BRIDGE','Q_PREPARE':'QSTATE','Q_SUPERPOSE':'QSTATE','Q_ENTANGLE':'QSTATE','Q_CHANNEL':'QSTATE','Q_MEASURE':'QRESULT','BRANE_LIFT':'M5','PROVENANCE_SEAL':'RECEIPT','ASSERT_CLOSURE':'BOOL','EMIT_RECEIPT':'RECEIPT'
}

def _tag(t):
    k=type_kind(t)
    if k in TypeTag.__members__: return TypeTag[k]
    if k in ('OPTION','RESULT'): return TypeTag.VARIANT
    return TypeTag.RECORD if k not in ('ANY',) else TypeTag.ANY

def _compatible(req,act):
    r=normalize_type(req); a=normalize_type(act)
    if r in ('ANY','RESOURCE') or a=='ANY': return True
    if r==a: return True
    return type_kind(r)==type_kind(a) and ('<' not in r or r==a)

class Compiler:
    def __init__(self,ast):
        self.ast=ast; self.ins=[]; self.nextreg=0; self.exports=[]; self.top={}
        self.meta={'data_types':{k:{'kind':v.kind,'fields':v.fields,'variants':v.variants} for k,v in ast.declarations.items()}}
    def emit(self,op,out=None,args=(),attrs=None,typ=TypeTag.ANY,src=None):
        i=Instruction(Opcode[op] if isinstance(op,str) else op,out,tuple(args),attrs or {},src,typ)
        self.ins.append(i); return len(self.ins)-1
    def newreg(self):
        r=self.nextreg; self.nextreg+=1
        if r>=256: raise ControlError('register budget exceeded','REGISTER_BUDGET',self.ast.file,0)
        return r
    def resolve(self,name,scope,line):
        if name not in scope: raise ControlError(f'unknown identity {name}','IDENTITY_UNKNOWN',self.ast.file,line)
        return scope[name]
    def bind(self,name,typ,scope,line):
        if name in scope: raise ControlError(f'duplicate identity {name}','DUPLICATE_VALUE',self.ast.file,line)
        r=self.newreg(); scope[name]=(r,normalize_type(typ)); return r
    def data_decl(self,t):
        k=type_kind(t)
        if k=='OPTION':
            a=type_args(t); return ('enum',{'Some':a[0] if a else 'ANY','None':None})
        if k=='RESULT':
            a=type_args(t); return ('enum',{'Ok':a[0] if a else 'ANY','Err':a[1] if len(a)>1 else 'ANY'})
        d=None
        for name,cand in self.ast.declarations.items():
            if name.upper()==k: d=cand; break
        if d:return (d.kind,d.fields if d.kind=='record' else d.variants)
        return (None,None)
    def compile_expr(self,expr,declared,scope,line,outreg):
        e=expr.strip(); dt=normalize_type(declared)
        if e in ('true','false'):
            if not _compatible(dt,'BOOL'): raise ControlError('bool literal type mismatch','DATA_TYPE',self.ast.file,line)
            self.emit('CONST',outreg,attrs={'value':e=='true'},typ=TypeTag.BOOL,src=f'{self.ast.file}:{line}'); return 'BOOL'
        if re.fullmatch(r'-?\d+',e):
            if not _compatible(dt,'INT'): raise ControlError('int literal type mismatch','DATA_TYPE',self.ast.file,line)
            self.emit('CONST',outreg,attrs={'value':int(e)},typ=TypeTag.INT,src=f'{self.ast.file}:{line}'); return 'INT'
        if re.fullmatch(r'-?\d+\.\d+',e):
            if not _compatible(dt,'FLOAT'): raise ControlError('float literal type mismatch','DATA_TYPE',self.ast.file,line)
            self.emit('CONST',outreg,attrs={'value':float(e)},typ=TypeTag.FLOAT,src=f'{self.ast.file}:{line}'); return 'FLOAT'
        if len(e)>=2 and e[0]=='"' and e[-1]=='"':
            if not _compatible(dt,'TEXT'): raise ControlError('text literal type mismatch','DATA_TYPE',self.ast.file,line)
            self.emit('CONST',outreg,attrs={'value':json.loads(e)},typ=TypeTag.TEXT,src=f'{self.ast.file}:{line}'); return 'TEXT'
        m=re.fullmatch(r'move\s+([A-Za-z_][A-Za-z0-9_]*)',e)
        if m:
            r,t=self.resolve(m.group(1),scope,line)
            if not _compatible(dt,t): raise ControlError('move type mismatch','DATA_TYPE',self.ast.file,line)
            self.emit('MOVE',outreg,[r],typ=_tag(t),src=f'{self.ast.file}:{line}'); return t
        m=re.fullmatch(r'record\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{(.*)\}',e)
        if m:
            tn=m.group(1); kind,spec=self.data_decl(tn)
            if kind!='record': raise ControlError(f'{tn} is not a record','DATA_TYPE',self.ast.file,line)
            pairs={}
            for item in split_top(m.group(2)):
                if '=' not in item: raise ControlError('record constructor field','DATA_RECORD_FIELDS',self.ast.file,line)
                k,v=item.split('=',1); pairs[k.strip()]=v.strip()
            if set(pairs)!=set(spec): raise ControlError(f'record fields {sorted(pairs)} != {sorted(spec)}','DATA_RECORD_FIELDS',self.ast.file,line)
            args=[]; fields=[]
            for f,ft in spec.items():
                rr,rt=self.resolve(pairs[f],scope,line)
                if not _compatible(ft,rt): raise ControlError(f'field {f} expects {ft}, got {rt}','DATA_TYPE',self.ast.file,line)
                args.append(rr); fields.append(f)
            if type_kind(dt)!=tn.upper(): raise ControlError('record declared type mismatch','DATA_TYPE',self.ast.file,line)
            self.emit('DATA_RECORD',outreg,args,{'record_type':tn,'fields':fields},TypeTag.RECORD,f'{self.ast.file}:{line}'); return dt
        m=re.fullmatch(r'field\s+([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z_][A-Za-z0-9_]*)',e)
        if m:
            rr,rt=self.resolve(m.group(1),scope,line); kind,spec=self.data_decl(rt)
            if kind!='record' or m.group(2) not in spec: raise ControlError('unknown record field','DATA_RECORD_FIELDS',self.ast.file,line)
            ft=spec[m.group(2)]
            if not _compatible(dt,ft): raise ControlError('field result type mismatch','DATA_TYPE',self.ast.file,line)
            self.emit('DATA_FIELD',outreg,[rr],{'field':m.group(2)},_tag(ft),f'{self.ast.file}:{line}'); return ft
        m=re.fullmatch(r'variant\s+([A-Za-z_][A-Za-z0-9_]*)::([A-Za-z_][A-Za-z0-9_]*)(?:\s+([A-Za-z_][A-Za-z0-9_]*))?',e)
        if m:
            tn,tag,val=m.groups(); kind,spec=self.data_decl(tn)
            if kind!='enum' or tag not in spec: raise ControlError('unknown variant','DATA_VARIANT_TAG',self.ast.file,line)
            pt=spec[tag]; args=[]
            if pt is None and val is not None: raise ControlError('payload not allowed','DATA_VARIANT_PAYLOAD',self.ast.file,line)
            if pt is not None:
                if val is None: raise ControlError('payload required','DATA_VARIANT_PAYLOAD',self.ast.file,line)
                rr,rt=self.resolve(val,scope,line)
                if not _compatible(pt,rt): raise ControlError('variant payload type mismatch','DATA_TYPE',self.ast.file,line)
                args=[rr]
            if type_kind(dt)!=tn.upper(): raise ControlError('variant declared type mismatch','DATA_TYPE',self.ast.file,line)
            self.emit('DATA_VARIANT',outreg,args,{'variant_type':tn,'tag':tag},TypeTag.VARIANT,f'{self.ast.file}:{line}'); return dt
        for ctor,tag in [('some','Some'),('ok','Ok'),('err','Err')]:
            m=re.fullmatch(ctor+r'\s+([A-Za-z_][A-Za-z0-9_]*)',e)
            if m:
                kind,spec=self.data_decl(dt)
                if kind!='enum' or tag not in spec: raise ControlError(f'{ctor} incompatible with {dt}','DATA_TYPE',self.ast.file,line)
                rr,rt=self.resolve(m.group(1),scope,line); pt=spec[tag]
                if not _compatible(pt,rt): raise ControlError('constructor payload mismatch','DATA_TYPE',self.ast.file,line)
                self.emit('DATA_VARIANT',outreg,[rr],{'variant_type':dt,'tag':tag},TypeTag.VARIANT,f'{self.ast.file}:{line}'); return dt
        if e=='none':
            kind,spec=self.data_decl(dt)
            if kind!='enum' or 'None' not in spec: raise ControlError('none requires OPTION','DATA_TYPE',self.ast.file,line)
            self.emit('DATA_VARIANT',outreg,[],{'variant_type':dt,'tag':'None'},TypeTag.VARIANT,f'{self.ast.file}:{line}'); return dt
        m=re.fullmatch(r'(eq|and|or|add|sub|lt|le)\s+([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z_][A-Za-z0-9_]*)',e)
        if m:
            op,a,b=m.groups(); ar,at=self.resolve(a,scope,line); br,bt=self.resolve(b,scope,line)
            table={'eq':('DATA_EQ','BOOL'),'and':('BOOL_AND','BOOL'),'or':('BOOL_OR','BOOL'),'add':('INT_ADD','INT'),'sub':('INT_SUB','INT'),'lt':('INT_LT','BOOL'),'le':('INT_LE','BOOL')}
            opc,rt=table[op]
            if op in ('and','or') and (type_kind(at)!='BOOL' or type_kind(bt)!='BOOL'): raise ControlError('boolean operands required','DATA_TYPE',self.ast.file,line)
            if op in ('add','sub','lt','le') and (type_kind(at)!='INT' or type_kind(bt)!='INT'): raise ControlError('integer operands required','DATA_TYPE',self.ast.file,line)
            if op=='eq' and not _compatible(at,bt): raise ControlError('equality operands incompatible','DATA_TYPE',self.ast.file,line)
            if not _compatible(dt,rt): raise ControlError('operation result type mismatch','DATA_TYPE',self.ast.file,line)
            self.emit(opc,outreg,[ar,br],typ=_tag(rt),src=f'{self.ast.file}:{line}'); return rt
        m=re.fullmatch(r'not\s+([A-Za-z_][A-Za-z0-9_]*)',e)
        if m:
            rr,rt=self.resolve(m.group(1),scope,line)
            if type_kind(rt)!='BOOL' or not _compatible(dt,'BOOL'): raise ControlError('not requires BOOL','DATA_TYPE',self.ast.file,line)
            self.emit('BOOL_NOT',outreg,[rr],typ=TypeTag.BOOL,src=f'{self.ast.file}:{line}'); return 'BOOL'
        raise ControlError(f'unknown expression {e!r}','DATA_EXPR',self.ast.file,line)
    def compile_base(self,st,scope):
        from genesis_frontend.parser import parse_source as base_parse
        src=f'genesis 0.1.0\nmodule _s14 {{\n{st.text}\n}}\n'
        try: bast=base_parse(src,self.ast.file)
        except Exception as e: raise ControlError(str(e),'BASE_STATEMENT',self.ast.file,st.line)
        if len(bast.statements)!=1: raise ControlError('expected one base statement','BASE_STATEMENT',self.ast.file,st.line)
        b=bast.statements[0]; opn=BASE_KIND_TO_OP[b.kind]; args=[]
        for a in b.args: args.append(self.resolve(a,scope,st.line)[0])
        out=None; typ=normalize_type(b.declared_type or BASE_RESULT[opn])
        if b.out: out=self.bind(b.out,typ,scope,st.line)
        self.emit(opn,out,args,dict(b.attrs),_tag(typ),f'{self.ast.file}:{st.line}')
    def compile_block(self,body,scope,top=False):
        for st in body:
            if isinstance(st,LetStmt):
                r=self.bind(st.name,st.typ,scope,st.line); self.compile_expr(st.expr,st.typ,scope,st.line,r)
            elif isinstance(st,BaseStmt): self.compile_base(st,scope)
            elif isinstance(st,ExportStmt):
                if not top: raise ControlError('export inside control region','REGION_ESCAPE',self.ast.file,st.line)
                r,t=self.resolve(st.name,scope,st.line)
                if not _compatible(st.typ,t): raise ControlError('export type mismatch','DATA_TYPE',self.ast.file,st.line)
                self.exports.append(r)
            elif isinstance(st,RepeatStmt):
                if st.count>4096: raise ControlError('repeat count exceeds 4096','REPEAT_BOUND',self.ast.file,st.line)
                for _ in range(st.count): self.compile_block(st.body,dict(scope),False)
            elif isinstance(st,IfStmt):
                cr,ct=self.resolve(st.cond,scope,st.line)
                if type_kind(ct)!='BOOL': raise ControlError('if condition must be BOOL','DATA_TYPE',self.ast.file,st.line)
                bi=self.emit('BRANCH',None,[cr],{'true':-1,'false':-1},TypeTag.VOID,f'{self.ast.file}:{st.line}')
                true_pc=len(self.ins); self.compile_block(st.then_body,dict(scope),False)
                j=self.emit('JUMP',None,attrs={'target':-1},typ=TypeTag.VOID,src=f'{self.ast.file}:{st.line}')
                false_pc=len(self.ins); self.compile_block(st.else_body,dict(scope),False)
                end=len(self.ins)
                self.ins[bi]=Instruction(Opcode.BRANCH,None,(cr,),{'true':true_pc,'false':false_pc},self.ins[bi].source,TypeTag.VOID)
                self.ins[j]=Instruction(Opcode.JUMP,None,(),{'target':end},self.ins[j].source,TypeTag.VOID)
            elif isinstance(st,MatchStmt): self.compile_match(st,scope)
            else: raise ControlError(f'unknown AST node {type(st)}','CONTROL_INTERNAL',self.ast.file,getattr(st,'line',0))
    def compile_match(self,st,scope):
        vr,vt=self.resolve(st.value,scope,st.line); kind,spec=self.data_decl(vt)
        if kind!='enum': raise ControlError('match requires sum type','DATA_TYPE',self.ast.file,st.line)
        seen=set(); default=False
        for idx,c in enumerate(st.cases):
            if c.tag=='_':
                if default: raise ControlError('duplicate default case','MATCH_DUPLICATE_CASE',self.ast.file,c.line)
                default=True
                if idx != len(st.cases)-1:
                    raise ControlError('default match case must be last','MATCH_DEFAULT_ORDER',self.ast.file,c.line)
            else:
                if c.tag in seen: raise ControlError('duplicate match case','MATCH_DUPLICATE_CASE',self.ast.file,c.line)
                if c.tag not in spec: raise ControlError(f'unknown case {c.tag}','DATA_VARIANT_TAG',self.ast.file,c.line)
                seen.add(c.tag)
        if not default and seen!=set(spec): raise ControlError(f'nonexhaustive match, missing {sorted(set(spec)-seen)}','MATCH_NONEXHAUSTIVE',self.ast.file,st.line)

        end_jumps=[]
        def compile_case_body(c):
            cs=dict(scope)
            if c.binder:
                if c.tag=='_':
                    raise ControlError('default case cannot bind a payload','DATA_VARIANT_PAYLOAD',self.ast.file,c.line)
                pt=spec[c.tag]
                if pt is None: raise ControlError('binder on payloadless variant','DATA_VARIANT_PAYLOAD',self.ast.file,c.line)
                br=self.bind(c.binder,pt,cs,c.line)
                self.emit('DATA_PAYLOAD',br,[vr],{'expected_tag':c.tag},_tag(pt),f'{self.ast.file}:{c.line}')
            self.compile_block(c.body,cs,False)

        for idx,c in enumerate(st.cases):
            is_last = idx == len(st.cases)-1
            # After all earlier tests fail, an exhaustive final explicit case or final
            # default is guaranteed. Lower it directly rather than manufacturing an
            # impossible fallthrough path in the verifier.
            if is_last and (c.tag=='_' or (not default and seen==set(spec))):
                compile_case_body(c)
                continue

            tr=self.newreg()
            self.emit('DATA_IS',tr,[vr],{'tag':c.tag},TypeTag.BOOL,f'{self.ast.file}:{c.line}')
            bi=self.emit('BRANCH',None,[tr],{'true':-1,'false':-1},TypeTag.VOID,f'{self.ast.file}:{c.line}')
            body_pc=len(self.ins)
            compile_case_body(c)
            j=self.emit('JUMP',None,attrs={'target':-1},typ=TypeTag.VOID,src=f'{self.ast.file}:{c.line}')
            end_jumps.append(j)
            next_pc=len(self.ins)
            self.ins[bi]=Instruction(Opcode.BRANCH,None,(tr,),{'true':body_pc,'false':next_pc},self.ins[bi].source,TypeTag.VOID)

        end=len(self.ins)
        for j in end_jumps:
            self.ins[j]=Instruction(Opcode.JUMP,None,(),{'target':end},self.ins[j].source,TypeTag.VOID)
    def compile(self):
        self.compile_block(self.ast.body,self.top,True)
        self.emit('HALT',typ=TypeTag.VOID,src=f'{self.ast.file}:halt')
        p=Program(self.ast.module,'0.2.0',self.ins,self.exports,{'source_version':'0.3.0','section':'14','ast_hash':sha256_obj({'module':self.ast.module,'decls':self.meta['data_types']})})
        p.metadata['verification']=verify(p)
        return p

def compile_source(text,file='<memory>'):
    ast=parse_source(text,file)
    return ast,Compiler(ast).compile()
