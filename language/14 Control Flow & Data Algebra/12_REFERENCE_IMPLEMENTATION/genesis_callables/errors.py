class CallableError(Exception):
    def __init__(self, message, code='CALLABLE_ERROR', file=None, line=None):
        self.code=code; self.file=file; self.line=line
        loc=''
        if file: loc += f' {file}'
        if line: loc += f':{line}'
        super().__init__(f'{code}{loc}: {message}')
