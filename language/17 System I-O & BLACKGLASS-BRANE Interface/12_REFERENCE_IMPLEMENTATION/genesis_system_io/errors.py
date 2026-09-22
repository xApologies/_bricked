class GenesisSystemError(RuntimeError):
    pass

def fail(code: str, detail: str = ""):
    msg = code if not detail else f"{code}: {detail}"
    raise GenesisSystemError(msg)
