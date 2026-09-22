from collections import defaultdict
from .errors import LinkError, CapabilityError
from .typesys import parse_type, compatible, erase_type
from .checker import check_gir
from .capabilities import check_capabilities, reference_backend_capabilities
from .proofs import proof_ledger
from .model import LinkResult
from .util import sha256_obj, sha256_bytes
from .vendor.genesis_vm import compile_gir, verify, encode

SUPPORTED_VERSION='0.1.0'

def _module_order(modules):
    names={m['module'] for m in modules}; deps={m['module']:set() for m in modules}; rev=defaultdict(set)
    for m in modules:
        for i in m.get('imports',[]):
            src=i.get('from')
            if src not in names: raise LinkError(f'IMPORT_UNRESOLVED: module {m["module"]} imports missing module {src}')
            deps[m['module']].add(src); rev[src].add(m['module'])
    ready=sorted(n for n,d in deps.items() if not d); out=[]
    while ready:
        x=ready.pop(0); out.append(x)
        for y in sorted(rev[x]):
            deps[y].discard(x)
            if not deps[y] and y not in out and y not in ready: ready.append(y); ready.sort()
    if len(out)!=len(names): raise LinkError('MODULE_CYCLE: '+','.join(sorted(names-set(out))))
    return out

def _interfaces(modules):
    table={}; byname={}
    for m in modules:
        name=m.get('module')
        if not name or name in byname: raise LinkError(f'MODULE_DUPLICATE: {name}')
        if m.get('ir')!='GIR-MODULE': raise LinkError(f'MODULE_FORMAT: {name}')
        if m.get('version','0.1.0')!=SUPPORTED_VERSION: raise LinkError(f'MODULE_VERSION: {name}')
        byname[name]=m
        seen=set()
        for e in m.get('exports',[]):
            sym=e['symbol']
            if sym in seen: raise LinkError(f'SYMBOL_DUPLICATE: {name}::{sym}')
            seen.add(sym); table[(name,sym)]={'module':name,'symbol':sym,'value':e['value'],'type':parse_type(e.get('type','ANY'))}
    return byname,table

def _validate_imports(modules,table):
    for m in modules:
        locals_=set()
        for i in m.get('imports',[]):
            loc=i['local']
            if loc in locals_: raise LinkError(f'SYMBOL_DUPLICATE: import alias {m["module"]}:{loc}')
            locals_.add(loc)
            key=(i['from'],i['symbol'])
            if key not in table: raise LinkError(f'IMPORT_UNRESOLVED: {m["module"]} -> {i["from"]}::{i["symbol"]}')
            if not compatible(i.get('type','ANY'),table[key]['type']): raise LinkError(f'IMPORT_TYPE_MISMATCH: {m["module"]}:{loc} requires {i.get("type")}, export is {table[key]["type"]}')

def link_bundle(bundle,backend=None):
    if bundle.get('link')!='GENESIS-LINK': raise LinkError('LINK_FORMAT')
    modules=list(bundle.get('modules',[])); byname,table=_interfaces(modules); _validate_imports(modules,table); order=_module_order(modules)
    global_values={}; renamed_by_module={}; module_hashes={}; nodes=[]; edges=[]
    # Allocate global names for every local producer first so imports can resolve independent of file order.
    for name in sorted(byname):
        m=byname[name]; ren={}
        for n in m.get('gir',{}).get('nodes',[]):
            if n.get('out'): ren[n['out']]=f'%{name}::{n["out"].lstrip("%")}'
        renamed_by_module[name]=ren; module_hashes[name]=sha256_obj(m)
    for (name,sym),e in table.items():
        if e['value'] not in renamed_by_module[name]: raise LinkError(f'EXPORT_UNRESOLVED: {name}::{sym} -> {e["value"]}')
        global_values[(name,sym)]=renamed_by_module[name][e['value']]
    # Merge in dependency order.
    for name in order:
        m=byname[name]; ren=renamed_by_module[name]
        imports={i['local']:global_values[(i['from'],i['symbol'])] for i in m.get('imports',[])}
        def rv(v):
            if isinstance(v,str) and v.startswith('%'):
                if v in imports: return imports[v]
                if v in ren: return ren[v]
            return v
        for n0 in m.get('gir',{}).get('nodes',[]):
            n=dict(n0); n['id']=f'{name}::{n0["id"]}'; n['args']=[rv(x) for x in n0.get('args',[])]
            if n0.get('out'): n['out']=ren[n0['out']]
            attrs=dict(n0.get('attrs',{}))
            # rewrite explicitly value-shaped attrs used by semantic witnesses
            for k,v in list(attrs.items()):
                if isinstance(v,str) and v.startswith('%'): attrs[k]=rv(v)
            n['attrs']=attrs
            nodes.append(n)
        for e0 in m.get('gir',{}).get('edges',[]):
            e=dict(e0); e['from']=f'{name}::{e0["from"]}'; e['to']=f'{name}::{e0["to"]}'; edges.append(e)
        # Every import-to-local-use dependency is already encoded by data arguments after substitution.
    requested=bundle.get('exports',[]); exports=[]
    for ref in requested:
        if '::' not in ref: raise LinkError(f'EXPORT_UNRESOLVED: malformed bundle export {ref}')
        mn,sym=ref.split('::',1); key=(mn,sym)
        if key not in global_values: raise LinkError(f'EXPORT_UNRESOLVED: {ref}')
        exports.append(global_values[key])
    # Compute refined seed-free linked check and preserve refinements as metadata.
    gir={'ir':'GIR','version':'0.1.0','name':bundle.get('name','linked_program'),'nodes':nodes,'edges':edges,'exports':exports}
    check=check_gir(gir,export_values=exports)
    if not check.ok: raise LinkError('STATIC_CHECK_FAILED: '+ '; '.join(f'{d.code}:{d.message}' for d in check.diagnostics))
    gir['metadata']={'section09':{'module_order':order,'module_hashes':module_hashes,'refined_types':{k:str(v) for k,v in sorted(check.value_types.items())},'linker':'section09-v0.1.0'}}
    cap=check_capabilities(gir,backend or reference_backend_capabilities())
    if not cap['ok']: raise CapabilityError('CAPABILITY_FAILED: '+ '; '.join(x['code']+':'+x['message'] for x in cap['diagnostics']))
    program=compile_gir(gir); verify(program); bytecode=encode(program)
    pre_receipt={'kind':'GENESIS_LINK_RECEIPT','version':'0.1.0','name':gir['name'],'modules':order,'module_hashes':module_hashes,'gir_hash':sha256_obj(gir),'gvm_sha256':sha256_bytes(bytecode),'backend':(backend or reference_backend_capabilities()).get('backend_id'),'exports':exports}
    receipt=dict(pre_receipt); receipt['link_id']='glnk-'+sha256_obj(pre_receipt)[:24]
    proofs=proof_ledger(check,cap,len(modules),len(table),receipt)
    if any(x['status']!='PASS' for x in proofs): raise LinkError('PROOF_LEDGER_FAILED')
    receipt['proof_root']=sha256_obj(proofs)
    return LinkResult(gir,program,bytecode,receipt,proofs,check)
