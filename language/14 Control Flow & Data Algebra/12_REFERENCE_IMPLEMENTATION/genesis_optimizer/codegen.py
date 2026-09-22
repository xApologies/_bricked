from dataclasses import dataclass
from .optimizer import optimize_gir
from .util import sha256_bytes, sha256_obj
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm import compile_gir,verify,encode,disassemble
from genesis_frontend.vendor.genesis_semantics.vendor.genesis_vm.model import Program,Instruction

@dataclass
class OptimizedArtifact:
    gir:dict; program:object; bytecode:bytes; optimization_receipt:dict; codegen_receipt:dict; analyses:dict

def codegen_gir(gir,level='O1',profile='audit',backend=None):
    if profile not in ('reference','audit','compact'): raise ValueError('unknown codegen profile '+profile)
    opt,orec,analyses=optimize_gir(gir,level,backend)
    p=compile_gir(opt)
    md=dict(p.metadata); md['section11']={'optimization_id':orec['optimization_id'],'level':level,'profile':profile,'optimized_gir_hash':orec['after_gir_hash']}
    ins=list(p.instructions)
    if profile=='compact':
        ins=[Instruction(i.op,i.out,i.args,i.attrs,None,i.result_type) for i in ins]
    p=Program(p.name,p.version,ins,p.exports,md)
    verify(p); bc=encode(p)
    pre={'kind':'GENESIS_CODEGEN_RECEIPT','version':'0.1.0','optimization_id':orec['optimization_id'],'profile':profile,'gvm_sha256':sha256_bytes(bc),'instruction_count':len(p.instructions),'source_labels':sum(i.source is not None for i in p.instructions)}
    crec=dict(pre); crec['codegen_id']='gcg-'+sha256_obj(pre)[:24]
    return OptimizedArtifact(opt,p,bc,orec,crec,analyses)
