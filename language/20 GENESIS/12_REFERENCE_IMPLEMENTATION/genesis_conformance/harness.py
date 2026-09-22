from pathlib import Path
from .release import load_json, verify_release, verify_core_lock, verify_abi, verify_format
from genesis_bootstrap import BootstrapHarness
from .errors import ConformanceError

class V1ConformanceHarness:
    def __init__(self, section_root): self.root=Path(section_root)
    def run(self):
        rel=load_json(self.root/'01_RELEASE_FREEZE/GENESIS_V1_0_RELEASE_DESCRIPTOR.json')
        lock=load_json(self.root/'01_RELEASE_FREEZE/SECTION_01_19_CORE_LOCK.json')
        abi=load_json(self.root/'02_ABI_FREEZE/GENESIS_V1_0_ABI_FREEZE.json')
        fmt=load_json(self.root/'03_FORMAT_FREEZE/GENESIS_V1_0_FORMAT_FREEZE.json')
        a=verify_release(rel); b=verify_core_lock(lock); c=verify_abi(abi); d=verify_format(fmt)
        ctrl=self.root/'15_EXAMPLES/bootstrap_controller.gen'; front=self.root/'15_EXAMPLES/self_host_frontier.json'
        br=BootstrapHarness(ctrl,front).run()
        if not br.fixed_point: raise ConformanceError('V1_BOOTSTRAP_FIXED_POINT_LOST')
        if br.self_hosted: raise ConformanceError('V1_FALSE_FULL_SELF_HOST_CLAIM')
        receipt={'kind':'GENESIS_V1_CONFORMANCE_RECEIPT','version':'1.0.0','status':'PASS','release_root':a['release_root'],'core_lock_root':b['core_lock_root'],'abi_freeze_root':c['abi_freeze_root'],'format_freeze_root':d['format_freeze_root'],'bootstrap_status':br.status,'bootstrap_fixed_point':br.fixed_point,'full_self_host':br.self_hosted}
        return receipt
