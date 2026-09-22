class TransformationError(Exception): pass
class AdmissionError(TransformationError): pass
class InvariantViolation(TransformationError): pass
class StaleParentError(TransformationError): pass
class DeltaIntegrityError(TransformationError): pass
class SelectorError(TransformationError): pass
class IdentityPolicyError(TransformationError): pass
