import copy
class BridgeBraneAdapter:
    def adapt(self,instance,receipt):
        bm=copy.deepcopy(instance.get('brane_m5',{}))
        bm.setdefault('I',{})['instance_id']=instance.get('instance_id'); bm['I']['canonical_mmo_id']=instance.get('canonical_mmo_id')
        bm.setdefault('D',{})['bridge_id']=receipt['bridge_id']; bm['D']['source_sector']=receipt['source_sector']; bm['D']['target_sector']=receipt['target_sector']; bm['D']['representation_views']=[receipt['source_representation_view_id'],receipt['target_representation_view_id']]
        bm.setdefault('Chi',{})['fabric_witness_id']=receipt['fabric_witness_id']; bm['Chi']['R_QG_relation_id']=receipt['common_ancestry']['relation_id']; bm['Chi']['current_sector']=receipt['target_sector']
        bm.setdefault('R',{})['bridge_depth']=int(bm.get('R',{}).get('bridge_depth',0))+1; bm['R']['last_bridge_closed']=True
        bm.setdefault('P',{})['bridge_receipt']=receipt
        return bm
