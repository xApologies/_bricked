class BootstrapError(RuntimeError):
    def __init__(self,code:str,detail:str=""):
        self.code=code; self.detail=detail
        super().__init__(code + (": "+detail if detail else ""))

def fail(code,detail=""):
    raise BootstrapError(code,detail)
