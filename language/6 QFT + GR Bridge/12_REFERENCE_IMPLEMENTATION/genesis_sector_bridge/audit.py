def audit_bridge_receipt(r):
    f=[]
    if r.get('status')!='CLOSED': f.append('status')
    if r.get('source_sector')==r.get('target_sector'): f.append('sector_change')
    if {r.get('source_sector'),r.get('target_sector')}!={'QFT','GR'}: f.append('sector_pair')
    if r.get('source_content_root')!=r.get('target_content_root'): f.append('content_root')
    if r.get('source_residue_root')!=r.get('target_residue_root'): f.append('residue_root')
    if not r.get('common_ancestry',{}).get('admitted'): f.append('common_ancestry')
    if r.get('fabric_witness_id')!=r.get('common_ancestry',{}).get('fabric_witness_id'): f.append('fabric_witness')
    if r.get('physics_status')!='SOFTWARE_REFERENCE_TRANSDUCTION': f.append('physics_status')
    return {'pass':not f,'findings':f}

def audit_mixed_road_receipt(r):
    f=[]
    if r.get('status')!='CLOSED':f.append('status')
    if r.get('source_content_root')!=r.get('final_content_root'):f.append('content_root')
    if not r.get('actions'):f.append('actions')
    if len(r.get('action_receipts',[]))!=len(r.get('actions',[])):f.append('action_count')
    for x in r.get('bridge_receipts',[]):
        if not audit_bridge_receipt(x)['pass']: f.append('bridge_receipt')
    return {'pass':not f,'findings':f}
