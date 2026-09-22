class TransformBraneAdapter:
    def adapt(self,parent,child,plan,receipt):
        pm=parent.get('brane_m5',{})
        depth=int(pm.get('R',{}).get('recursive_depth',len(parent.get('history',[]))))+1
        return {
          'I':{'canonical_mmo_id':child['canonical_mmo_id'],'instance_id':child['instance_id'],'representation_id':child['representation_id'],'parent_instance_id':parent['instance_id']},
          'D':{'inherited':pm.get('D',{}),'transformation_plan_id':plan['plan_id'],'effects':plan['effects']},
          'Chi':{'fabric_tag':child['fabric_tag'],'region':child['region'],'post_state_root':receipt['post_state_root'],'effects':plan['effects']},
          'R':{'recursive_depth':depth,'parent_instance_id':parent['instance_id'],'transform_plan_id':plan['plan_id'],'history_tail':child.get('history',[])[-4:]},
          'P':{'inherited':pm.get('P',{}),'transformation_receipt':receipt},
        }
