from .util import digest_obj
from .errors import CommonAncestryMismatch

def common_ancestry(q,g):
    if {q.sector,g.sector}!={'QFT','GR'}: raise CommonAncestryMismatch('R_QG requires QFT and GR views')
    if q.fabric_witness_id!=g.fabric_witness_id: raise CommonAncestryMismatch('fabric witness mismatch')
    if q.canonical_mmo_id!=g.canonical_mmo_id: raise CommonAncestryMismatch('MMO identity mismatch')
    if q.content_root!=g.content_root: raise CommonAncestryMismatch('content root mismatch')
    if q.residue_root!=g.residue_root: raise CommonAncestryMismatch('residue root mismatch')
    relation_id=digest_obj({'relation':'R_QG','q':q.representation_view_id,'g':g.representation_view_id,'fabric_witness_id':q.fabric_witness_id})
    return {'kind':'R_QG_COMMON_ANCESTRY','relation_id':relation_id,'admitted':True,'fabric_witness_id':q.fabric_witness_id,'qft_view_id':q.representation_view_id if q.sector=='QFT' else g.representation_view_id,'gr_view_id':g.representation_view_id if g.sector=='GR' else q.representation_view_id,'canonical_mmo_id':q.canonical_mmo_id,'content_root':q.content_root,'residue_root':q.residue_root}
