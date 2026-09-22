from pathlib import Path
from dataclasses import asdict
import hashlib,json,copy
from .effects import CAPABILITIES
from .operators import operator_from_spec
from .selectors import resolve_selector
from .view import TransformView
from .delta import TransformationDeltaWriter,TransformationDeltaSegment
from .invariants import check_invariants
from .model import TransformPlan,TransformResult
from .util import digest_obj,stable_json,now_ns,file_sha256
from .errors import AdmissionError,StaleParentError,IdentityPolicyError,TransformationError
from .brane import TransformBraneAdapter
from .ledger import TransformationLedger

class TransformationEngine:
    def __init__(self,fabric,output_dir,ledger_path=None):
        self.fabric=fabric; self.output_dir=Path(output_dir); self.output_dir.mkdir(parents=True,exist_ok=True); self.ledger=TransformationLedger(ledger_path or self.output_dir/'TRANSFORMATION_LEDGER.jsonl')
    def _chain(self,req): return list(req.segment_chain)
    def _effects(self,ops): return sorted({e.value for op in ops for e in op.effects})
    def _parent_hashes(self,paths): return {str(p):file_sha256(p) for p in paths}
    def _child_meta(self,parent,plan,delta_path,delta_hash,post_root):
        c=copy.deepcopy(parent); c['parent_instance_id']=parent['instance_id']; c['instance_id']=plan.child_instance_id
        if plan.identity_policy=='DERIVE_MMO': c['canonical_mmo_id']=plan.derived_mmo_id
        if plan.identity_policy=='DERIVE_REPRESENTATION': c['representation_id']=plan.derived_representation_id or (parent['representation_id']+'::'+plan.plan_id[:12])
        c['state']='LIVE'; c['segment_path']=str(delta_path); c['segment_sha256']=delta_hash; c['segment_chain']=list(parent.get('segment_chain') or [parent['segment_path']])+[str(delta_path)]
        c.setdefault('history',[]); c['history']=list(c['history'])+[{'event':'TRANSFORMATION_CLOSED','plan_id':plan.plan_id,'parent_instance_id':parent['instance_id'],'post_state_root':post_root,'timestamp_ns':now_ns()}]
        c.setdefault('provenance',[]); return c
    def plan(self,req):
        parent=req.parent_instance; chain=self._chain(req); view=TransformView(self.fabric,chain)
        try: pre=view.state_root(parent['region']['start'],parent['region']['count'])
        finally:view.close()
        if req.expected_parent_root and req.expected_parent_root!=pre: raise StaleParentError('parent root mismatch')
        ops=[operator_from_spec(s) for s in req.operators]; eff=self._effects(ops)
        cap=CAPABILITIES.get(req.capability_profile)
        if cap is None: raise AdmissionError('unknown capability')
        from .effects import Effect
        eset={Effect(e) for e in eff}
        if not cap.admits(eset): raise AdmissionError(f'effects denied by {cap.name}: '+','.join(sorted(eff)))
        if req.identity_policy not in {'PRESERVE_MMO','DERIVE_REPRESENTATION','DERIVE_MMO'}: raise IdentityPolicyError('identity policy')
        if req.identity_policy=='DERIVE_MMO' and not req.derived_mmo_id: raise IdentityPolicyError('derived_mmo_id required')
        canonical={'parent':parent['instance_id'],'pre':pre,'capability':req.capability_profile,'operators':req.operators,'invariants':asdict(req.invariants),'identity_policy':req.identity_policy,'derived_mmo_id':req.derived_mmo_id,'derived_representation_id':req.derived_representation_id}
        pid=digest_obj(canonical); cid=digest_obj({'parent':parent['instance_id'],'plan':pid})[:32]
        return TransformPlan(pid,parent['instance_id'],cid,pre,req.capability_profile,eff,req.operators,asdict(req.invariants),req.identity_policy,req.derived_mmo_id,req.derived_representation_id)
    def execute(self,req):
        plan=self.plan(req); parent=req.parent_instance; chain=self._chain(req); before_hashes=self._parent_hashes(chain); fabric_hash=file_sha256(self.fabric.path)
        staged={}; pview=TransformView(self.fabric,chain,staged={}); sview=TransformView(self.fabric,chain,staged=staged)
        try:
            ops=[operator_from_spec(s) for s in req.operators]
            for spec,op in zip(req.operators,ops):
                idxs=resolve_selector(parent,spec.get('selector',{'type':'all'}))
                if getattr(op,'group',False): op.apply_group(idxs,sview.read_index,lambda i,c:staged.__setitem__(i,c))
                else:
                    for idx in idxs: staged[idx]=op.apply(idx,sview.read_index(idx),{'parent':parent,'plan':plan})
            # sparse: remove unchanged writes
            changed=[i for i in sorted(staged) if staged[i]!=pview.read_index(i)]
            staged={i:staged[i] for i in changed}; sview.staged=staged
            post=sview.state_root(parent['region']['start'],parent['region']['count'])
            plan_dict=asdict(plan)
            # provisional child metadata used for invariant check
            child_meta=copy.deepcopy(parent); child_meta['instance_id']=plan.child_instance_id
            if plan.identity_policy=='DERIVE_MMO': child_meta['canonical_mmo_id']=plan.derived_mmo_id
            if plan.identity_policy=='DERIVE_REPRESENTATION': child_meta['representation_id']=plan.derived_representation_id or (parent['representation_id']+'::'+plan.plan_id[:12])
            invariant_results=check_invariants(parent,child_meta,changed,pview.read_index,sview.read_index,req.invariants)
        except Exception:
            pview.close(); sview.close(); raise
        pview.close(); sview.close()
        delta_path=self.output_dir/(plan.child_instance_id+'.gtd')
        pd=hashlib.sha256(parent['instance_id'].encode()).hexdigest(); cd=hashlib.sha256(plan.child_instance_id.encode()).hexdigest()
        writer=TransformationDeltaWriter(delta_path,parent['fabric_tag'],parent['region']['start'],parent['region']['count'],pd,cd,plan.plan_id,plan.pre_state_root,post)
        try:
            for i in changed: writer.write(i,staged[i])
            payload_hash=writer.finalize()
        except Exception:
            writer.abort(); raise
        delta_hash=file_sha256(delta_path)
        # reopen and independently reconstruct
        d=TransformationDeltaSegment(delta_path,verify=True); d.close()
        cchain=list(parent.get('segment_chain') or chain)+[str(delta_path)]; cview=TransformView(self.fabric,cchain)
        try: verified_post=cview.state_root(parent['region']['start'],parent['region']['count'])
        finally:cview.close()
        if verified_post!=post: raise TransformationError('post root re-read mismatch')
        if self._parent_hashes(chain)!=before_hashes: raise TransformationError('parent segment changed')
        if file_sha256(self.fabric.path)!=fabric_hash: raise TransformationError('base fabric changed')
        receipt={'kind':'TRANSFORMATION_CLOSURE_RECEIPT','status':'CLOSED','plan_id':plan.plan_id,'parent_instance_id':parent['instance_id'],'child_instance_id':plan.child_instance_id,'canonical_mmo_before':parent['canonical_mmo_id'],'canonical_mmo_after':child_meta['canonical_mmo_id'],'pre_state_root':plan.pre_state_root,'post_state_root':post,'changed_cells':len(changed),'effects':plan.effects,'capability_profile':plan.capability_profile,'invariants':invariant_results,'delta_payload_hash':payload_hash,'delta_file_sha256':delta_hash,'parent_segment_hashes':before_hashes,'base_fabric_sha256':fabric_hash,'timestamp_ns':now_ns()}
        child=self._child_meta(parent,plan,delta_path,delta_hash,post); child['provenance']=list(child.get('provenance',[]))+[{'transformation_receipt':receipt}]
        child['brane_m5']=TransformBraneAdapter().adapt(parent,child,asdict(plan),receipt)
        self.ledger.append(receipt)
        return TransformResult(child,asdict(plan),receipt,str(delta_path),len(changed),plan.pre_state_root,post)
