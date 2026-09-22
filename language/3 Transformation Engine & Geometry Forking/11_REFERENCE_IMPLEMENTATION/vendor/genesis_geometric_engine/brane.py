from .util import digest_obj
class BraneM5Adapter:
    version='BRANE_M5_ADAPTER_V0_1'
    def adapt(self,bundle,plan,instance,receipts):
        I={'canonical_mmo_id':bundle.canonical_mmo_id,'instance_id':instance.instance_id,'representation_id':bundle.representation_id,
           'invariant_digest':digest_obj({'mmo':bundle.canonical_mmo_id,'representation':bundle.representation_id})}
        D={'dependencies':list(bundle.dependencies),'source_hashes':bundle.source_hashes,'parent_instance_id':instance.parent_instance_id}
        Chi={'fabric_tag':instance.fabric_tag,'region':{'start':instance.region.start,'count':instance.region.count},'segment_sha256':instance.segment_sha256,
             'mapping_profile':instance.mapping_profile,'roles':instance.roles}
        R={'state':instance.state,'history':list(instance.history),'parent_instance_id':instance.parent_instance_id}
        P={'provenance':list(bundle.provenance)+list(instance.provenance),'receipts':receipts,'adapter_version':self.version}
        return {'I':I,'D':D,'Chi':Chi,'R':R,'P':P}
