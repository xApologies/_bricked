class PortalBraneAdapter:
    version='PORTAL_BRANE_M5_ADAPTER_V0_1'
    def adapt(self,source,dest,plan,receipt):
        sm=source.get('brane_m5',{}); depth=int(sm.get('R',{}).get('recursive_depth',len(source.get('history',[]))))+1
        return {
          'I':{'canonical_mmo_id':dest['canonical_mmo_id'],'instance_id':dest['instance_id'],'representation_id':dest['representation_id'],'source_instance_id':source['instance_id']},
          'D':{'inherited':sm.get('D',{}),'portal_id':plan['portal_id'],'corridor_edge_ids':plan['corridor']['edge_ids'],'corridor_domains':plan['corridor']['domains']},
          'Chi':{'fabric_tag':dest['fabric_tag'],'region':dest['region'],'content_root':receipt['destination_content_root'],'chirality_class':receipt['chirality_class'],'color_trajectory':plan['corridor']['color_trajectory']},
          'R':{'recursive_depth':depth,'source_instance_id':source['instance_id'],'portal_id':plan['portal_id'],'history_tail':dest.get('history',[])[-6:]},
          'P':{'inherited':sm.get('P',{}),'portal_receipt':receipt,'adapter_version':self.version},
        }
