class PackageError(Exception):
    code='PACKAGE_ERROR'
    def __init__(self,message,code=None):
        if code: self.code=code
        self.message=message
        super().__init__(f'{self.code}: {message}')

class ManifestError(PackageError): code='MANIFEST_INVALID'
class ResolutionError(PackageError): code='DEPENDENCY_CONFLICT'
class StoreError(PackageError): code='PACKAGE_HASH_MISMATCH'
