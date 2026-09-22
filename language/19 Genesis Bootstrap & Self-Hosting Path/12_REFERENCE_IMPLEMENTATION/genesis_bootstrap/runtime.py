from __future__ import annotations
from pathlib import Path
from genesis_system_io.runtime import SystemRuntime
from .compiler_port import CompilerAwareBraneHost

class BootstrapRuntime(SystemRuntime):
    def __init__(self,program,base:Path,compiler_id="python-oracle:genesis-system-0.6.0"):
        super().__init__(program,base)
        self.brane=CompilerAwareBraneHost(self.cas,compiler_id=compiler_id)
