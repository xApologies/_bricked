class ConcurrencyError(Exception):
    def __init__(self, message: str, code: str = "CONCURRENCY_ERROR"):
        self.code = code
        super().__init__(f"{code}: {message}")
