from .util import sha256_obj
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import compile_gir,VM

def _export_hashes(res): return [{'type':v.type.value,'hash':sha256_obj(v.value)} for v in res.exports.values()]

def compare_execution(original_gir,optimized_artifact):
    r0=VM().run(compile_gir(original_gir)); r1=VM().run(optimized_artifact.program)
    e0=_export_hashes(r0); e1=_export_hashes(r1)
    pre={'kind':'GENESIS_OPT_EQUIVALENCE','version':'0.1.0','exports_equal':e0==e1,'original_exports':e0,'optimized_exports':e1,'original_ledger_root':r0.receipt.get('ledger_root'),'optimized_ledger_root':r1.receipt.get('ledger_root')}
    pre['ledger_equal']=pre['original_ledger_root']==pre['optimized_ledger_root']
    pre['status']='PASS' if pre['exports_equal'] and pre['ledger_equal'] else 'FAIL'
    return pre
