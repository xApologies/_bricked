from .util import digest_obj

def audit_road_receipt(receipt):
    findings=[]
    if receipt.get('status')!='CLOSED': findings.append('status_not_closed')
    prs=receipt.get('portal_receipts',[])
    if not prs: findings.append('no_portals')
    for i,p in enumerate(prs):
        if p.get('status')!='CLOSED': findings.append(f'portal_{i}_not_closed')
        if i and prs[i-1].get('destination_instance_id')!=p.get('source_instance_id'): findings.append(f'portal_{i}_lineage_break')
    if receipt.get('source_content_root')!=receipt.get('final_content_root'): findings.append('content_root_changed')
    if prs and receipt.get('source_content_root')!=prs[0].get('source_content_root'): findings.append('source_root_mismatch')
    if prs and receipt.get('final_content_root')!=prs[-1].get('destination_content_root'): findings.append('final_root_mismatch')
    calc=digest_obj({'portal_ids':[p.get('portal_id') for p in prs],'edges':[e for p in prs for e in p.get('corridor',{}).get('edge_ids',[])],'colors':[c for p in prs for c in p.get('corridor',{}).get('color_trajectory',[])],'chirality_class':receipt.get('chirality_class'),'sector':receipt.get('sector'),'source_root':receipt.get('source_content_root'),'final_root':receipt.get('final_content_root')})
    if calc!=receipt.get('transport_holonomy_witness'): findings.append('transport_holonomy_mismatch')
    return {'pass':not findings,'findings':findings}
