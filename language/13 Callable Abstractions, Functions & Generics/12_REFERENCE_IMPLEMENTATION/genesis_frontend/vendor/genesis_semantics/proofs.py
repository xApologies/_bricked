def proof_ledger(check,cap,module_count,symbol_count,link_receipt=None):
    d=check.as_dict()
    codes={x['code'] for x in d['diagnostics']}
    def stat(blockers): return 'FAIL' if codes & set(blockers) else 'PASS'
    out=[
      {'id':'PO-SYMBOL-RESOLUTION','status':stat({'IMPORT_UNRESOLVED','EXPORT_UNRESOLVED','SYMBOL_DUPLICATE','MODULE_CYCLE'}),'witness':{'modules':module_count,'symbols':symbol_count}},
      {'id':'PO-TYPE-SAFETY','status':stat({'TYPE_MISMATCH','ARITY_MISMATCH','UNKNOWN_VALUE','TYPE_SYNTAX'}),'witness':{'checked_nodes':d['witnesses'].get('checked_nodes',0),'refined_values':len(d['value_types'])}},
      {'id':'PO-EFFECT-BOUNDS','status':stat({'EFFECT_BUDGET_EXCEEDED'}),'witness':{'effects':d['effects']}},
      {'id':'PO-LINEAR-OWNERSHIP','status':stat({'LINEAR_USE_AFTER_MOVE','LINEAR_ALIAS','QSTATE_GENERIC_MOVE','QSTATE_LEAK'}),'witness':{'live_exported':d['witnesses'].get('live_qstate_exports',[])}},
      {'id':'PO-CLOSURE','status':stat({'PORTAL_UNCLOSED','PORTAL_NOT_OPEN','ROAD_UNCLOSED','ROAD_NOT_OPEN'}),'witness':{'open_portals':d['witnesses'].get('open_portals',[]),'open_roads':d['witnesses'].get('open_roads',[])}},
      {'id':'PO-SECTOR-TRANSDUCTION','status':stat({'BRIDGE_REQUIRED','BRIDGE_MISMATCH','SECTOR_MISMATCH'}),'witness':{'bridges':d['witnesses'].get('bridge_witnesses',[])}},
      {'id':'PO-CAPABILITY','status':'PASS' if cap.get('ok') else 'FAIL','witness':{'required_features':cap.get('required_features',[])}},
      {'id':'PO-PROVENANCE','status':'PASS' if link_receipt is not None else 'PENDING','witness':{'link_receipt':None if link_receipt is None else link_receipt.get('link_id')}}
    ]
    return out
