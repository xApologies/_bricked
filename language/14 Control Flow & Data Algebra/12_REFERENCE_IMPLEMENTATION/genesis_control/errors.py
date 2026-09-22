class ControlError(Exception):
    def __init__(self, message, code='CONTROL', file='<memory>', line=0):
        self.code=code; self.file=file; self.line=line
        super().__init__(f'{code} {file}:{line}: {message}')
class VerifyError(ControlError): pass
class RuntimeFault(ControlError): pass
class BytecodeError(ControlError): pass
