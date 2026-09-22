class RecursionErrorBase(Exception):
    def __init__(self,message,code='RECURSION_ERROR',file=None,line=None):
        self.message=message; self.code=code; self.file=file; self.line=line
        loc=f'{file}:{line}: ' if file and line else ''
        super().__init__(f'{loc}{code}: {message}')

class ParseError(RecursionErrorBase): pass
class CompileError(RecursionErrorBase): pass
class VerifyError(RecursionErrorBase): pass
class RuntimeFault(RecursionErrorBase): pass
